# 🏁 Integration: Data Pipeline
<!-- ⏱️ 20 min | 🔴 Advanced -->

**What You'll Learn:** Combine NumPy skills into a real data processing pipeline.

## Pipeline Steps

1. Generate synthetic data (random, with patterns)
2. Clean: remove outliers, handle missing values
3. Transform: normalize, feature engineering
4. Aggregate: compute statistics per group
5. Export: save processed data

## Generate Data

```python
rng = np.random.default_rng(42)
n = 1000
data = np.column_stack([
    rng.normal(50, 10, n),          # feature_1
    rng.exponential(20, n),         # feature_2
    rng.uniform(0, 1, n),           # feature_3
    rng.integers(0, 4, n),          # category
])
```

## Clean & Transform

```python
# Remove outliers (Z-score > 3)
z_scores = np.abs((data - data.mean(0)) / data.std(0))
clean = data[(z_scores < 3).all(axis=1)]

# Normalize (min-max)
min_vals = clean.min(0)
max_vals = clean.max(0)
normalized = (clean - min_vals) / (max_vals - min_vals)
```

## Aggregate

```python
# Mean per category
for cat in range(4):
    mask = normalized[:, 3] == cat
    print(f"Category {cat}: mean = {normalized[mask, :3].mean(0)}")
```

## Run the Code

```bash
python code/10-integration-data-pipeline.py
```
