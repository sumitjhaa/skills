# 27. Tensor Networks: MPS, TT, PEPS

## Introduction

Tensor networks decompose high-order tensors into networks of smaller tensors. They originated in quantum physics and are increasingly used in ML for handling exponentially large state spaces.

## Matrix Product States (MPS) / Tensor Train (TT)

A d-dimensional tensor is represented as a chain of 3-way tensors:

X(i₁,i₂,...,i_d) = Σ_{α₁,...,α_{d-1}} G₁(i₁,α₁) G₂(α₁,i₂,α₂) ... G_d(α_{d-1},i_d)

Storage cost: O(d·r²·n) instead of O(n^d), where r is the bond dimension.

```python
def mps_to_tensor(cores):
    """Convert MPS cores to full tensor."""
    d = len(cores)
    result = cores[0]
    for k in range(1, d):
        result = np.tensordot(result, cores[k], axes=(-1, 0))
    return result
```

## PEPS (Projected Entangled Pair States)

PEPS extends MPS to 2D grid structures, capturing more complex entanglement at higher computational cost.

## DMRG for ML

The Density Matrix Renormalization Group (DMRG) algorithm optimizes MPS for regression and classification:

```python
def dmrg_sweep(cores, X, y, direction='right'):
    # Sweep through sites, optimizing one core at a time
    for site in range(len(cores)):
        # Fix other cores, optimize current
        cores[site] = local_optimization(cores, site, X, y)
    return cores
```

## Tensor Regression Networks

Replace the weight matrix in regression with an MPS, reducing parameters from exponential to polynomial.

## What You'll Implement

- MPS/TT decomposition and reconstruction
- PEPS structure
- DMRG-inspired optimization for ML
- Tensor regression network
- Compression ratio analysis
- Compare with full tensor methods
