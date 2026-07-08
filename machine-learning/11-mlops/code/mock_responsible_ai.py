"""
Mock Responsible AI — demonstrates fairness metrics (demographic parity),
SHAP-style feature importance, and differential privacy concepts.
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification


# ---------------------------------------------------------------------------
# Fairness Metrics
# ---------------------------------------------------------------------------

def demographic_parity_difference(y_pred: np.ndarray, groups: np.ndarray) -> float:
    """Difference in positive prediction rates between groups."""
    unique_groups = np.unique(groups)
    rates = []
    for g in unique_groups:
        mask = groups == g
        rate = y_pred[mask].mean()
        rates.append(rate)
    return float(max(rates) - min(rates))


def equal_opportunity_difference(y_true: np.ndarray, y_pred: np.ndarray, groups: np.ndarray) -> float:
    """Difference in True Positive Rate between groups."""
    unique_groups = np.unique(groups)
    tprs = []
    for g in unique_groups:
        mask = groups == g
        tp = ((y_pred[mask] == 1) & (y_true[mask] == 1)).sum()
        actual_pos = (y_true[mask] == 1).sum()
        tpr = tp / actual_pos if actual_pos > 0 else 0
        tprs.append(tpr)
    return float(max(tprs) - min(tprs))


# ---------------------------------------------------------------------------
# SHAP-style Feature Importance (simplified)
# ---------------------------------------------------------------------------

def shap_importance(model, X: np.ndarray, n_samples: int = 50) -> dict:
    """Simulate SHAP values using a simple perturbation method."""
    X_ref = X[:n_samples]
    baseline = model.predict_proba(X_ref)[:, 1].mean()

    importances = {}
    for col_idx in range(X.shape[1]):
        X_perm = X_ref.copy()
        np.random.shuffle(X_perm[:, col_idx])
        perturbed = model.predict_proba(X_perm)[:, 1].mean()
        importances[col_idx] = float(baseline - perturbed)

    return importances


# ---------------------------------------------------------------------------
# Differential Privacy (mock DP-SGD)
# ---------------------------------------------------------------------------

def apply_dp_noise(gradients: np.ndarray, noise_multiplier: float = 1.0, max_grad_norm: float = 1.0) -> np.ndarray:
    """Apply gradient clipping + noise (DP-SGD style)."""
    norm = np.linalg.norm(gradients)
    if norm > max_grad_norm:
        gradients = gradients * (max_grad_norm / norm)
    noise = np.random.normal(0, noise_multiplier * max_grad_norm, size=gradients.shape)
    return gradients + noise


# ---------------------------------------------------------------------------
# Model Card
# ---------------------------------------------------------------------------

def generate_model_card() -> dict:
    return {
        "model_name": "MockClassifier",
        "version": "1.0.0",
        "intended_use": "Binary classification for demonstration",
        "training_data": {
            "source": "sklearn make_classification",
            "size": 1000,
            "features": 10,
        },
        "performance": {
            "accuracy": 0.87,
            "f1_score": 0.86,
        },
        "fairness": {
            "demographic_parity_diff": 0.03,
            "demographic_parity_threshold": 0.1,
        },
        "limitations": [
            "Synthetic data only — not validated on real-world data",
            "May not generalize to imbalanced distributions",
        ],
        "ethical_considerations": [
            "Evaluate on target population before deployment",
            "Monitor for drift in production",
        ],
    }


if __name__ == "__main__":
    print("=== Responsible AI Demo ===\n")

    X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
    X_train, X_test = X[:800], X[800:]
    y_train, y_test = y[:800], y[800:]

    model = LogisticRegression(max_iter=500)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Simulate two demographic groups
    rng = np.random.default_rng(42)
    groups = rng.integers(0, 2, size=len(y_test))

    dpd = demographic_parity_difference(y_pred, groups)
    eod = equal_opportunity_difference(y_test, y_pred, groups)

    print(f"Demographic Parity Diff: {dpd:.4f}  (target < 0.10)")
    print(f"Equal Opportunity Diff:  {eod:.4f}  (target < 0.10)")

    print("\n=== SHAP Feature Importance ===")
    imp = shap_importance(model, X_test)
    for col, val in sorted(imp.items(), key=lambda x: abs(x[1]), reverse=True):
        direction = "+" if val > 0 else "-"
        print(f"  Feature {col:2d}: {direction} {abs(val):.4f}")

    print("\n=== Differential Privacy (DP-SGD) ===")
    grad = np.random.randn(100)
    noisy_grad = apply_dp_noise(grad, noise_multiplier=0.8, max_grad_norm=1.0)
    noise_magnitude = np.linalg.norm(noisy_grad - grad)
    print(f"  Original gradient norm: {np.linalg.norm(grad):.4f}")
    print(f"  Noisy gradient norm:    {np.linalg.norm(noisy_grad):.4f}")
    print(f"  Added noise magnitude:  {noise_magnitude:.4f}")

    print("\n=== Model Card ===")
    card = generate_model_card()
    for k, v in card.items():
        print(f"  {k}: {v}")
