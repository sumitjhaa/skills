"""Integration: exploratory data analysis pipeline."""
import pandas as pd
import numpy as np


print("=== EDA Pipeline ===\n")

rng = np.random.default_rng(42)
n = 500
df = pd.DataFrame({
    "customer_id": range(1, n + 1),
    "age": rng.integers(18, 75, n),
    "income": rng.normal(60000, 20000, n).round(-2),
    "spending": rng.exponential(500, n).round(2),
    "tenure": rng.integers(1, 60, n),
    "region": rng.choice(["North", "South", "East", "West"], n),
    "segment": rng.choice(["Basic", "Premium", "Enterprise"], n, p=[0.5, 0.3, 0.2]),
})
df.loc[rng.choice(n, 20), "income"] = np.nan
df.loc[rng.choice(n, 15), "spending"] = np.nan

print("1. Initial inspection:")
print(f"  Shape: {df.shape}")
print(f"  Dtypes:\n{df.dtypes.value_counts()}")
print(f"  Missing:\n{df.isna().sum()}")

print("\n2. Summary statistics:")
print(f"  Numeric:\n{df.describe()}")
print(f"  Categorical:\n{df.select_dtypes(include='object').nunique()}")

print("\n3. Cleaning:")
df_clean = df.copy()
df_clean["income"].fillna(df_clean["income"].median(), inplace=True)
df_clean["spending"].fillna(0, inplace=True)
print(f"  Missing after fill: {df_clean.isna().sum().sum()}")

print("\n4. Region & segment analysis:")
grouped = df_clean.groupby(["region", "segment"]).agg(
    avg_income=("income", "mean"),
    avg_spending=("spending", "mean"),
    avg_tenure=("tenure", "mean"),
    count=("customer_id", "count"),
).round(2)
print(f"{grouped}")

print("\n5. Correlation (numeric):")
numeric = df_clean.select_dtypes(include=["number"])
corr = numeric.corr()
print(f"{corr}")

print("\n6. Spending segments:")
df_clean["spending_tier"] = pd.qcut(df_clean["spending"], q=3, labels=["Low", "Mid", "High"])
print(f"  Spending tier distribution:\n{df_clean['spending_tier'].value_counts()}")

print("\n7. Income outliers (Z-score > 3):")
z = np.abs((df_clean["income"] - df_clean["income"].mean()) / df_clean["income"].std())
outliers = z > 3
print(f"  Outliers: {outliers.sum()} rows")

print("\n8. Top 5 customers by spending:")
top5 = df_clean.nlargest(5, "spending")[["customer_id", "spending", "region", "segment"]]
print(f"{top5}")
