# 📦 Large Datasets
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** Memory optimization, chunking, dtypes for large data, out-of-core.

## Memory Usage

```python
df.info(memory_usage="deep")          # Actual memory
df.memory_usage(deep=True) / 1024**2  # MB per column
```

## Optimize Dtypes

```python
def optimize_dtypes(df):
    for col in df.select_dtypes(include="float"):
        df[col] = pd.to_numeric(df[col], downcast="float")
    for col in df.select_dtypes(include="integer"):
        df[col] = pd.to_numeric(df[col], downcast="integer")
    for col in df.select_dtypes(include="object"):
        if df[col].nunique() / len(df) < 0.5:
            df[col] = df[col].astype("category")
    return df
```

## Sampling

```python
# Work with a sample first
sample = df.sample(frac=0.1, random_state=42)
```

## Filter Before Load

```python
cols = ["id", "name", "value"]
dtypes = {"id": "int32", "value": "float32"}
df = pd.read_csv("large.csv", usecols=cols, dtype=dtypes)
```

<!-- 🤔 Downcast floats to float32 and ints to int32 for ~50% memory savings. -->

## Run the Code

```bash
python code/29-large-datasets.py
```
