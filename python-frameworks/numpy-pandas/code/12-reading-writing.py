"""Reading and writing data in various formats."""
import pandas as pd
import numpy as np
import tempfile
import os


print("=== Reading & Writing Data ===")

tmpdir = tempfile.mkdtemp()

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "score": [88.5, 92.3, 85.0],
})

csv_path = os.path.join(tmpdir, "data.csv")
df.to_csv(csv_path, index=False)
loaded_csv = pd.read_csv(csv_path)
print(f"CSV:\n{loaded_csv}")

df.to_csv(csv_path, index=False)
loaded_idx = pd.read_csv(csv_path, index_col=0)
print(f"\nCSV with index:\n{loaded_idx}")

json_path = os.path.join(tmpdir, "data.json")
df.to_json(json_path, orient="records", indent=2)
loaded_json = pd.read_json(json_path)
print(f"\nJSON:\n{loaded_json}")

parquet_path = os.path.join(tmpdir, "data.parquet")
try:
    df.to_parquet(parquet_path, index=False)
    loaded_pq = pd.read_parquet(parquet_path)
    print(f"\nParquet:\n{loaded_pq}")
except Exception as e:
    print(f"\nParquet not available: {e}")

print(f"\nOptions demo:")
pd.set_option("display.precision", 3)
print(df.describe())

for f in os.listdir(tmpdir):
    os.remove(os.path.join(tmpdir, f))
os.rmdir(tmpdir)
