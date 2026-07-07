"""Indexing, slicing, fancy indexing, boolean masks."""
import numpy as np


print("=== Indexing & Slicing ===")

arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(f"Array:\n{arr}")
print(f"arr[0]:     {arr[0]}")
print(f"arr[0, 1]:  {arr[0, 1]}")
print(f"arr[-1]:    {arr[-1]}")

print(f"\nSlicing:")
print(f"arr[:, 0]:    {arr[:, 0]}")
print(f"arr[0, :2]:   {arr[0, :2]}")
print(f"arr[:2, :2]:\n{arr[:2, :2]}")
print(f"arr[::2, ::2]:\n{arr[::2, ::2]}")

print(f"\nFancy indexing:")
arr1d = np.array([10, 20, 30, 40, 50])
print(f"arr1d = {arr1d}")
print(f"arr1d[[0, 2, 4]]: {arr1d[[0, 2, 4]]}")

rows = np.array([0, 1, 2])
cols = np.array([2, 1, 0])
print(f"arr[rows, cols]: {arr[rows, cols]}")

print(f"\nBoolean masks:")
arr = np.array([1, 2, 3, 4, 5, 6])
print(f"arr = {arr}")
print(f"arr > 3:        {arr > 3}")
print(f"arr[arr > 3]:   {arr[arr > 3]}")
print(f"arr[arr % 2 == 0]: {arr[arr % 2 == 0]}")
