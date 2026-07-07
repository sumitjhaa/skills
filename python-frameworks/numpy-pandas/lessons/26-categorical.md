# 🏷️ Categorical Data
<!-- ⏱️ 10 min | 🟡 Intermediate -->

**What You'll Learn:** Categorical dtype, memory savings, category operations.

## Creating Categories

```python
df["category"] = df["category"].astype("category")
df["size"] = pd.Categorical(df["size"], categories=["S", "M", "L", "XL"], ordered=True)
```

## Benefits

```python
# Memory: categories use less memory than object dtype
print(f"Memory: {df.memory_usage(deep=True)}")

# Ordered: supports comparison
df[df["size"] > "M"]
```

## Category Operations

```python
df["size"].cat.codes        # Integer codes
df["size"].cat.categories   # Category labels
df["size"].cat.add_categories(["XXL"])  # Add new category
df["size"].cat.remove_unused_categories()
```

## Renaming Categories

```python
df["size"] = df["size"].cat.rename_categories({
    "S": "Small", "M": "Medium", "L": "Large"
})
```

<!-- 🤔 Use `astype('category')` for string columns with few unique values — saves memory and speeds up groupby. -->

## Run the Code

```bash
python code/26-categorical.py
```
