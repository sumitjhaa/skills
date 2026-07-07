"""Advanced GroupBy — custom agg, apply, multiple functions."""
import pandas as pd
import numpy as np


print("=== Advanced GroupBy ===")

rng = np.random.default_rng(42)
df = pd.DataFrame({
    "category": rng.choice(["Electronics", "Clothing", "Food", "Books"], 100),
    "subcategory": rng.choice(["Premium", "Standard", "Budget"], 100),
    "sales": rng.normal(1000, 300, 100).round(2),
    "profit": rng.normal(200, 100, 100).round(2),
    "rating": rng.uniform(1, 5, 100).round(1),
})

print(f"Data (first 5):\n{df.head()}")

def range_func(x):
    return x.max() - x.min()

print(f"\nMultiple aggregations:")
result = df.groupby("category")["sales"].agg(["sum", "mean", "std", range_func, lambda x: x.quantile(0.75)])
result.columns = ["total", "mean", "std", "range", "p75"]
print(f"{result}")

print(f"\nNamed aggregations:")
named = df.groupby("category").agg(
    total_sales=("sales", "sum"),
    avg_sales=("sales", "mean"),
    avg_profit=("profit", "mean"),
    avg_rating=("rating", "mean"),
    count=("sales", "count"),
).round(2)
print(f"{named}")

print(f"\nMultiple group keys:")
multi = df.groupby(["category", "subcategory"]).agg(
    total_sales=("sales", "sum"),
    avg_rating=("rating", "mean"),
).round(2)
print(f"{multi}")

print(f"\nApply (top 2 per category):")
top2 = df.groupby("category").apply(
    lambda g: g.nlargest(2, "sales")
).reset_index(level=1, drop=True).reset_index()
print(f"{top2[['category', 'sales']]}")
