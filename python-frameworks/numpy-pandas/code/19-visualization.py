"""Quick visualization with pandas + matplotlib."""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import tempfile
import os


print("=== Visualization ===")

rng = np.random.default_rng(42)
dates = pd.date_range("2025-01-01", periods=100, freq="D")
df = pd.DataFrame({
    "date": dates,
    "sales": rng.normal(1000, 200, 100).cumsum(),
    "expenses": rng.normal(800, 150, 100).cumsum(),
})
df.set_index("date", inplace=True)

tmpdir = tempfile.mkdtemp()

print("\nLine plot:")
ax = df.plot(title="Sales vs Expenses", figsize=(8, 4), grid=True)
plt.tight_layout()
path = os.path.join(tmpdir, "line.png")
plt.savefig(path)
print(f"  Saved: {path}")
plt.close()

print("\nHistogram:")
ax = df["sales"].plot(kind="hist", bins=15, title="Sales Distribution")
plt.tight_layout()
path = os.path.join(tmpdir, "hist.png")
plt.savefig(path)
print(f"  Saved: {path}")
plt.close()

cats = pd.DataFrame({
    "category": rng.choice(["A", "B", "C", "D"], 50),
    "value": rng.exponential(100, 50),
})
print("\nBar plot:")
cats.groupby("category")["value"].sum().plot(kind="bar", title="Total by Category")
plt.tight_layout()
path = os.path.join(tmpdir, "bar.png")
plt.savefig(path)
print(f"  Saved: {path}")
plt.close()

print("\nBoxplot:")
cats.boxplot(column="value", by="category")
plt.tight_layout()
path = os.path.join(tmpdir, "box.png")
plt.savefig(path)
print(f"  Saved: {path}")
plt.close()

for f in os.listdir(tmpdir):
    os.remove(os.path.join(tmpdir, f))
os.rmdir(tmpdir)
print("\nAll plots generated successfully.")
