# 💾 File I/O
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Load and save arrays (text, binary, compressed).

## Text Files

```python
np.savetxt("data.csv", arr, delimiter=",", header="a,b,c")
arr = np.loadtxt("data.csv", delimiter=",", skiprows=1)
```

## Binary (NumPy Format)

```python
np.save("array.npy", arr)       # Single array
arr = np.load("array.npy")

np.savez("data.npz", a=a, b=b)  # Multiple arrays
data = np.load("data.npz")
data["a"], data["b"]
```

## Compressed

```python
np.savez_compressed("data.npz", a=a, b=b)  # Smaller file
```

## CSV with Pandas

```python
import pandas as pd
df = pd.read_csv("data.csv")
arr = df.to_numpy()
```

<!-- 🤔 Use `.npy` for speed, `.csv` for interoperability. -->

## Run the Code

```bash
python code/09-file-io.py
```
