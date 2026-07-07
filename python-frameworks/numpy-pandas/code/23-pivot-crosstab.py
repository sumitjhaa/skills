"""Pivot tables and crosstab — Excel-style summaries."""
import pandas as pd
import numpy as np


print("=== Pivot Tables & Crosstab ===")

rng = np.random.default_rng(42)
df = pd.DataFrame({
    "region": rng.choice(["North", "South", "East", "West"], 200),
    "quarter": rng.choice(["Q1", "Q2", "Q3", "Q4"], 200),
    "segment": rng.choice(["Retail", "Wholesale", "Online"], 200),
    "sales": rng.normal(50000, 15000, 200).round(2),
    "profit": rng.normal(10000, 5000, 200).round(2),
})

print(f"Pivot table (sum sales by region × quarter):")
pivot = pd.pivot_table(
    df, values="sales", index="region", columns="quarter",
    aggfunc="sum", margins=True,
)
print(f"{pivot}")

print(f"\nMultiple values:")
multi = pd.pivot_table(
    df, values=["sales", "profit"], index="region",
    columns="quarter", aggfunc="mean",
).round(2)
print(f"{multi}")

print(f"\nCrosstab (frequency):")
ct = pd.crosstab(df["region"], df["segment"], margins=True)
print(f"{ct}")

print(f"\nCrosstab (row %):")
ct_pct = pd.crosstab(df["region"], df["segment"], normalize="index").round(3)
print(f"{ct_pct}")

print(f"\nPivot with segment as second index:")
pivot2 = pd.pivot_table(
    df, values="sales", index=["region", "segment"],
    columns="quarter", aggfunc="sum",
)
print(f"{pivot2}")
