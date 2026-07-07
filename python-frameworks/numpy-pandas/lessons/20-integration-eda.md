# 🏁 Integration: EDA Pipeline
<!-- ⏱️ 20 min | 🔴 Advanced -->

**What You'll Learn:** Complete exploratory data analysis with pandas.

## Pipeline Steps

1. Load data
2. Initial inspection (shape, types, summary)
3. Clean (missing values, outliers, types)
4. Explore (statistics, distributions, correlations)
5. Visualize (histograms, boxplots, scatter matrix)
6. Report (group summaries, insights)

## Initial Inspection

```python
df.info()
df.describe()
df.isna().sum()
df.nunique()
```

## Correlation Analysis

```python
numeric = df.select_dtypes(include=["number"])
corr = numeric.corr()
# Show high correlations
high_corr = corr[abs(corr) > 0.5].stack().index
```

## Outlier Detection

```python
def detect_outliers_zscore(df, threshold=3):
    z = np.abs((df - df.mean()) / df.std())
    return (z > threshold).any(axis=1)
```

## Group Aggregations

```python
df.groupby("category").agg({
    "price": ["mean", "std", "min", "max"],
    "rating": "mean",
    "name": "count",
})
```

## Run the Code

```bash
python code/20-integration-eda.py
```
