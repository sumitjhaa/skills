# 08. Eigenvalues: Power Iteration, QR Algorithm, Rayleigh Quotient

## Introduction

Eigenvalues and eigenvectors are fundamental: A**v** = λ**v**. The set of eigenvalues is the **spectrum** of A.

## Power Iteration

The simplest method to find the dominant eigenvalue:

```python
def power_iteration(A, max_iter=1000, tol=1e-10):
    n = A.shape[0]
    v = np.random.randn(n)
    v = v / np.linalg.norm(v)
    for i in range(max_iter):
        Av = A @ v
        v_new = Av / np.linalg.norm(Av)
        lam = v_new @ (A @ v_new)
        if np.linalg.norm(v_new - v) < tol:
            break
        v = v_new
    return lam, v
```

## Inverse Iteration

To find eigenvalues near a shift μ, apply power iteration to (A − μI)⁻¹:

```python
def inverse_iteration(A, mu, max_iter=100, tol=1e-10):
    n = A.shape[0]
    v = np.random.randn(n)
    v = v / np.linalg.norm(v)
    B = A - mu * np.eye(n)
    for _ in range(max_iter):
        w = np.linalg.solve(B, v)
        v_new = w / np.linalg.norm(w)
        lam = v_new @ (A @ v_new)
        if np.linalg.norm(v_new - v) < tol:
            break
        v = v_new
    return lam, v
```

## Rayleigh Quotient

ρ(**x**) = (**x**ᵀA**x**) / (**x**ᵀ**x**) lies between λₘᵢₙ and λₘₐₓ. The gradient of ρ gives the eigenvector direction.

## QR Algorithm

The workhorse for computing all eigenvalues:

```python
def qr_algorithm(A, max_iter=1000, tol=1e-10):
    T = A.copy()
    n = A.shape[0]
    for _ in range(max_iter):
        Q, R = np.linalg.qr(T)
        T = R @ Q
        off_diag = np.linalg.norm(np.tril(T, -1))
        if off_diag < tol:
            break
    return np.diag(T)
```

With shifts (Wilkinson shift or Rayleigh quotient shift), convergence is cubic.

## Lanczos Iteration

For large sparse symmetric matrices, Lanczos tridiagonalizes the matrix:

```python
def lanczos(A, k):
    n = A.shape[0]
    v = np.random.randn(n)
    v = v / np.linalg.norm(v)
    alpha = np.zeros(k)
    beta = np.zeros(k)
    V = np.zeros((n, k+1))
    V[:, 0] = v
    for j in range(k):
        w = A @ V[:, j]
        alpha[j] = V[:, j] @ w
        w -= alpha[j] * V[:, j]
        if j > 0:
            w -= beta[j-1] * V[:, j-1]
        beta[j] = np.linalg.norm(w)
        if beta[j] > 1e-14:
            V[:, j+1] = w / beta[j]
        else:
            break
    T = np.diag(alpha) + np.diag(beta[:k-1], 1) + np.diag(beta[:k-1], -1)
    return T, V
```

## What You'll Implement

- Power iteration for dominant eigenvalue
- Inverse iteration with shift
- Rayleigh quotient iteration (cubic convergence)
- Basic QR algorithm (without and with shifts)
- Lanczos iteration for symmetric matrices
- Convergence visualization
