# 📐 Linear Algebra
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Matrix operations, dot products, decompositions, solving systems.

## Matrix Multiplication

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

np.dot(a, b)       # [[19 22] [43 50]]
a @ b              # Same (Python 3.5+)
```

## Transpose & Reshape

```python
a.T       # Transpose
a.reshape(4,)  # [1 2 3 4]
a.flatten()    # Same but returns copy
```

## Common Operations

```python
np.linalg.inv(a)       # Inverse
np.linalg.det(a)       # Determinant
np.linalg.eig(a)       # Eigenvalues & eigenvectors
np.linalg.svd(a)       # SVD decomposition
```

## Solving Linear Systems

```python
A = np.array([[2, 1], [1, 1]])
b = np.array([5, 3])
x = np.linalg.solve(A, b)
# x = [2. 1.]
```

<!-- 🧠 Use `@` for matrix multiplication — it's cleaner than `np.dot()` or `np.matmul()`. -->

## Run the Code

```bash
python code/05-linear-algebra.py
```
