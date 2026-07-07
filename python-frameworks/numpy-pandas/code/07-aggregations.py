"""Aggregations — sum, mean, std, axis, nan-safe."""
import numpy as np


print("=== Aggregations ===")

arr = np.array([1, 2, 3, 4, 5])
print(f"arr = {arr}")
print(f"sum = {np.sum(arr)}")
print(f"mean = {np.mean(arr)}")
print(f"min = {np.min(arr)}")
print(f"max = {np.max(arr)}")
print(f"std = {np.std(arr):.4f}")
print(f"var = {np.var(arr):.4f}")

print(f"\nAxis parameter:")
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print(f"2D array:\n{arr2d}")
print(f"sum(axis=0): {arr2d.sum(axis=0)}")
print(f"sum(axis=1): {arr2d.sum(axis=1)}")
print(f"mean(axis=0): {arr2d.mean(axis=0)}")
print(f"mean(axis=1): {arr2d.mean(axis=1)}")

print(f"\nCumulative:")
arr = np.array([1, 2, 3, 4])
print(f"cumsum: {np.cumsum(arr)}")
print(f"cumprod: {np.cumprod(arr)}")

print(f"\nNan-safe:")
arr_nan = np.array([1, 2, np.nan, 4, np.nan])
print(f"arr with NaN: {arr_nan}")
print(f"nanmean: {np.nanmean(arr_nan)}")
print(f"nansum:  {np.nansum(arr_nan)}")
print(f"nanmin:  {np.nanmin(arr_nan)}")

print(f"\nPercentile:")
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(f"25th pct: {np.percentile(data, 25)}")
print(f"50th pct: {np.percentile(data, 50)}")
print(f"75th pct: {np.percentile(data, 75)}")
