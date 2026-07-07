"""Array manipulation — reshape, concat, split, stacking."""
import numpy as np


print("=== Array Manipulation ===")

arr = np.arange(12)
print(f"Original: {arr}")
print(f"Reshape (3,4):\n{arr.reshape(3, 4)}")
print(f"Reshape (2,2,3):\n{arr.reshape(2, 2, 3)}")
print(f"Reshape (-1, 4):\n{arr.reshape(-1, 4)}")

print(f"\nConcatenation:")
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])
print(f"A:\n{a}")
print(f"B:\n{b}")
print(f"vstack:\n{np.vstack([a, b])}")
print(f"hstack:\n{np.hstack([a, b.T])}")

print(f"\nSplitting:")
arr = np.arange(10)
print(f"arr: {arr}")
parts = np.split(arr, [3, 7])
for i, p in enumerate(parts):
    print(f"  Part {i}: {p}")

print(f"\nAdding/removing axes:")
arr = np.array([1, 2, 3])
print(f"arr: {arr}, shape={arr.shape}")
print(f"newaxis:\n{arr[:, np.newaxis]}, shape={arr[:, np.newaxis].shape}")
print(f"expand_dims:\n{np.expand_dims(arr, 1)}, shape={np.expand_dims(arr, 1).shape}")

arr_2d = np.array([[1, 2, 3]])
print(f"\nSqueeze: {np.squeeze(arr_2d)}, shape={np.squeeze(arr_2d).shape}")

print(f"\nRepeat & tile:")
arr = np.array([1, 2, 3])
print(f"repeat(2): {np.repeat(arr, 2)}")
print(f"tile(2):   {np.tile(arr, 2)}")
