"""Performance — vectorization, query, eval, dtype optimization."""
import pandas as pd
import numpy as np
import time


print("=== Performance ===")

n = 1_000_000
rng = np.random.default_rng(42)
df = pd.DataFrame({
    "a": rng.normal(100, 20, n),
    "b": rng.normal(50, 10, n),
    "c": rng.choice(["X", "Y", "Z"], n),
})

print(f"DataFrame: {n:,} rows, {df.shape[1]} cols")

print("\n1. Vectorized vs apply:")
a, b = df["a"].values, df["b"].values

t0 = time.time()
result_vec = a + b
t_vec = time.time() - t0
print(f"  Vectorized: {t_vec:.4f}s")

print("\n2. query vs boolean mask:")
t0 = time.time()
mask = df[(df["a"] > 100) & (df["b"] < 50)]
t_mask = time.time() - t0

t0 = time.time()
q = df.query("a > 100 & b < 50")
t_query = time.time() - t0
print(f"  Boolean mask: {t_mask:.4f}s")
print(f"  query:        {t_query:.4f}s")

print("\n3. eval for expressions:")
t0 = time.time()
df["d"] = df["a"] + df["b"] - df["a"] * df["b"] / 100
t_manual = time.time() - t0
t0 = time.time()
df["d_eval"] = pd.eval("df.a + df.b - df.a * df.b / 100")
t_eval = time.time() - t0
print(f"  Manual: {t_manual:.4f}s")
print(f"  eval:   {t_eval:.4f}s")

print("\n4. Categorical optimization:")
t0 = time.time()
df.groupby("c")["a"].mean()
t_obj = time.time() - t0
df["c"] = df["c"].astype("category")
t0 = time.time()
df.groupby("c", observed=True)["a"].mean()
t_cat = time.time() - t0
print(f"  Object groupby: {t_obj:.4f}s")
print(f"  Category groupby: {t_cat:.4f}s")
