"""Linear regression — fit, predict, evaluate."""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


print("=== Linear Regression ===\n")

rng = np.random.default_rng(42)
n = 200
X = rng.normal(0, 1, (n, 3))
true_coef = np.array([3.5, -2.0, 1.2])
y = X @ true_coef + rng.normal(0, 0.5, n)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

print(f"Coefficients: {model.coef_}")
print(f"True coefs:   {true_coef}")
print(f"Intercept: {model.intercept_:.4f}")

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"\nMSE: {mse:.4f}")
print(f"R² Score: {r2:.4f}")

residuals = y_test - y_pred
print(f"Residual mean: {residuals.mean():.4f} (should be ~0)")
print(f"Residual std:  {residuals.std():.4f}")

rng2 = np.random.default_rng(99)
X_poly = rng2.normal(0, 1, (n, 1))
y_poly = 2 + 3 * X_poly.squeeze() - 0.5 * X_poly.squeeze()**2 + rng2.normal(0, 0.5, n)

from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly_aug = poly.fit_transform(X_poly)
model_poly = LinearRegression()
model_poly.fit(X_poly_aug, y_poly)
print(f"\nPolynomial coefs (linear, squared): {model_poly.coef_}")
print(f"Intercept: {model_poly.intercept_:.4f}")
