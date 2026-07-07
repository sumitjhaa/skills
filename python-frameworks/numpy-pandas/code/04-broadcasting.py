"""Broadcasting — shape compatibility, newaxis, centering."""
import numpy as np


print("=== Broadcasting ===")

a = np.array([[1], [2], [3]])
b = np.array([10, 20, 30])
print(f"a (3x1):\n{a}")
print(f"b (3,):  {b}")
print(f"a + b:\n{a + b}")

ones = np.ones((3, 4))
row = np.array([1, 2, 3, 4])
print(f"\nOnes (3x4):\n{ones}")
print(f"Row (4,):  {row}")
print(f"Ones + row:\n{ones + row}")

print(f"\nAdding axis with newaxis:")
arr = np.array([1, 2, 3])
print(f"arr:            {arr}, shape: {arr.shape}")
print(f"arr[:, newaxis]:\n{arr[:, np.newaxis]}, shape: {arr[:, np.newaxis].shape}")
print(f"arr[newaxis, :]: {arr[np.newaxis, :]}, shape: {arr[np.newaxis, :].shape}")

print(f"\nCentering data:")
rng = np.random.default_rng(42)
data = rng.normal(10, 2, (5, 3))
print(f"Data:\n{data}")
mean = data.mean(axis=0)
print(f"Mean (axis=0): {mean}")
centered = data - mean
print(f"Centered:\n{centered}")
print(f"Centered mean (should be ~0): {centered.mean(axis=0)}")

print(f"\nOuter product via broadcasting:")
x = np.array([1, 2, 3])
y = np.array([10, 20, 30, 40])
print(f"x @ y^T:\n{x[:, np.newaxis] * y[np.newaxis, :]}")
