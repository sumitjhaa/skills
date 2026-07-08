"""
Mock Drift Detection — implements statistical drift detection using
Population Stability Index (PSI) and Kolmogorov-Smirnov (KS) test,
similar to Evidently AI's approach.
"""

import numpy as np
from scipy.stats import ks_2samp


def compute_psi(expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
    """Population Stability Index — measures distribution shift."""
    expected_percents, edges = np.histogram(expected, bins=bins, range=(0, 1))
    actual_percents, _ = np.histogram(actual, bins=bins, range=(0, 1))

    expected_percents = expected_percents / expected_percents.sum() + 1e-8
    actual_percents = actual_percents / actual_percents.sum() + 1e-8

    psi = np.sum((actual_percents - expected_percents) * np.log(actual_percents / expected_percents))
    return float(psi)


def detect_drift(
    reference: np.ndarray,
    current: np.ndarray,
    feature_name: str = "feature",
    psi_threshold: float = 0.2,
    ks_alpha: float = 0.05,
) -> dict:
    """Run PSI + KS tests on a single feature."""
    psi = compute_psi(reference, current)
    ks_stat, ks_pvalue = ks_2samp(reference, current)

    drifted = psi > psi_threshold or ks_pvalue < ks_alpha

    return {
        "feature": feature_name,
        "psi": round(psi, 4),
        "psi_drift": psi > psi_threshold,
        "ks_statistic": round(ks_stat, 4),
        "ks_pvalue": round(ks_pvalue, 6),
        "ks_drift": ks_pvalue < ks_alpha,
        "drift_detected": drifted,
    }


def generate_report(reference_data: dict, current_data: dict) -> list[dict]:
    """Run drift detection on all features (like Evidently DataDriftPreset)."""
    results = []
    for feat_name in reference_data:
        ref = np.array(reference_data[feat_name])
        cur = np.array(current_data[feat_name])
        result = detect_drift(ref, cur, feature_name=feat_name)
        results.append(result)
    return results


if __name__ == "__main__":
    rng = np.random.default_rng(42)

    reference = {
        "age": rng.normal(35, 10, 1000),
        "income": rng.exponential(50, 1000),
        "click_rate": rng.beta(2, 5, 1000),
    }

    # Current — same distribution for age, shifted for income and click_rate
    current_no_drift = {
        "age": rng.normal(35, 10, 1000),
        "income": rng.exponential(50, 1000),
        "click_rate": rng.beta(2, 5, 1000),
    }

    current_with_drift = {
        "age": rng.normal(40, 12, 1000),  # shifted mean
        "income": rng.exponential(80, 1000),  # shifted
        "click_rate": rng.beta(5, 2, 1000),  # shifted
    }

    print("=== No Drift Scenario ===")
    for r in generate_report(reference, current_no_drift):
        status = "DRIFT" if r["drift_detected"] else "OK"
        print(f"  {r['feature']:12s} psi={r['psi']:.4f} ks_p={r['ks_pvalue']:.6f} [{status}]")

    print("\n=== Drift Scenario ===")
    for r in generate_report(reference, current_with_drift):
        status = "DRIFT" if r["drift_detected"] else "OK"
        print(f"  {r['feature']:12s} psi={r['psi']:.4f} ks_p={r['ks_pvalue']:.6f} [{status}]")
