"""Array operations — vectorized arithmetic, ufuncs."""
import numpy as np


print("=== Array Operations ===")

a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

print(f"a = {a}")
print(f"b = {b}")
print(f"a + b  = {a + b}")
print(f"a * b  = {a * b}")
print(f"a ** 2 = {a ** 2}")
print(f"a > 2  = {a > 2}")
print(f"a @ b  = {a @ b}")

print(f"\nUniversal functions:")
print(f"sqrt(a): {np.sqrt(a)}")
print(f"exp(a):  {np.exp(a)}")
print(f"log(a):  {np.log(a)}")
print(f"sin(a):  {np.sin(a)}")

print(f"\nScalar broadcasting:")
print(f"a + 10: {a + 10}")
print(f"a * 2:  {a * 2}")

print(f"\nClip:")
arr = np.array([1, 2, 3, 4, 5, 6])
print(f"Clip(2, 5): {np.clip(arr, 2, 5)}")

print(f"\nWhere:")
arr = np.array([10, -1, 20, -2, 30])
print(f"Where positive: {np.where(arr > 0, arr, 0)}")
