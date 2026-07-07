"""MultiIndex — hierarchical indexing, selection, stack/unstack."""
import pandas as pd
import numpy as np


print("=== MultiIndex ===")

arrays = [["A", "A", "B", "B", "C", "C"], [2023, 2024, 2023, 2024, 2023, 2024]]
index = pd.MultiIndex.from_arrays(arrays, names=["group", "year"])
df = pd.DataFrame({"value": [10, 20, 30, 40, 50, 60]}, index=index)
print(f"MultiIndex DataFrame:\n{df}")

print(f"\nSelect group A:")
print(f"{df.loc['A']}")

print(f"\nSelect (A, 2024):")
print(f"{df.loc[('A', 2024)]}")

print(f"\nCross-section year=2024:")
print(f"{df.xs(2024, level='year')}")

print(f"\nUnstack:")
print(f"{df.unstack()}")

print(f"\nStack:")
unstacked = df.unstack()
print(f"{unstacked.stack()}")

print(f"\nMultiIndex columns:")
rng = np.random.default_rng(42)
cols = pd.MultiIndex.from_tuples([
    ("sales", "Q1"), ("sales", "Q2"), ("costs", "Q1"), ("costs", "Q2")
])
df_multi = pd.DataFrame(rng.random((3, 4)), columns=cols)
df_multi.index = ["Store_A", "Store_B", "Store_C"]
print(f"{df_multi}")
print(f"\nSales columns:\n{df_multi['sales']}")
