"""Large datasets — memory optimization, downcasting, chunking."""
import pandas as pd
import numpy as np


print("=== Large Datasets ===")

rng = np.random.default_rng(42)
n = 100_000
df = pd.DataFrame({
    "id": range(n),
    "category": rng.choice(["Electronics", "Clothing", "Food", "Books"], n),
    "price": rng.normal(50, 20, n).round(2),
    "quantity": rng.integers(1, 100, n),
    "rating": rng.uniform(1, 5, n).round(1),
})

print(f"Original memory:")
mem_before = df.memory_usage(deep=True).sum() / 1024**2
print(f"  Total: {mem_before:.2f} MB")
print(f"  Per column:\n{df.memory_usage(deep=True) / 1024**2}")

print(f"\nOptimizing dtypes...")
df_opt = df.copy()
for col in df_opt.select_dtypes(include="float").columns:
    df_opt[col] = pd.to_numeric(df_opt[col], downcast="float")
for col in df_opt.select_dtypes(include="integer").columns:
    df_opt[col] = pd.to_numeric(df_opt[col], downcast="integer")
for col in df_opt.select_dtypes(include="object").columns:
    nunique = df_opt[col].nunique()
    if nunique / len(df_opt) < 0.5:
        df_opt[col] = df_opt[col].astype("category")

mem_after = df_opt.memory_usage(deep=True).sum() / 1024**2
print(f"  Total: {mem_after:.2f} MB")
print(f"  Saved: {(1 - mem_after / mem_before) * 100:.1f}%")
print(f"  Dtypes:\n{df_opt.dtypes}")

print(f"\nColumn types after optimization:")
print(f"  {df_opt.dtypes.value_counts()}")

print(f"\nSampling (10%):")
sample = df.sample(frac=0.1, random_state=42)
print(f"  Full: {len(df):,} rows, Sample: {len(sample):,} rows")

print(f"\nChunked processing (simulated):")
chunk_size = 20_000
total = 0
for start in range(0, n, chunk_size):
    chunk = df.iloc[start:start + chunk_size]
    total += chunk["price"].sum()
print(f"  Processed {n:,} rows in {n // chunk_size} chunks")
print(f"  Total price: ${total:,.2f}")
