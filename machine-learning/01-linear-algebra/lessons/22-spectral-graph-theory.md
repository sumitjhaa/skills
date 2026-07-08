# 22. Spectral Graph Theory

## Introduction

Spectral graph theory studies graph properties through the eigenvalues and eigenvectors of associated matrices (adjacency, Laplacian).

## Graph Fourier Transform

The eigenvectors of the graph Laplacian form a Fourier-like basis for signals defined on the graph:

**x̂** = Uᵀ**x** (graph Fourier transform)
**x** = U**x̂** (inverse graph Fourier transform)

```python
def graph_fourier_transform(L, x):
    eigvals, U = np.linalg.eigh(L)
    x_hat = U.T @ x
    return x_hat, eigvals, U
```

## Spectral Graph Convolution

Convolution on graphs is defined in the spectral domain:

g ⋆ **x** = U g(Λ) Uᵀ **x**

where g(Λ) is a diagonal matrix of filter coefficients applied to eigenvalues.

```python
def spectral_convolution(L, x, filter_coeffs):
    eigvals, U = np.linalg.eigh(L)
    x_hat = U.T @ x
    x_filtered = U @ (filter_coeffs * x_hat)
    return x_filtered
```

## Spectral Graph CNN

ChebNet approximates the filter using Chebyshev polynomials of the Laplacian, avoiding explicit eigendecomposition:

g_θ(Λ) ≈ Σⱼ θⱼ Tⱼ(Λ̃)

## Applications

- **Community detection**: Spectral clustering
- **Graph signal denoising**: Low-pass filtering in spectral domain
- **Node classification**: Spectral GCNs
- **Graph visualization**: Laplacian eigenmaps

## What You'll Implement

- Graph Fourier transform (forward and inverse)
- Spectral filtering (low-pass, high-pass, band-pass)
- Chebyshev polynomial filter approximation
- Spectral graph convolution layer
- Graph signal denoising example
- Visualize graph signals in spectral domain
