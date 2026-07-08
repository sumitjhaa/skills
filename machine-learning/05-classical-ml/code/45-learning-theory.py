"""Learning Theory: VC dimension estimation and PAC bounds with visualization."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

def vc_dim_linear(d):
    return d + 1

def pac_bound_hoeffding(n, d, delta=0.05):
    vc = vc_dim_linear(d)
    eps = np.sqrt((vc * (np.log(2 * n / vc) + 1) + np.log(1 / delta)) / n)
    return eps

def emp_risk_minimization(X, y, X_test, y_test):
    model = LogisticRegression(max_iter=200)
    model.fit(X, y)
    train_err = np.mean(model.predict(X) != y)
    test_err = np.mean(model.predict(X_test) != y_test)
    return train_err, test_err

def structural_risk_minimization(X, y, delta=0.05):
    n, d = X.shape
    best_idx = 0
    best_sr = float('inf')
    results = []
    for d_eff in range(1, d + 1):
        X_sub = X[:, :d_eff]
        model = LogisticRegression(max_iter=200)
        model.fit(X_sub, y)
        train_err = np.mean(model.predict(X_sub) != y)
        vc = d_eff + 1
        pen = np.sqrt((vc * (np.log(2 * n / vc) + 1) + np.log(np.log2(2 * n / vc)) + np.log(1 / delta)) / n)
        sr = train_err + pen
        results.append((d_eff, train_err, pen, sr))
        if sr < best_sr:
            best_sr = sr
            best_idx = d_eff
    return best_idx, best_sr, results

if __name__ == "__main__":
    np.random.seed(42)
    print("=== Learning Theory: VC Dimension & PAC Bounds ===\n")

    X, y = make_classification(n_samples=500, n_features=10, random_state=42)
    split = 300
    X_tr, X_te = X[:split], X[split:]
    y_tr, y_te = y[:split], y[split:]

    train_err, test_err = emp_risk_minimization(X_tr, y_tr, X_te, y_te)
    print(f"Empirical Risk: train={train_err:.4f}, test={test_err:.4f}")

    eps = pac_bound_hoeffding(len(y_tr), X_tr.shape[1])
    print(f"PAC bound epsilon: {eps:.4f}")
    print(f"Generalization bound: R(h) ≤ {train_err:.4f} + {eps:.4f} = {train_err + eps:.4f}")
    bound_holds = test_err <= train_err + eps
    print(f"Bound holds: {bound_holds}")

    best_d, best_sr, srm_results = structural_risk_minimization(X_tr, y_tr)
    print(f"\nSRM selected d={best_d}, penalized risk={best_sr:.4f}")

    # SVM model complexity
    print(f"\nSVM complexity analysis:")
    for C in [0.01, 0.1, 1.0, 10.0, 100.0]:
        model = SVC(C=C, kernel='linear', gamma='scale').fit(X_tr, y_tr)
        te = np.mean(model.predict(X_te) != y_te)
        print(f"  C={C:6.2f} test error: {te:.4f}")

    # PAC bound vs sample size
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    ns = np.arange(20, 1000, 10)
    for d, c in zip([2, 5, 10, 20], ['C0', 'C1', 'C2', 'C3']):
        eps_vals = [pac_bound_hoeffding(n, d) for n in ns]
        axes[0, 0].plot(ns, eps_vals, c=c, label=f'd={d}')
    axes[0, 0].set_xlabel("Sample size n")
    axes[0, 0].set_ylabel("PAC bound ε")
    axes[0, 0].set_title("PAC Bound vs Sample Size")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # SRM complexity penalty
    d_vals = np.arange(1, 21)
    for n, c in zip([50, 200, 500, 2000], ['C0', 'C1', 'C2', 'C3']):
        pen_vals = [np.sqrt((vc_dim_linear(d) * (np.log(2 * n / vc_dim_linear(d)) + 1) + np.log(1 / 0.05)) / n)
                    for d in d_vals]
        axes[0, 1].plot(d_vals, pen_vals, c=c, label=f'n={n}')
    axes[0, 1].set_xlabel("VC dimension (d+1)")
    axes[0, 1].set_ylabel("Complexity penalty")
    axes[0, 1].set_title("SRM Complexity Penalty")
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # SRM detailed results
    d_effs = [r[0] for r in srm_results]
    train_errs = [r[1] for r in srm_results]
    pens = [r[2] for r in srm_results]
    srs = [r[3] for r in srm_results]
    axes[1, 0].plot(d_effs, train_errs, 'o-', label='Empirical risk')
    axes[1, 0].plot(d_effs, pens, 's-', label='Penalty')
    axes[1, 0].plot(d_effs, srs, '^-', label='SRM bound')
    axes[1, 0].axvline(best_d, color='r', ls='--', alpha=0.5, label=f'Best d={best_d}')
    axes[1, 0].set_xlabel("Number of features")
    axes[1, 0].set_ylabel("Error / Bound")
    axes[1, 0].set_title("Structural Risk Minimization")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Train vs test error with increasing features
    test_errs = []
    for d in range(1, 11):
        model = LogisticRegression(max_iter=200).fit(X_tr[:, :d], y_tr)
        te = np.mean(model.predict(X_te[:, :d]) != y_te)
        test_errs.append(te)
    axes[1, 1].plot(range(1, 11), test_errs, 'o-')
    axes[1, 1].axhline(train_err, color='r', ls='--', label='Train error (all features)')
    axes[1, 1].set_xlabel("Number of features")
    axes[1, 1].set_ylabel("Test error")
    axes[1, 1].set_title("Test Error vs Dimensionality")
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("../../assets/phase05/45-learning-theory.png")
    plt.close()
    print("\nFigure saved to 45-learning-theory.png")

    # Delta sensitivity
    print("\n=== Sensitivity to δ ===")
    for delta in [0.01, 0.05, 0.1, 0.2]:
        eps_d = pac_bound_hoeffding(len(y_tr), X_tr.shape[1], delta)
        print(f"  δ={delta:.2f}: ε={eps_d:.4f}, bound={train_err + eps_d:.4f}")

    # Edge case: very small sample
    print("\n=== Edge Cases ===")
    X_small, y_small = make_classification(n_samples=20, n_features=3, n_informative=2, n_redundant=0, random_state=42)
    eps_small = pac_bound_hoeffding(len(y_small), X_small.shape[1])
    print(f"  n=20, d=3: PAC bound ε={eps_small:.4f}")

    # Edge case: delta close to 1
    eps_loose = pac_bound_hoeffding(len(y_tr), X_tr.shape[1], delta=0.5)
    print(f"  δ=0.5: ε={eps_loose:.4f}")
