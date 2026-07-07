"""Categorical data — memory savings, ordered categories, operations."""
import pandas as pd
import numpy as np


print("=== Categorical Data ===")

rng = np.random.default_rng(42)
n = 1000
df = pd.DataFrame({
    "id": range(n),
    "city": rng.choice(["NYC", "SF", "LA", "CHI", "SEA"], n),
    "size": rng.choice(["S", "M", "L", "XL"], n, p=[0.3, 0.4, 0.2, 0.1]),
    "value": rng.normal(100, 20, n),
})

object_mem = df.memory_usage(deep=True)
print(f"Memory (object):")
print(f"  city: {object_mem['city'] / 1024:.1f} KB")
print(f"  size: {object_mem['size'] / 1024:.1f} KB")

df["city"] = df["city"].astype("category")
df["size"] = pd.Categorical(df["size"], categories=["S", "M", "L", "XL"], ordered=True)

cat_mem = df.memory_usage(deep=True)
print(f"\nMemory (category):")
print(f"  city: {cat_mem['city'] / 1024:.1f} KB (saved {object_mem['city'] / 1024 - cat_mem['city'] / 1024:.1f} KB)")
print(f"  size: {cat_mem['size'] / 1024:.1f} KB")

print(f"\nOrdered category comparison:")
print(f"  Categories: {list(df['size'].cat.categories)}")
print(f"  S < L:      {(df['size'] > 'M').sum()} values > M")

print(f"\nCategory codes:")
print(f"  First 5 codes: {df['size'].cat.codes[:5].tolist()}")

print(f"\nRename categories:")
df["size"] = df["size"].cat.rename_categories({
    "S": "Small", "M": "Medium", "L": "Large", "XL": "X-Large"
})
print(f"  {df['size'].value_counts()}")

print(f"\nGroupBy with categories (faster):")
print(f"  Mean value by size:\n{df.groupby('size', observed=True)['value'].mean()}")
