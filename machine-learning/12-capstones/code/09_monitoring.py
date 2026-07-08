"""
12.09: ML Monitoring Platform
Monitor model predictions, detect data/concept drift,
track performance, and generate alerts with a dashboard.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Optional, Tuple
from scipy import stats
from datetime import datetime, timedelta
import json


# ─────────────────────────────────────────────
# Data Generation (simulated production)
# ─────────────────────────────────────────────

def generate_reference_data(n: int = 1000, n_features: int = 8, seed: int = 42) -> np.ndarray:
    """Generate reference (training) data distribution."""
    np.random.seed(seed)
    data = np.random.randn(n, n_features).astype(np.float64)
    # Add some structure
    data[:, 0] = data[:, 0] * 2 + 1  # feature 0: mean=1, std=2
    data[:, 1] = np.random.exponential(2, n)  # feature 1: exponential
    data[:, 2] = np.random.uniform(-3, 3, n)  # feature 2: uniform
    data[:, 3] = np.random.beta(2, 5, n)  # feature 3: beta
    data[:, 4] = np.random.poisson(3, n).astype(np.float64)  # feature 4: poisson
    data[:, 5:8] = np.random.randn(n, 3) * 0.5  # features 5-7: narrow normal
    return data


def generate_production_data(reference: np.ndarray, n_batches: int = 50,
                              batch_size: int = 20, drift_start: int = 20) -> List[np.ndarray]:
    """Simulate production data with drift after a certain point."""
    np.random.seed(123)
    _, n_features = reference.shape
    batches = []

    for i in range(n_batches):
        if i < drift_start:
            # No drift: sample from reference
            idx = np.random.choice(len(reference), batch_size)
            batch = reference[idx].copy()
        else:
            # Data drift: shift mean and scale
            drift_strength = min(1.0, (i - drift_start) / 10)
            base = np.random.randn(batch_size, n_features).astype(np.float64)
            # Shift features 0, 1, 2 increasingly
            base[:, 0] = base[:, 0] * 2 + 1 + drift_strength * 2
            base[:, 1] = np.random.exponential(2 + drift_strength, batch_size)
            base[:, 2] = np.random.uniform(-3 + drift_strength, 3 + drift_strength, batch_size)
            base[:, 3:8] = np.random.randn(batch_size, n_features - 3) * 0.5
            batch = base

        batches.append(batch.astype(np.float64))

    return batches


def generate_predictions(model_accuracy: float = 0.85, n_batches: int = 50,
                         batch_size: int = 20, perf_drop: int = 35) -> List[Tuple[np.ndarray, np.ndarray]]:
    """Simulate predictions with ground truth. Performance drops after perf_drop."""
    np.random.seed(456)
    results = []
    for i in range(n_batches):
        if i < perf_drop:
            acc = model_accuracy
        else:
            acc = max(0.5, model_accuracy - 0.3 * min(1.0, (i - perf_drop) / 10))

        predictions = np.random.randint(0, 2, batch_size)
        correct = np.random.random(batch_size) < acc
        ground_truth = np.where(correct, predictions, 1 - predictions)
        results.append((predictions, ground_truth))

    return results


# ─────────────────────────────────────────────
# Drift Detection
# ─────────────────────────────────────────────

class DriftDetector:
    """Detect data drift using statistical tests."""

    @staticmethod
    def psi(reference: np.ndarray, current: np.ndarray, n_bins: int = 10) -> float:
        """Population Stability Index."""
        all_vals = np.concatenate([reference, current])
        bins = np.linspace(np.min(all_vals), np.max(all_vals), n_bins + 1)
        ref_hist, _ = np.histogram(reference, bins=bins, density=True)
        cur_hist, _ = np.histogram(current, bins=bins, density=True)
        ref_hist = ref_hist / ref_hist.sum()
        cur_hist = cur_hist / cur_hist.sum()
        ref_hist = np.clip(ref_hist, 1e-10, None)
        cur_hist = np.clip(cur_hist, 1e-10, None)
        psi_val = np.sum((ref_hist - cur_hist) * np.log(ref_hist / cur_hist))
        return float(psi_val)

    @staticmethod
    def ks_test(reference: np.ndarray, current: np.ndarray) -> Tuple[float, float]:
        """Kolmogorov-Smirnov test.
        Returns: (statistic, p-value)
        """
        stat, pval = stats.ks_2samp(reference, current)
        return float(stat), float(pval)

    @staticmethod
    def chi_squared(reference: np.ndarray, current: np.ndarray, n_bins: int = 10) -> Tuple[float, float]:
        """Chi-squared test for categorical/discretized data.
        Returns: (statistic, p-value)
        """
        all_vals = np.concatenate([reference, current])
        bins = np.linspace(np.min(all_vals), np.max(all_vals), n_bins + 1)
        ref_hist, _ = np.histogram(reference, bins=bins)
        cur_hist, _ = np.histogram(current, bins=bins)
        # Normalize to same total count
        ref_hist = ref_hist / ref_hist.sum() * len(current)
        mask = ref_hist > 0
        if not mask.any():
            return 0.0, 1.0
        chi2 = np.sum((cur_hist[mask] - ref_hist[mask]) ** 2 / ref_hist[mask])
        pval = 1 - stats.chi2.cdf(chi2, mask.sum() - 1)
        return float(chi2), float(pval)


class ConceptDriftDetector:
    """Detect concept drift using Page-Hinkley and DDM."""

    @staticmethod
    def page_hinkley(errors: np.ndarray, threshold: float = 20, alpha: float = 0.05) -> Tuple[bool, int]:
        """Page-Hinkley test for change detection."""
        cum_sum = 0
        min_cum = 0
        mean_est = errors[0]

        for t, error in enumerate(errors):
            mean_est = mean_est + alpha * (error - mean_est)
            cum_sum += error - mean_est - 0.001  # delta parameter
            min_cum = min(min_cum, cum_sum)
            if cum_sum - min_cum > threshold:
                return True, t
        return False, -1

    @staticmethod
    def ddm(errors: np.ndarray, warning_level: float = 2.0,
            drift_level: float = 3.0) -> Tuple[str, int]:
        """Drift Detection Method."""
        n = len(errors)
        p_min = float('inf')
        s_min = float('inf')
        p_mean = 0.0
        p_std = 0.0
        state = "normal"

        for t, error in enumerate(errors):
            p_mean = (p_mean * t + error) / (t + 1)
            p_std = np.sqrt(p_mean * (1 - p_mean) / (t + 1))

            if p_mean + p_std < p_min + s_min:
                p_min = p_mean
                s_min = p_std

            if p_mean + p_std > p_min + drift_level * s_min:
                return "drift", t
            elif p_mean + p_std > p_min + warning_level * s_min:
                state = "warning"

        return state, -1


# ─────────────────────────────────────────────
# Performance Monitor
# ─────────────────────────────────────────────

class PerformanceTracker:
    """Track model performance over time using sliding windows."""
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.correct = []
        self.total = []

    def update(self, predictions: np.ndarray, ground_truth: np.ndarray):
        self.correct.extend((predictions == ground_truth).tolist())
        self.total.extend([1] * len(predictions))

    def accuracy(self) -> float:
        if not self.total:
            return 0.0
        window_correct = sum(self.correct[-self.window_size:])
        window_total = sum(self.total[-self.window_size:])
        return window_correct / window_total if window_total > 0 else 0.0

    def precision_recall_f1(self, predictions: np.ndarray,
                            ground_truth: np.ndarray) -> Dict:
        tp = np.sum((predictions == 1) & (ground_truth == 1))
        fp = np.sum((predictions == 1) & (ground_truth == 0))
        fn = np.sum((predictions == 0) & (ground_truth == 1))

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

        return {'precision': precision, 'recall': recall, 'f1': f1}


# ─────────────────────────────────────────────
# Alert Engine
# ─────────────────────────────────────────────

class Alert:
    def __init__(self, severity: str, message: str, timestamp: float, metric: str):
        self.severity = severity
        self.message = message
        self.timestamp = timestamp
        self.metric = metric

    def __repr__(self):
        t = datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return f"[{self.severity.upper()}] {t} | {self.message}"


class AlertEngine:
    """Threshold-based and trend-based alerting."""
    def __init__(self, cooldown_seconds: float = 60):
        self.cooldown = cooldown_seconds
        self.alerts: List[Alert] = []
        self._last_alert_time = {}

    def check_threshold(self, value: float, threshold: float, metric: str,
                        direction: str = 'above', severity: str = 'WARN') -> Optional[Alert]:
        triggered = (value > threshold) if direction == 'above' else (value < threshold)
        if not triggered:
            return None

        now = time.time()
        last_time = self._last_alert_time.get(metric, 0)
        if now - last_time < self.cooldown:
            return None

        self._last_alert_time[metric] = now
        alert = Alert(severity, f"{metric} = {value:.4f} (threshold: {threshold})", now, metric)
        self.alerts.append(alert)
        return alert

    def check_trend(self, values: List[float], window: int = 5,
                    metric: str = 'accuracy', severity: str = 'CRITICAL') -> Optional[Alert]:
        if len(values) < window * 2:
            return None

        recent = values[-window:]
        older = values[-2 * window:-window]
        if np.mean(recent) < np.mean(older) - 0.05:
            now = time.time()
            last_time = self._last_alert_time.get(f"{metric}_trend", 0)
            if now - last_time >= self.cooldown:
                self._last_alert_time[f"{metric}_trend"] = now
                alert = Alert(severity,
                              f"{metric} dropping: {np.mean(older):.4f} → {np.mean(recent):.4f}",
                              now, metric)
                self.alerts.append(alert)
                return alert
        return None

    def get_recent_alerts(self, n: int = 10) -> List[Alert]:
        return self.alerts[-n:]


# ─────────────────────────────────────────────
# Monitoring Dashboard
# ─────────────────────────────────────────────

class MonitoringDashboard:
    """Generate monitoring dashboard plots."""
    def __init__(self):
        self.history = {
            'psi': [],
            'ks_stat': [],
            'chi2_stat': [],
            'accuracy': [],
            'timestamps': [],
        }

    def update(self, metrics: Dict, timestamp: float):
        for k, v in metrics.items():
            if k in self.history:
                self.history[k].append(v)
        self.history['timestamps'].append(timestamp)

    def plot(self, save_path: str = '../../assets/phase12/09_monitoring_dashboard.png'):
        fig, axes = plt.subplots(2, 3, figsize=(16, 9))

        times = self.history['timestamps']
        if len(times) == 0:
            return

        # Time labels
        time_labels = list(range(len(times)))

        # 1. PSI over time
        if self.history['psi']:
            ax = axes[0, 0]
            ax.plot(time_labels, self.history['psi'], 'r-', linewidth=2)
            ax.axhline(y=0.1, color='orange', linestyle='--', alpha=0.7, label='Warning')
            ax.axhline(y=0.25, color='red', linestyle='--', alpha=0.7, label='Drift')
            ax.set_xlabel('Batch')
            ax.set_ylabel('PSI')
            ax.set_title('Population Stability Index')
            ax.legend()
            ax.grid(alpha=0.3)

        # 2. KS statistic over time
        if self.history['ks_stat']:
            ax = axes[0, 1]
            ax.plot(time_labels, self.history['ks_stat'], 'b-', linewidth=2)
            ax.axhline(y=0.1, color='orange', linestyle='--', alpha=0.7)
            ax.set_xlabel('Batch')
            ax.set_ylabel('KS Statistic')
            ax.set_title('KS Test (Feature 0)')
            ax.grid(alpha=0.3)

        # 3. Chi-squared over time
        if self.history['chi2_stat']:
            ax = axes[0, 2]
            ax.plot(time_labels, self.history['chi2_stat'], 'g-', linewidth=2)
            ax.set_xlabel('Batch')
            ax.set_ylabel('Chi-squared')
            ax.set_title('Chi-squared Test (Feature 3)')
            ax.grid(alpha=0.3)

        # 4. Accuracy over time
        if self.history['accuracy']:
            ax = axes[1, 0]
            ax.plot(time_labels, self.history['accuracy'], 'purple', linewidth=2)
            ax.axhline(y=0.8, color='green', linestyle='--', alpha=0.7, label='Target')
            ax.axhline(y=0.7, color='orange', linestyle='--', alpha=0.7, label='Warning')
            ax.set_xlabel('Batch')
            ax.set_ylabel('Accuracy')
            ax.set_title('Model Performance')
            ax.set_ylim(0.4, 1.0)
            ax.legend()
            ax.grid(alpha=0.3)

        # 5. Alerts timeline
        ax = axes[1, 1]
        ax.text(0.5, 0.5, 'See alert log in console output',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=12, style='italic', color='gray')
        ax.set_title('Alerts')
        ax.axis('off')

        # 6. Feature drift heatmap (summary)
        ax = axes[1, 2]
        if len(self.history['psi']) > 0:
            n_feats = min(8, len(self.history.get('feature_psi', [])))
            if n_feats > 0:
                heatmap_data = np.array(self.history.get('feature_psi', []))
                if heatmap_data.ndim == 1:
                    heatmap_data = heatmap_data.reshape(1, -1)
                im = ax.imshow(heatmap_data, cmap='Reds', aspect='auto')
                ax.set_xlabel('Feature')
                ax.set_ylabel('Time')
                ax.set_title('Feature Drift (PSI)')
                plt.colorbar(im, ax=ax)
            else:
                # Show recent PSI values as bar chart
                psi_vals = self.history['psi'][-10:]
                ax.bar(range(len(psi_vals)), psi_vals, color='coral', alpha=0.7)
                ax.axhline(y=0.1, color='orange', linestyle='--')
                ax.set_xlabel('Recent batches')
                ax.set_ylabel('PSI')
                ax.set_title('Recent PSI Values')
                ax.grid(alpha=0.3)

        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        plt.close()


# ─────────────────────────────────────────────
# Main monitoring simulation
# ─────────────────────────────────────────────

import time

def main():
    print("=" * 60)
    print("ML MONITORING PLATFORM")
    print("=" * 60)

    # Generate data
    print("\n[1] Generating data...")
    reference = generate_reference_data(1000, 8)
    prod_batches = generate_production_data(reference, n_batches=40, batch_size=20, drift_start=15)
    perf_data = generate_predictions(model_accuracy=0.88, n_batches=40, batch_size=20, perf_drop=25)

    # Initialize components
    drift_detector = DriftDetector()
    concept_detector = ConceptDriftDetector()
    perf_tracker = PerformanceTracker(window_size=50)
    alert_engine = AlertEngine(cooldown_seconds=10)
    dashboard = MonitoringDashboard()

    # Store per-feature PSI
    feature_psi_history = []

    print("[2] Running monitoring simulation...")
    print()

    for batch_idx, (batch, (preds, truth)) in enumerate(zip(prod_batches, perf_data)):
        timestamp = time.time()

        # ── Data Drift Detection ──
        # Feature 0: PSI
        psi_0 = drift_detector.psi(reference[:, 0], batch[:, 0])
        # Feature 0: KS test
        ks_stat, ks_pval = drift_detector.ks_test(reference[:, 0], batch[:, 0])
        # Feature 3: Chi-squared
        chi2, chi2_pval = drift_detector.chi_squared(reference[:, 3], batch[:, 3])

        # Per-feature PSI (for heatmap)
        feature_psi = [drift_detector.psi(reference[:, f], batch[:, f]) for f in range(min(8, batch.shape[1]))]
        feature_psi_history.append(feature_psi)

        # ── Performance Tracking ──
        perf_tracker.update(preds, truth)
        accuracy = perf_tracker.accuracy()

        # ── Concept Drift ──
        if batch_idx < len(perf_data) - 1:
            errors = 1 - (preds == truth).astype(float)
            ph_drift, ph_point = concept_detector.page_hinkley(errors, threshold=10)

        # ── Alerts ──
        if psi_0 > 0.1:
            alert_engine.check_threshold(psi_0, 0.1, f"PSI_feat0", 'above', 'WARN')
        if psi_0 > 0.25:
            alert_engine.check_threshold(psi_0, 0.25, f"PSI_feat0", 'above', 'CRITICAL')
        if ks_stat > 0.15:
            alert_engine.check_threshold(ks_stat, 0.15, f"KS_feat0", 'above', 'WARN')
        if accuracy < 0.70:
            alert_engine.check_threshold(accuracy, 0.70, "accuracy", 'below', 'CRITICAL')

        # Trend-based alert on accuracy
        dashboard.history['accuracy'].append(accuracy)
        if len(dashboard.history['accuracy']) > 5:
            alert_engine.check_trend(dashboard.history['accuracy'], window=5, metric='accuracy')

        # ── Dashboard Update ──
        dashboard.update({
            'psi': psi_0,
            'ks_stat': ks_stat,
            'chi2_stat': chi2,
            'accuracy': accuracy,
        }, timestamp)
        dashboard.history['feature_psi'] = feature_psi_history

        # Print periodic status
        if (batch_idx + 1) % 10 == 0:
            drift_status = "DRIFT" if psi_0 > 0.1 else "OK"
            print(f"  Batch {batch_idx+1:2d}/40 | PSI: {psi_0:.4f} | KS: {ks_stat:.4f} | "
                  f"Acc: {accuracy:.4f} | Status: {drift_status}")

    # ── Summary ──
    print("\n" + "=" * 60)
    print("MONITORING SUMMARY")
    print("=" * 60)

    # Recent alerts
    recent_alerts = alert_engine.get_recent_alerts(5)
    print(f"\nRecent Alerts ({len(recent_alerts)}):")
    for alert in recent_alerts:
        print(f"  {alert}")

    # Overall stats
    final_accuracy = perf_tracker.accuracy()
    avg_psi = np.mean(dashboard.history['psi'])
    max_psi = max(dashboard.history['psi'])
    print(f"\nFinal Accuracy: {final_accuracy:.4f}")
    print(f"Average PSI: {avg_psi:.4f}")
    print(f"Max PSI: {max_psi:.4f}")
    print(f"Total Alerts: {len(alert_engine.alerts)}")

    # Detection time for drift
    psi_over_threshold = [i for i, p in enumerate(dashboard.history['psi']) if p > 0.1]
    if psi_over_threshold:
        first_drift = psi_over_threshold[0]
        print(f"First drift detected at batch: {first_drift + 1} "
              f"(actual drift started at batch 16)")

    # Generate dashboard plot
    dashboard.plot('09_monitoring_dashboard.png')
    print("\nSaved 09_monitoring_dashboard.png")

    # Drift comparison plot
    fig, ax = plt.subplots(figsize=(10, 4))
    batch_nums = list(range(1, len(dashboard.history['psi']) + 1))
    ax.plot(batch_nums, dashboard.history['psi'], 'r-', linewidth=2, label='PSI (Data Drift)')
    ax.plot(batch_nums, dashboard.history['accuracy'], 'purple', linewidth=2, label='Accuracy (Performance)')
    ax.axvline(x=16, color='gray', linestyle='--', alpha=0.5, label='Drift injected')
    ax.set_xlabel('Batch')
    ax.set_ylabel('Metric Value')
    ax.set_title('Data Drift vs Model Performance')
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase12/09_monitoring_drift_vs_perf.png', dpi=150)
    plt.close()
    print("Saved 09_monitoring_drift_vs_perf.png")


if __name__ == '__main__':
    main()
