"""Integration: end-to-end customer analytics project."""
import pandas as pd
import numpy as np


print("=" * 60)
print("  CUSTOMER ANALYTICS — Full Analysis Pipeline")
print("=" * 60, "\n")

rng = np.random.default_rng(42)
n_customers = 2000
n_transactions = 20000

print("1. Generating synthetic data...")
customers = pd.DataFrame({
    "customer_id": range(1, n_customers + 1),
    "age": rng.integers(18, 75, n_customers),
    "income": rng.normal(60000, 25000, n_customers).round(-2),
    "region": rng.choice(["North", "South", "East", "West"], n_customers),
    "signup_date": pd.date_range("2023-01-01", periods=n_customers, freq="h")[
        rng.choice(n_customers, n_customers, replace=False)
    ],
})

transactions = pd.DataFrame({
    "transaction_id": range(1, n_transactions + 1),
    "customer_id": rng.choice(customers["customer_id"], n_transactions),
    "amount": rng.exponential(100, n_transactions).round(2),
    "date": pd.date_range("2024-01-01", periods=n_transactions, freq="h")[
        rng.choice(n_transactions, n_transactions, replace=False)
    ],
    "category": rng.choice(["Electronics", "Clothing", "Food", "Travel"], n_transactions),
})
print(f"  Customers: {len(customers):,}")
print(f"  Transactions: {len(transactions):,}")

print("\n2. Cleaning...")
customers.loc[rng.choice(n_customers, 50, replace=False), "income"] = np.nan
customers["income"].fillna(customers["income"].median(), inplace=True)
transactions.dropna(inplace=True)

print(f"  Missing: {customers.isna().sum().sum()} remaining")

print("\n3. Customer metrics (RFM-style):")
tx_summary = transactions.groupby("customer_id").agg(
    recency=("date", "max"),
    frequency=("transaction_id", "count"),
    monetary=("amount", "sum"),
    avg_amount=("amount", "mean"),
).reset_index()

tx_summary["recency_days"] = (
    pd.Timestamp("2025-01-01") - tx_summary["recency"]
).dt.days

customers_full = customers.merge(tx_summary, on="customer_id", how="left").fillna(0)
print(f"  Metrics computed for {len(customers_full):,} customers")

print("\n4. Segmentation:")
customers_full["spending_tier"] = pd.qcut(
    customers_full["monetary"], q=4,
    labels=["Low", "Medium-Low", "Medium-High", "High"]
)

segment_profiles = pd.pivot_table(
    customers_full,
    values=["age", "income", "monetary", "frequency", "avg_amount"],
    index="spending_tier",
    aggfunc="mean",
).round(2)
print(f"Segment profiles:\n{segment_profiles}")

print("\n5. Regional analysis:")
regional = pd.pivot_table(
    customers_full,
    values=["monetary", "frequency"],
    index="region",
    columns="spending_tier",
    aggfunc="mean",
).round(2)
print(f"{regional}")

print("\n6. Monthly trends:")
transactions["month"] = transactions["date"].dt.to_period("M")
monthly = transactions.groupby("month").agg(
    revenue=("amount", "sum"),
    transactions=("transaction_id", "count"),
    unique_customers=("customer_id", "nunique"),
)
print(f"  First 6 months:\n{monthly.head(6)}")

print("\n7. Top categories:")
cat_stats = pd.pivot_table(
    transactions,
    values="amount",
    index="category",
    aggfunc=["sum", "mean", "count"],
).round(2)
print(f"{cat_stats}")

print("\n8. Cross-segment comparisons:")
high_value = customers_full[customers_full["monetary"] > customers_full["monetary"].quantile(0.9)]
low_value = customers_full[customers_full["monetary"] < customers_full["monetary"].quantile(0.1)]
print(f"  High-value customers: {len(high_value)}")
print(f"  Avg income: ${high_value['income'].mean():,.0f}")
print(f"  Avg age: {high_value['age'].mean():.1f}")
print(f"\n  Low-value customers: {len(low_value)}")
print(f"  Avg income: ${low_value['income'].mean():,.0f}")
print(f"  Avg age: {low_value['age'].mean():.1f}")

print("\n" + "=" * 60)
print("  ANALYSIS COMPLETE")
print("=" * 60)
