# ⚡ Performance
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** Vectorization, eval, query, chunking, parallel apply.

## Use Vectorized Ops

```python
# Slow
df["new"] = df.apply(lambda row: row["a"] + row["b"], axis=1)

# Fast
df["new"] = df["a"] + df["b"]
```

## eval for Expressions

```python
# Instead of:
df[(df["a"] > 0) & (df["b"] < 0)]

# Use:
df.query("a > 0 & b < 0")
```

## pd.eval

```python
result = pd.eval("df.a + df.b - df.c")
```

## Chunking Large Files

```python
chunks = pd.read_csv("large.csv", chunksize=10000)
results = []
for chunk in chunks:
    results.append(chunk["value"].mean())
```

## Select Dtypes

```python
# Only process numeric columns
numeric = df.select_dtypes(include="number")
numeric.mean()
```

<!-- 🤔 `df.query()` and `pd.eval()` use numexpr under the hood for fast evaluation. -->

## Run the Code

```bash
python code/28-performance.py
```
