"""Indexing and selection — loc, iloc, boolean masks."""
import pandas as pd
import numpy as np


print("=== Indexing & Selection ===")

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "age": [25, 30, 35, 28, 40],
    "city": ["NYC", "SF", "LA", "NYC", "SF"],
    "salary": [70000, 120000, 90000, 85000, 110000],
})
print(f"DataFrame:\n{df}")

print(f"\nColumn selection:")
print(f"  df['name']: {df['name'].tolist()}")
print(f"  df[['name', 'age']]:\n{df[['name', 'age']]}")

print(f"\nRow selection (iloc):")
print(f"  df.iloc[0]: {df.iloc[0].to_dict()}")
print(f"  df.iloc[1:3]:\n{df.iloc[1:3]}")

print(f"\nRow selection (loc):")
print(f"  df.loc[0]: {df.loc[0].to_dict()}")
print(f"  df.loc[0:2]:\n{df.loc[0:2]}")

print(f"\nMixed selection:")
print(f"  df.loc[0:2, ['name', 'age']]:\n{df.loc[0:2, ['name', 'age']]}")
print(f"  df.iloc[0:3, 0:2]:\n{df.iloc[0:3, 0:2]}")

print(f"\nBoolean filtering:")
print(f"  Age > 30:\n{df[df['age'] > 30]}")
print(f"  Age > 25 and NYC:\n{df[(df['age'] > 25) & (df['city'] == 'NYC')]}")

print(f"\nisin:")
print(f"  City in [NYC, SF]:\n{df[df['city'].isin(['NYC', 'SF'])]}")

print(f"\nQuery:")
print(f"  df.query('age > 30 & salary > 100000'):\n{df.query('age > 30 & salary > 100000')}")
