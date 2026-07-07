"""Integration: data processing pipeline with NumPy."""
import numpy as np


print("=== Data Pipeline ===\n")

rng = np.random.default_rng(42)
n = 200

feature_1 = rng.normal(50, 10, n)
feature_2 = rng.exponential(20, n)
feature_3 = rng.uniform(0, 1, n)
categories = rng.integers(0, 4, n)

data = np.column_stack([feature_1, feature_2, feature_3, categories])
print(f"Generated {n} rows, 4 columns")
print(f"Shape: {data.shape}")

print("\nBasic stats:")
print(f"  mean:  {data[:, :3].mean(axis=0)}")
print(f"  std:   {data[:, :3].std(axis=0)}")
print(f"  min:   {data[:, :3].min(axis=0)}")
print(f"  max:   {data[:, :3].max(axis=0)}")

z_scores = np.abs((data[:, :3] - data[:, :3].mean(axis=0)) / data[:, :3].std(axis=0))
valid_rows = (z_scores < 3).all(axis=1)
clean = data[valid_rows]
print(f"\nOutliers removed: {n - len(clean)} rows")
print(f"Clean shape: {clean.shape}")

min_vals = clean[:, :3].min(axis=0)
max_vals = clean[:, :3].max(axis=0)
normalized = (clean[:, :3] - min_vals) / (max_vals - min_vals)
normalized_data = np.column_stack([normalized, clean[:, 3]])
print(f"\nNormalized range: [{normalized.min():.3f}, {normalized.max():.3f}]")

print("\nPer-category stats:")
for cat in range(4):
    mask = normalized_data[:, 3] == cat
    subset = normalized_data[mask]
    print(f"  Category {cat}: n={len(subset):3d}, "
          f"f1={subset[:, 0].mean():.3f}, "
          f"f2={subset[:, 1].mean():.3f}, "
          f"f3={subset[:, 2].mean():.3f}")

corr = np.corrcoef(normalized.T)
print(f"\nCorrelation matrix (features 0-2):")
print(f"  {corr[0, 1]:.3f} {corr[0, 2]:.3f}")
print(f"  {corr[1, 0]:.3f} {corr[1, 2]:.3f}")
print(f"  {corr[2, 0]:.3f} {corr[2, 1]:.3f}")
