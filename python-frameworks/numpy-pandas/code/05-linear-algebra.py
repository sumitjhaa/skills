"""Linear algebra — matrix ops, solve, eig, SVD."""
import numpy as np


print("=== Linear Algebra ===")

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print(f"A:\n{a}")
print(f"B:\n{b}")
print(f"A @ B:\n{a @ b}")
print(f"np.dot(A, B):\n{np.dot(a, b)}")

print(f"\nTranspose & reshape:")
print(f"A.T:\n{a.T}")
print(f"A.reshape(4,): {a.reshape(4)}")
print(f"A.flatten():  {a.flatten()}")

print(f"\nMatrix properties:")
print(f"det(A): {np.linalg.det(a):.4f}")
print(f"inv(A):\n{np.linalg.inv(a)}")

print(f"\nEigenvalues:")
eigvals, eigvecs = np.linalg.eig(a)
print(f"Eigenvalues: {eigvals}")
print(f"Eigenvectors:\n{eigvecs}")

print(f"\nSolving linear system:")
A = np.array([[2, 1], [1, 1]])
b_vec = np.array([5, 3])
x = np.linalg.solve(A, b_vec)
print(f"Solve Ax = b: x = {x}")
print(f"Verify Ax = {A @ x}")

print(f"\nSVD:")
u, s, vt = np.linalg.svd(a)
print(f"U:\n{u}, s: {s}, VT:\n{vt}")
print(f"Reconstruct: U @ diag(s) @ VT:\n{u @ np.diag(s) @ vt}")
