"""Polynomial regression — degree selection, overfitting demo."""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import r2_score, mean_squared_error


print("=== Polynomial Regression ===\n")

rng = np.random.default_rng(42)
X = rng.uniform(-3, 3, 200).reshape(-1, 1)
y = 0.5 * X.squeeze()**2 + X.squeeze() + rng.normal(0, 1, 200)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Degree selection (CV R²):")
for degree in [1, 2, 3, 5, 10, 15]:
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_poly = poly.fit_transform(X_train)
    model = LinearRegression()
    scores = cross_val_score(model, X_poly, y_train, cv=5, scoring='r2')
    print(f"  degree={degree:2d}: CV R²={scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

best_deg = 2
poly = PolynomialFeatures(degree=best_deg, include_bias=False)
X_poly_train = poly.fit_transform(X_train)
X_poly_test = poly.transform(X_test)
model = LinearRegression()
model.fit(X_poly_train, y_train)

y_pred = model.predict(X_poly_test)
print(f"\nBest model (degree={best_deg}):")
print(f"  Test R²:  {r2_score(y_test, y_pred):.4f}")
print(f"  Test RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")

print(f"\nInteraction features:")
X2 = rng.normal(0, 1, (100, 3))
poly_interact = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
X_interact = poly_interact.fit_transform(X2)
print(f"  Original features: {X2.shape[1]}")
print(f"  Interaction features: {X_interact.shape[1]}")
print(f"  Feature names: {poly_interact.get_feature_names_out()}")
