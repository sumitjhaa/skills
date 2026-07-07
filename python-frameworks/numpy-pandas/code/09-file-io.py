"""File I/O — save and load arrays in text, binary, compressed formats."""
import numpy as np
import tempfile
import os


print("=== File I/O ===")

arr = np.array([[1.5, 2.3, 3.1], [4.7, 5.2, 6.9]])
print(f"Original array:\n{arr}")

tmpdir = tempfile.mkdtemp()

csv_file = os.path.join(tmpdir, "data.csv")
np.savetxt(csv_file, arr, delimiter=",", header="a,b,c")
loaded_csv = np.loadtxt(csv_file, delimiter=",", skiprows=1)
print(f"\nCSV load:\n{loaded_csv}")

npy_file = os.path.join(tmpdir, "array.npy")
np.save(npy_file, arr)
loaded_npy = np.load(npy_file)
print(f"\nNPY load:\n{loaded_npy}")

npz_file = os.path.join(tmpdir, "data.npz")
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
np.savez(npz_file, a=a, b=b)
loaded = np.load(npz_file)
print(f"\nNPZ load:")
print(f"  a: {loaded['a']}")
print(f"  b: {loaded['b']}")

npz_comp = os.path.join(tmpdir, "data_compressed.npz")
np.savez_compressed(npz_file, a=a, b=b)
print(f"\nNPZ file size:")
print(f"  npy:   {os.path.getsize(npy_file)} bytes")
print(f"  npz:   {os.path.getsize(npz_file)} bytes")

for f in os.listdir(tmpdir):
    os.remove(os.path.join(tmpdir, f))
os.rmdir(tmpdir)
