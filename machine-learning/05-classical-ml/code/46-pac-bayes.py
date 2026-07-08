"""PAC-Bayes bound demonstration with visualization."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

def kl_divergence(prior, posterior):
    prior = np.maximum(prior, 1e-15)
    posterior = np.maximum(posterior, 1e-15)
    return np.sum(prior * np.log(prior / posterior))

def pac_bayes_bound(emp_risk, kl, n, delta=0.05):
    eps = np.sqrt((kl + np.log(2 * np.sqrt(n) / delta)) / (2 * n))
    return min(emp_risk + eps, 1.0)

class GibbsClassifier:
    def __init__(self, n_models=50):
        self.n_models = n_models
        self.models = []

    def fit(self, X, y):
        n, d = X.shape
        self.models = []
        for _ in range(self.n_models):
            idx = np.random.choice(n, n, replace=True)
            X_boot, y_boot = X[idx], y[idx]
            from sklearn.linear_model import LogisticRegression
            m = LogisticRegression(max_iter=200)
            m.fit(X_boot, y_boot)
            self.models.append(m)
        emp_risk = self.empirical_risk(X, y)
        prior = np.ones(self.n_models) / self.n_models
        self.posterior = np.array([1.0 / self.n_models] * self.n_models)
        kl = kl_divergence(prior, self.posterior)
        bound = pac_bayes_bound(emp_risk, kl, n)
        return emp_risk, bound

    def predict(self, X):
        preds = np.array([m.predict(X) for m in self.models])
        return np.round(preds.mean(axis=0)).astype(int)

    def empirical_risk(self, X, y):
        return 1 - np.mean(self.predict(X) == y)

def bound_vs_n_models(X_tr, y_tr, X_te, y_te):
    n_values = [5, 10, 20, 50, 100, 200]
    bounds = []
    test_errors = []
    emp_risks = []
    for n_m in n_values:
        gc = GibbsClassifier(n_models=n_m)
        emp, bound = gc.fit(X_tr, y_tr)
        test_err = 1 - np.mean(gc.predict(X_te) == y_te)
        bounds.append(bound)
        test_errors.append(test_err)
        emp_risks.append(emp)
    return n_values, bounds, test_errors, emp_risks

if __name__ == "__main__":
    np.random.seed(42)
    print("=== PAC-Bayes Bound Demonstration ===")

    X, y = make_classification(n_samples=200, n_features=5, random_state=42)

    gc = GibbsClassifier(n_models=20)
    emp, bound = gc.fit(X, y)
    print(f"Gibbs classifier empirical risk: {emp:.4f}")
    print(f"PAC-Bayes bound: {bound:.4f}")
    print(f"Generalization gap bound: {bound - emp:.4f}")

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    test_acc = np.mean(gc.predict(X_te) == y_te)
    print(f"Test accuracy: {test_acc:.4f}")
    print(f"True generalization error: {1 - test_acc:.4f}")
    print(f"PAC-Bayes bound holds: {bound >= 1 - test_acc}")

    # Bound analysis vs number of models
    print("\n=== Bound vs Number of Models ===")
    n_vals, bounds, test_errs, emp_risks = bound_vs_n_models(X_tr, y_tr, X_te, y_te)
    for n_m, b, te, er in zip(n_vals, bounds, test_errs, emp_risks):
        print(f"  n_models={n_m:3d}: emp_risk={er:.4f}, bound={b:.4f}, test_err={te:.4f}")

    # Delta sensitivity
    print("\n=== Sensitivity to δ ===")
    for delta in [0.01, 0.05, 0.1, 0.2, 0.5]:
        gc_d = GibbsClassifier(n_models=20)
        emp_d, _ = gc_d.fit(X_tr, y_tr)
        kl = kl_divergence(np.ones(20) / 20, np.ones(20) / 20)
        b = pac_bayes_bound(emp_d, kl, len(X_tr), delta)
        print(f"  δ={delta:.2f}: bound={b:.4f}")

    # Comparison with ERM
    print("\n=== Comparison with ERM ===")
    from sklearn.linear_model import LogisticRegression
    erm = LogisticRegression(max_iter=200)
    erm.fit(X_tr, y_tr)
    erm_test_err = 1 - np.mean(erm.predict(X_te) == y_te)
    gc20 = GibbsClassifier(n_models=50)
    emp_gc, bound_gc = gc20.fit(X_tr, y_tr)
    gc_test_err = 1 - np.mean(gc20.predict(X_te) == y_te)
    print(f"  ERM test error:     {erm_test_err:.4f}")
    print(f"  Gibbs test error:   {gc_test_err:.4f}")
    print(f"  PAC-Bayes bound:    {bound_gc:.4f} (gap={bound_gc - emp_gc:.4f})")

    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(n_vals, emp_risks, 'o-', label='Empirical risk')
    axes[0].plot(n_vals, test_errs, 's-', label='Test error')
    axes[0].plot(n_vals, bounds, '^-', label='PAC-Bayes bound')
    axes[0].set_xlabel("Number of models (M)")
    axes[0].set_ylabel("Error / Bound")
    axes[0].set_title("PAC-Bayes Bound vs Ensemble Size")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Bound components
    gaps = [b - e for b, e in zip(bounds, emp_risks)]
    axes[0].fill_between(n_vals, emp_risks, bounds, alpha=0.2, color='gray', label='Gap')

    # KL divergence for different posteriors
    n_test = 50
    kl_vals = []
    for k in range(1, n_test):
        post = np.zeros(n_test)
        post[:k] = 1.0 / k
        prior = np.ones(n_test) / n_test
        kl_vals.append(kl_divergence(prior, post))
    axes[1].plot(range(1, n_test), kl_vals)
    axes[1].axvline(20, color='r', ls='--', label='M=20')
    axes[1].set_xlabel("Number of active models")
    axes[1].set_ylabel("KL(prior || posterior)")
    axes[1].set_title("KL Divergence for Sparse Posteriors")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("../../assets/phase05/46-pac-bayes.png")
    plt.close()
    print("\nFigure saved to 46-pac-bayes.png")

    # Edge case: deterministic posterior
    print("\n=== Edge Cases ===")
    prior = np.array([0.5, 0.5])
    post_det = np.array([1.0, 0.0])
    kl_det = kl_divergence(prior, post_det)
    print(f"  KL(prior=[0.5,0.5] || posterior=[1,0]) = {kl_det:.4f}")
    bound_det = pac_bayes_bound(0.1, kl_det, 100)
    print(f"  PAC-Bayes bound (det): {bound_det:.4f}")

    # Edge case: uniform posterior = prior → KL=0
    kl_zero = kl_divergence(prior, prior.copy())
    bound_zero = pac_bayes_bound(0.1, kl_zero, 100)
    print(f"  KL(prior || prior) = {kl_zero:.4f}")
    print(f"  PAC-Bayes bound (KL=0): {bound_zero:.4f}")
