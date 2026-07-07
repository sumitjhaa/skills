"""NumPy arrays — creation, shapes, dtypes."""
import numpy as np


print("=== NumPy Arrays ===")

arr = np.array([1, 2, 3, 4, 5])
print(f"From list: {arr}")

zeros = np.zeros((2, 3))
print(f"Zeros (2x3):\n{zeros}")

ones = np.ones((2, 3))
print(f"Ones (2x3):\n{ones}")

eye = np.eye(3)
print(f"Identity:\n{eye}")

r = np.arange(0, 10, 2)
print(f"Arange (0, 10, 2): {r}")

s = np.linspace(0, 1, 5)
print(f"Linspace (0-1, 5): {s}")

arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print(f"\n2D array:\n{arr2d}")
print(f"Shape: {arr2d.shape}, ndim: {arr2d.ndim}, size: {arr2d.size}")

arr_f32 = np.array([1, 2, 3], dtype=np.float32)
print(f"\nFloat32: {arr_f32}, dtype: {arr_f32.dtype}")

arr_bool = np.array([True, False, True])
print(f"Bool: {arr_bool}, dtype: {arr_bool.dtype}")
