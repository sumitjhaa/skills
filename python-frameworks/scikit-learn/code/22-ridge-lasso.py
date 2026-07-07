"""Ridge & Lasso — regularization, alpha tuning, L1 feature selection."""
import numpy as np
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.datasets import make_regression


print("=== Ridge & Lasso ===\n")

X, y = make_regression(n_samples=300, n_features=20, n_informative=5,
                        noise=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Alpha tuning:")
for alpha in [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]:
    ridge = Ridge(alpha=alpha)
    ridge.fit(X_train, y_train)
    train_r2 = r2_score(y_train, ridge.predict(X_train))
    test_r2 = r2_score(y_test, ridge.predict(X_test))
    print(f"  alpha={alpha:7.3f}: train_R²={train_r2:.4f}, test_R²={test_r2:.4f}")

print(f"\nLasso (feature selection):")
for alpha in [0.1, 1.0, 10.0]:
    lasso = Lasso(alpha=alpha, max_iter=5000)
    lasso.fit(X_train, y_train)
    n_zero = np.sum(np.abs(lasso.coef_) < 1e-10)
    test_r2 = r2_score(y_test, lasso.predict(X_test))
    print(f"  alpha={alpha:5.1f}: {n_zero} zero coefs, test_R²={test_r2:.4f}")

print(f"\nElasticNet:")
en = ElasticNet(alpha=1.0, l1_ratio=0.5, max_iter=5000)
en.fit(X_train, y_train)
print(f"  Test R²: {r2_score(y_test, en.predict(X_test)):.4f}")
print(f"  Zero coefs: {np.sum(np.abs(en.coef_) < 1e-10)}")

print(f"\nRidge coefficients (alpha=1):")
ridge_best = Ridge(alpha=1.0)
ridge_best.fit(X_train, y_train)
print(f"  Non-zero: {np.sum(np.abs(ridge_best.coef_) > 1e-10)} / {len(ridge_best.coef_)}")
