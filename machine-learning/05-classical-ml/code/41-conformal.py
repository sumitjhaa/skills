"""Conformal Prediction (split conformal) from scratch with analysis."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

class SplitConformal:
    def __init__(self, model, alpha=0.1):
        self.model = model
        self.alpha = float(alpha)
        self.cal_scores = None
        self.classes_ = None

    def fit(self, X, y):
        X_tr, X_cal, y_tr, y_cal = train_test_split(X, y, test_size=0.3, random_state=42)
        self.model.fit(X_tr, y_tr)
        self.classes_ = np.unique(y)
        probs = self.model.predict_proba(X_cal)
        self.cal_scores = np.asarray(1 - probs[np.arange(len(y_cal)), y_cal], dtype=np.float64)
        self.cal_labels = y_cal
        return self

    def predict_set(self, X, alpha=None):
        if alpha is None:
            alpha = float(self.alpha)
        q = np.quantile(self.cal_scores, 1.0 - float(alpha))
        probs = self.model.predict_proba(X)
        prediction_sets = []
        for p in probs:
            prediction_sets.append(list(np.where(1 - p <= q)[0]))
        return prediction_sets

    def __init__(self, model, alpha=0.1):
        self.model = model
        self.alpha = float(alpha)
        self.cal_scores = None
        self.classes_ = None

    def coverage(self, X, y, alpha=None):
        pred_sets = self.predict_set(X, alpha)
        covered = sum(1 for i, ps in enumerate(pred_sets) if y[i] in ps)
        return covered / len(y)

    def avg_set_size(self, X, alpha=None):
        pred_sets = self.predict_set(X, alpha)
        return np.mean([len(ps) for ps in pred_sets])

if __name__ == "__main__":
    np.random.seed(42)
    from sklearn.linear_model import LogisticRegression

    X, y = make_classification(n_samples=500, n_features=10, n_classes=3,
                               n_informative=5, random_state=42)

    model = LogisticRegression(max_iter=200)
    cp = SplitConformal(model, alpha=0.1)
    cp.fit(X, y)

    print("=== Split Conformal Prediction ===")
    pred_sets = cp.predict_set(X[:10])
    print(f"Sample prediction sets:")
    for i, ps in enumerate(pred_sets):
        print(f"  Sample {i}: {ps} (true label={y[i]})")

    # Coverage analysis across alphas
    print("\n=== Coverage vs Alpha ===")
    alphas = np.linspace(0.01, 0.5, 10)
    coverages = []
    sizes = []
    for alpha in alphas:
        cov = cp.coverage(X, y, alpha)
        sz = cp.avg_set_size(X, alpha=alpha)
        coverages.append(cov)
        sizes.append(sz)
        print(f"  alpha={alpha:.2f}: coverage={cov:.4f}, avg size={sz:.2f}")

    # Compare with sklearn
    print("\n=== Model Comparison ===")
    from sklearn.tree import DecisionTreeClassifier

    for name, m in [
        ("LogisticRegression", LogisticRegression(max_iter=200)),
        ("DecisionTree", DecisionTreeClassifier(max_depth=5, min_samples_leaf=10)),
    ]:
        cp2 = SplitConformal(m, alpha=0.1)
        cp2.fit(X, y)
        cov = cp2.coverage(X, y)
        sz = cp2.avg_set_size(X)
        print(f"  {name}: coverage={cov:.4f}, avg size={sz:.2f}")

    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(alphas, coverages, 'bo-', label='Empirical coverage')
    axes[0].plot(alphas, 1 - alphas, 'r--', label='Target (1-α)')
    axes[0].fill_between(alphas, 1 - alphas - 0.05, 1 - alphas + 0.05, alpha=0.1, color='r')
    axes[0].set_xlabel("α")
    axes[0].set_ylabel("Coverage")
    axes[0].set_title("Conformal Coverage vs α")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(alphas, sizes, 'go-')
    axes[1].set_xlabel("α")
    axes[1].set_ylabel("Avg prediction set size")
    axes[1].set_title("Efficiency vs α")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("../../assets/phase05/41-conformal.png")
    plt.close()
    print("\nFigure saved to 41-conformal.png")

    # Edge case: binary classification
    print("\n=== Edge Cases ===")
    X_bin, y_bin = make_classification(n_samples=200, n_features=5, n_classes=2, random_state=42)
    cp_bin = SplitConformal(LogisticRegression(max_iter=200), alpha=0.1)
    cp_bin.fit(X_bin, y_bin)
    cov_bin = cp_bin.coverage(X_bin, y_bin)
    sz_bin = cp_bin.avg_set_size(X_bin)
    print(f"  Binary: coverage={cov_bin:.4f}, avg size={sz_bin:.2f}")

    # Edge case: calibration scores distribution
    print(f"  Calibration score stats: min={cp.cal_scores.min():.4f}, "
          f"max={cp.cal_scores.max():.4f}, median={np.median(cp.cal_scores):.4f}")

    # Conformal guarantee check
    print(f"\nConformal guarantee (coverage >= 1-α): {cov_bin >= 0.90}")
