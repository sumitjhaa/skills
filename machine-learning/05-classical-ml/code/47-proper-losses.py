"""Proper Loss Functions: Brier, Log-loss, Hinge comparison with calibration."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

def brier_loss(p, y):
    return (p - y)**2

def log_loss(p, y):
    p = np.clip(p, 1e-15, 1 - 1e-15)
    return -(y * np.log(p) + (1 - y) * np.log(1 - p))

def hinge_loss(f, y):
    return np.maximum(0, 1 - (2 * y - 1) * f)

def zero_one_loss(p, y, threshold=0.5):
    return ((p >= threshold) != y).astype(float)

def plot_losses():
    p = np.linspace(0.001, 0.999, 100)
    y = 1
    x = np.log(p / (1 - p))  # logit

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].plot(p, brier_loss(p, y), label='Brier (quadratic)', lw=2)
    axes[0].plot(p, log_loss(p, y), label='Log-loss (cross-entropy)', lw=2)
    axes[0].plot(p, hinge_loss(x, y), label='Hinge (score-based)', lw=2, alpha=0.7)
    axes[0].plot(p, zero_one_loss(p, y), label='0-1 loss', lw=2, ls='--')
    axes[0].set_xlabel('Predicted probability p')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Binary Loss Functions (y=1)')
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # Expected loss minimization
    p_grid = np.linspace(0.01, 0.99, 99)
    true_ps = [0.3, 0.5, 0.7]
    for true_p in true_ps:
        exp_brier = true_p * brier_loss(p_grid, 1) + (1 - true_p) * brier_loss(p_grid, 0)
        min_idx = np.argmin(exp_brier)
        axes[1].plot(p_grid, exp_brier, label=f'p*={true_p}')
        axes[1].axvline(p_grid[min_idx], ls='--', alpha=0.5,
                        color=f'C{true_ps.index(true_p)}')
    axes[1].set_xlabel('Predicted probability')
    axes[1].set_ylabel('Expected Brier loss')
    axes[1].set_title('Brier is proper: minimum at p = p*')
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("../../assets/phase05/47-proper-losses.png")
    plt.close()

def calibration_curve(y_true, y_prob, n_bins=10):
    bins = np.linspace(0, 1, n_bins + 1)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    frac_pos = np.zeros(n_bins)
    count = np.zeros(n_bins)
    for i in range(n_bins):
        idx = (y_prob >= bins[i]) & (y_prob < bins[i + 1])
        if idx.sum() > 0:
            frac_pos[i] = y_true[idx].mean()
            count[i] = idx.sum()
    return bin_centers, frac_pos, count

if __name__ == "__main__":
    print("=== Proper Loss Functions ===")
    plot_losses()
    print("Loss function comparison plot saved.")

    X, y = make_classification(n_samples=1000, random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    lr = LogisticRegression(max_iter=200).fit(X_tr, y_tr)
    p = lr.predict_proba(X_te)[:, 1]
    scores = lr.decision_function(X_te)

    print(f"\nBrier score: {np.mean(brier_loss(p, y_te)):.4f}")
    print(f"Log-loss:    {np.mean(log_loss(p, y_te)):.4f}")
    print(f"Hinge loss:  {np.mean(hinge_loss(scores, y_te)):.4f}")

    # Comparison across models
    print("\n=== Model Comparison ===")
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.naive_bayes import GaussianNB

    for name, model in [
        ("LogisticRegression", LogisticRegression(max_iter=200)),
        ("DecisionTree", DecisionTreeClassifier(max_depth=5)),
        ("GaussianNB", GaussianNB()),
    ]:
        model.fit(X_tr, y_tr)
        p_m = model.predict_proba(X_te)[:, 1]
        brier = np.mean(brier_loss(p_m, y_te))
        ll = np.mean(log_loss(p_m, y_te))
        print(f"  {name}: Brier={brier:.4f}, LogLoss={ll:.4f}")

    # Calibration analysis
    print("\n=== Calibration ===")
    bin_centers, frac_pos, counts = calibration_curve(y_te, p, n_bins=10)
    for i in range(len(bin_centers)):
        if counts[i] > 0:
            print(f"  [{bin_centers[i]:.2f}] frac_pos={frac_pos[i]:.3f}, count={int(counts[i])}")

    ece = np.sum(counts * np.abs(frac_pos - bin_centers)) / counts.sum()
    print(f"  Expected Calibration Error: {ece:.4f}")

    # Proper vs improper: show that log-loss is proper
    print("\n=== Properness Check ===")
    print("Log-loss E[L(p, y)] = p*·log(p) + (1-p*)·log(1-p)")
    print("  minimizer = p* (proper)")
    print("Hinge E[L(f, y)] = p*·max(0, 1-f) + (1-p*)·max(0, 1+f)")
    print("  minimizer = sign(p* - 0.5) (classification-calibrated but not proper)")

    # Edge case: perfect prediction
    print("\n=== Edge Cases ===")
    p_perfect = np.array([1.0, 0.0, 1.0])
    y_perfect = np.array([1, 0, 1])
    print(f"  Perfect predictions: Brier={np.mean(brier_loss(p_perfect, y_perfect)):.4f}")

    p_all_wrong = np.array([0.0, 1.0, 0.0])
    print(f"  All wrong: Brier={np.mean(brier_loss(p_all_wrong, y_perfect)):.4f}")

    # Hinge vs Brier vs Log-loss for a specific instance
    p_instance = 0.7
    y_instance = 1
    f_instance = np.log(p_instance / (1 - p_instance))
    print(f"\n  Loss values for p=0.7, y=1:")
    print(f"    Brier:    {brier_loss(p_instance, y_instance):.4f}")
    print(f"    Log-loss: {log_loss(p_instance, y_instance):.4f}")
    print(f"    Hinge:    {hinge_loss(f_instance, y_instance):.4f}")
