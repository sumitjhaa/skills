# 🏗️ Series & DataFrames
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Create Series and DataFrames, basic attributes, indexing.

## Series

```python
import pandas as pd

s = pd.Series([10, 20, 30, 40], index=["a", "b", "c", "d"])
s["a"]   # 10
s.values # array([10, 20, 30, 40])
s.index  # Index(['a', 'b', 'c', 'd'])
```

## DataFrame from Dict

```python
data = {
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["NYC", "SF", "LA"],
}
df = pd.DataFrame(data)
```

## DataFrame from List of Dicts

```python
data = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
]
df = pd.DataFrame(data)
```

## Basic Attributes

```python
df.shape      # (rows, cols)
df.columns    # Column labels
df.dtypes     # Column dtypes
df.index      # Row labels
df.head()     # First 5 rows
df.tail(3)    # Last 3 rows
df.info()     # Summary
df.describe() # Statistical summary
```

<!-- 🤔 Pandas is built on NumPy. Each column has a single dtype. -->

## Run the Code

```bash
python code/11-series-dataframe.py
```
