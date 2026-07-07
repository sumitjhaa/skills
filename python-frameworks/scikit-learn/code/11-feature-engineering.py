"""Feature engineering — polynomial, interactions, binning."""
import numpy as np
from sklearn.preprocessing import PolynomialFeatures, KBinsDiscretizer


print("=== Feature Engineering ===\n")

rng = np.random.default_rng(42)
X = rng.normal(0, 1, (100, 2))

print("Original shape:", X.shape)

poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)
print(f"Polynomial (deg=2): {X_poly.shape[1]} features")
print(f"  Feature names: {poly.get_feature_names_out()}")

poly_interact = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
X_interact = poly_interact.fit_transform(X)
print(f"Interactions only: {X_interact.shape[1]} features")

kbd = KBinsDiscretizer(n_bins=4, encode='onehot-dense')
X_binned = kbd.fit_transform(X)
print(f"\nBinned shape: {X_binned.shape} (2 cols -> 8 one-hot cols)")

print(f"\nDate features (using pandas):")
import pandas as pd
dates = pd.date_range("2025-01-01", periods=10, freq="D")
df = pd.DataFrame({"date": dates})
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["day_of_week"] = df["date"].dt.dayofweek
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
print(df[["date", "year", "month", "day", "day_of_week", "is_weekend"]])
