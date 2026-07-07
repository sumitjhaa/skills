"""Random numbers — generators, distributions, shuffling."""
import numpy as np


print("=== Random Numbers ===")

rng = np.random.default_rng(42)

u = rng.random(5)
print(f"Uniform [0,1): {u}")

ints = rng.integers(0, 10, 5)
print(f"Integers 0-9: {ints}")

normal = rng.normal(0, 1, 5)
print(f"Normal(0,1): {normal}")

print(f"\nDistributions:")
print(f"Uniform(0,10):   {rng.uniform(0, 10, 5)}")
print(f"Binomial(10,.5): {rng.binomial(10, 0.5, 5)}")
print(f"Poisson(3):      {rng.poisson(3, 5)}")
print(f"Exponential(1):  {rng.exponential(1, 5)}")

print(f"\nShuffle:")
arr = np.arange(10)
print(f"Before: {arr}")
rng.shuffle(arr)
print(f"After:  {arr}")

print(f"\nChoice:")
print(f"Sample 3: {rng.choice(np.arange(10), 3)}")
print(f"Without replacement: {rng.choice(np.arange(10), 5, replace=False)}")

print(f"\nReproducibility:")
rng1 = np.random.default_rng(42)
rng2 = np.random.default_rng(42)
print(f"rng1: {rng1.random(3)}")
print(f"rng2: {rng2.random(3)}")
