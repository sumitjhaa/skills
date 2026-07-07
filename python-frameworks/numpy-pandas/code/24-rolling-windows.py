"""Rolling windows — custom functions, expanding, EWMA."""
import pandas as pd
import numpy as np


print("=== Rolling Windows ===\n")

rng = np.random.default_rng(42)
dates = pd.date_range("2025-01-01", periods=200, freq="D")
df = pd.DataFrame({"date": dates, "value": rng.normal(100, 15, 200)})
df.set_index("date", inplace=True)

df["ma_7"] = df["value"].rolling(7).mean()
df["ma_30"] = df["value"].rolling(30).mean()

print(f"Rolling means (first 10):")
print(f"{df.head(10)}")

def rolling_cv(x):
    return x.std() / x.mean() if x.mean() != 0 else 0

df["cv_20"] = df["value"].rolling(20).apply(rolling_cv)
print(f"\nRolling CV (first 10):")
print(f"{df[['value', 'cv_20']].head(10)}")

print(f"\nExpanding:")
df["expanding_max"] = df["value"].expanding().max()
df["expanding_std"] = df["value"].expanding().std()
print(f"{df[['value', 'expanding_max', 'expanding_std']].head(10)}")

print(f"\nEWM (span=10):")
df["ewm_10"] = df["value"].ewm(span=10).mean()
print(f"{df[['value', 'ewm_10']].head(10)}")

print(f"\nMultiple windows comparison (last 10):")
cols = ["value", "ma_7", "ma_30", "ewm_10"]
print(f"{df[cols].tail(10).round(2)}")

print(f"\nRolling std (20-day):")
df["std_20"] = df["value"].rolling(20).std()
print(f"  Mean rolling std: {df['std_20'].mean():.2f}")
print(f"  Overall std:      {df['value'].std():.2f}")
