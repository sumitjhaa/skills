"""Missing data strategies — imputation, interpolation, pattern detection."""
import pandas as pd
import numpy as np


print("=== Missing Data Strategies ===\n")

rng = np.random.default_rng(42)
dates = pd.date_range("2025-01-01", periods=50, freq="D")
df = pd.DataFrame({
    "date": dates,
    "value": rng.normal(100, 15, 50).round(2),
    "income": rng.normal(60000, 10000, 50).round(-2),
    "region": rng.choice(["North", "South", "East", "West"], 50),
})

missing_idx = rng.choice(50, 10, replace=False)
df.loc[missing_idx, "value"] = np.nan
missing_idx2 = rng.choice(50, 8, replace=False)
df.loc[missing_idx2, "income"] = np.nan

print(f"1. Missing count:")
print(f"{df.isna().sum()}")

print(f"\n2. Forward/backward fill:")
df["value_ffill"] = df["value"].ffill()
df["value_bfill"] = df["value"].bfill()
print(f"  Forward fill (first 15):\n{df[['date', 'value', 'value_ffill']].head(15)}")

print(f"\n3. Linear interpolation:")
df["value_interp"] = df["value"].interpolate(method="linear")
print(f"  Interpolated (first 15):\n{df[['date', 'value', 'value_interp']].head(15)}")

print(f"\n4. Group-wise imputation:")
df["income_filled"] = df.groupby("region")["income"].transform(
    lambda x: x.fillna(x.median())
)
print(f"  Income filled by region median:")
print(f"  Missing before: {df['income'].isna().sum()}")
print(f"  Missing after:  {df['income_filled'].isna().sum()}")

print(f"\n5. Missing indicator:")
df["value_missing"] = df["value"].isna().astype(int)
print(f"  Indicator column mean: {df['value_missing'].mean():.2f}")

print(f"\n6. Pattern detection:")
missing_pattern = df[["value", "income"]].isna().value_counts()
print(f"  Missing patterns:\n{missing_pattern}")
