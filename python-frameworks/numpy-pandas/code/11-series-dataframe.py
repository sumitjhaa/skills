"""Series and DataFrames — creation, attributes, basic operations."""
import pandas as pd
import numpy as np


print("=== Series & DataFrames ===")

s = pd.Series([10, 20, 30, 40], index=["a", "b", "c", "d"])
print(f"Series:\n{s}")
print(f"  s['a']: {s['a']}")
print(f"  values: {s.values}")
print(f"  index:  {list(s.index)}")

data = {
    "name": ["Alice", "Bob", "Charlie", "Diana"],
    "age": [25, 30, 35, 28],
    "city": ["NYC", "SF", "LA", "NYC"],
    "salary": [70000, 120000, 90000, 85000],
}
df = pd.DataFrame(data)
print(f"\nDataFrame:\n{df}")
print(f"\nShape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"Dtypes:\n{df.dtypes}")

print(f"\nHead (first 2):\n{df.head(2)}")
print(f"\nTail (last 2):\n{df.tail(2)}")
print(f"\nDescribe:\n{df.describe()}")

print(f"\nInfo:")
df.info()

print(f"\nNunique:\n{df.nunique()}")

print(f"\nSelecting columns:")
print(f"  Single col: {df['name'].tolist()}")
print(f"  Multi cols:\n{df[['name', 'age']]}")
