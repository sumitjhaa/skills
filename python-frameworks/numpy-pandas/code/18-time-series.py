"""Time series — datetime, resampling, rolling windows."""
import pandas as pd
import numpy as np


print("=== Time Series ===")

rng = np.random.default_rng(42)
dates = pd.date_range("2025-01-01", periods=365, freq="D")
values = rng.normal(100, 10, 365) + np.sin(np.arange(365) * 2 * np.pi / 365) * 20
df = pd.DataFrame({"date": dates, "value": values})
df.set_index("date", inplace=True)
print(f"Data (first 5):\n{df.head()}")

print(f"\nMonthly mean:")
monthly = df.resample("ME").mean()
print(monthly.head())

print(f"\nWeekly sum:")
weekly = df.resample("W").sum()
print(weekly.head())

print(f"\nDaily access:")
print(f"  Year: {df.index.year[:5].tolist()}")
print(f"  Month: {df.index.month[:5].tolist()}")
print(f"  Day of week: {df.index.dayofweek[:5].tolist()}")

print(f"\nShifting:")
df["prev_day"] = df["value"].shift(1)
df["daily_change"] = df["value"].diff()
df["pct_change"] = df["value"].pct_change()
print(df.head())

print(f"\nRolling (7-day mean):")
df["rolling_7"] = df["value"].rolling(7).mean()
print(f"  First 10 rows:\n{df[['value', 'rolling_7']].head(10)}")

print(f"\nExpanding mean:")
df["expanding_mean"] = df["value"].expanding().mean()
print(f"  First {df.index[0].date()} -> {df.index[-1].date()}")
print(f"  Final expanding mean: {df['expanding_mean'].iloc[-1]:.2f}")
print(f"  Overall mean: {df['value'].mean():.2f}")
