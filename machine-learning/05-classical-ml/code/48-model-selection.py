"""Model Selection: AIC, BIC from scratch vs cross-validation with visualization."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

def aic(n, mse, k):
    return n * np.log(mse) + 2 * k

def bic(n, mse, k):
    return n * np.log(mse) + k * np.log(n)

def aicc(n, mse, k):
    return aic(n, mse, k) + 2 * k * (k + 1) / (n - k - 1)

if __name__ == "__main__":
    np.random.seed(42)
    print("=== Model Selection: AIC, BIC, AICc, CV ===\n")

    X, y = make_regression(n_samples=200, n_features=10, noise=0.5, random_state=42)

    results = []
    for d in range(1, 11):
        X_sub = X[:, :d]
        model = LinearRegression().fit(X_sub, y)
        pred = model.predict(X_sub)
        mse = np.mean((pred - y)**2)
        n = len(y)
        k = d + 1  # number of parameters (d features + intercept)
        aic_val = aic(n, mse, k)
        bic_val = bic(n, mse, k)
        aicc_val = aicc(n, mse, k) if n > k + 1 else float('inf')
        cv = cross_val_score(LinearRegression(), X_sub, y, cv=5,
                             scoring='neg_mean_squared_error').mean()
        results.append((d, mse, aic_val, bic_val, aicc_val, -cv))
        print(f"d={d:2d}  MSE={mse:.4f}  AIC={aic_val:.2f}  AICc={aicc_val:.2f}  "
              f"BIC={bic_val:.2f}  CV={-cv:.4f}")

    best_aic = min(results, key=lambda r: r[2])
    best_bic = min(results, key=lambda r: r[3])
    best_aicc = min(results, key=lambda r: r[4])
    best_cv = min(results, key=lambda r: r[5])
    print(f"\nBest AIC:  d={best_aic[0]}, value={best_aic[2]:.2f}")
    print(f"Best AICc: d={best_aicc[0]}, value={best_aicc[4]:.2f}")
    print(f"Best BIC:  d={best_bic[0]}, value={best_bic[3]:.2f}")
    print(f"Best CV:   d={best_cv[0]}, value={best_cv[5]:.4f}")

    # Different noise levels
    print("\n=== Noise Level Sensitivity ===")
    for noise in [0.1, 0.5, 1.0, 2.0]:
        X_n, y_n = make_regression(n_samples=200, n_features=10, noise=noise, random_state=42)
        best_d = 0
        best_score = float('inf')
        for d in range(1, 11):
            model = LinearRegression().fit(X_n[:, :d], y_n)
            mse = np.mean((model.predict(X_n[:, :d]) - y_n)**2)
            b = bic(len(y_n), mse, d + 1)
            if b < best_score:
                best_score = b
                best_d = d
        print(f"  noise={noise:.1f}: BIC selects d={best_d}")

    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ds = [r[0] for r in results]
    mses = [r[1] for r in results]
    aics = [r[2] for r in results]
    bics = [r[3] for r in results]
    aiccs = [r[4] for r in results]
    cvs = [r[5] for r in results]

    axes[0].plot(ds, mses, 'o-', label='MSE')
    axes[0].plot(ds, aics, 's-', label='AIC')
    axes[0].plot(ds, aiccs, 'D-', label='AICc')
    axes[0].plot(ds, bics, '^-', label='BIC')
    axes[0].set_xlabel("Number of features (d)")
    axes[0].set_ylabel("Criterion value")
    axes[0].set_title("Model Selection Criteria")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(ds, mses, 'o-', label='MSE (train)')
    axes[1].plot(ds, cvs, 's-', label='CV MSE (5-fold)')
    axes[1].set_xlabel("Number of features (d)")
    axes[1].set_ylabel("MSE")
    axes[1].set_title("Training MSE vs Cross-Validation MSE")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("../../assets/phase05/48-model-selection.png")
    plt.close()
    print("\nFigure saved to 48-model-selection.png")

    # Edge case: small sample
    print("\n=== Edge Cases ===")
    X_small, y_small = make_regression(n_samples=15, n_features=5, noise=0.5, random_state=42)
    for d in [1, 2, 3]:
        model = LinearRegression().fit(X_small[:, :d], y_small)
        mse = np.mean((model.predict(X_small[:, :d]) - y_small)**2)
        k = d + 1
        a = aic(15, mse, k)
        b = bic(15, mse, k)
        ac = aicc(15, mse, k) if 15 > k + 1 else float('inf')
        print(f"  n=15, d={d}: AIC={a:.2f}, AICc={ac:.2f}, BIC={b:.2f}")

    # Edge case: AICc vs AIC as n grows
    print("\n  AICc correction term vs sample size:")
    for n in [10, 20, 50, 100, 500]:
        corr = 2 * 3 * 4 / (n - 4) if n > 4 else float('inf')
        print(f"    n={n}: AICc correction={corr:.4f}")
