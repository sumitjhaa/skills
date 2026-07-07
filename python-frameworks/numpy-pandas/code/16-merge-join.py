"""Merge and join — combining DataFrames."""
import pandas as pd
import numpy as np


print("=== Merge & Join ===")

users = pd.DataFrame({
    "user_id": [1, 2, 3, 4],
    "name": ["Alice", "Bob", "Charlie", "Diana"],
    "city": ["NYC", "SF", "LA", "NYC"],
})

orders = pd.DataFrame({
    "order_id": [101, 102, 103, 104, 105],
    "user_id": [1, 2, 1, 3, 99],
    "amount": [50.0, 30.0, 20.0, 100.0, 75.0],
    "date": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05"],
})

print(f"Users:\n{users}")
print(f"\nOrders:\n{orders}")

print(f"\nInner join:\n{pd.merge(users, orders, on='user_id')}")
print(f"\nLeft join:\n{pd.merge(users, orders, on='user_id', how='left')}")
print(f"\nRight join:\n{pd.merge(users, orders, on='user_id', how='right')}")
print(f"\nOuter join:\n{pd.merge(users, orders, on='user_id', how='outer')}")

print(f"\nMerge with indicator:")
result = pd.merge(users, orders, on="user_id", how="outer", indicator=True)
print(f"  Join keys:\n{result['_merge'].value_counts()}")

print(f"\nConcat rows:")
extra = pd.DataFrame({"user_id": [5, 6], "name": ["Eve", "Frank"], "city": ["SF", "LA"]})
combined = pd.concat([users, extra], ignore_index=True)
print(f"  {combined}")

print(f"\nConcat columns:")
bonus = pd.DataFrame({"bonus": [5000, 3000, 7000, 4000]})
combined_cols = pd.concat([users, bonus], axis=1)
print(f"  {combined_cols}")
