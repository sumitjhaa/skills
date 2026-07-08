# 16. Random Matrix Theory: Wigner, Marchenko–Pastur, Tracy–Widom

## Introduction

Random matrix theory (RMT) studies the eigenvalue distributions of matrices with random entries. It provides universal laws governing the spectra of large random matrices.

## Wigner's Semicircle Law

For an n×n symmetric random matrix with i.i.d. entries (mean 0, variance σ²), the empirical spectral distribution converges to a semicircle:

ρ(λ) = (1/(2πσ²)) √(4σ² − λ²), |λ| ≤ 2σ

```python
import numpy as np

def wigner_matrix(n, sigma=1):
    X = np.random.randn(n, n) * sigma / np.sqrt(n)
    return (X + X.T) / np.sqrt(2)

eigvals = np.linalg.eigvalsh(wigner_matrix(1000))
```

## Marchenko–Pastur Law

For a sample covariance matrix S = (1/p) X Xᵀ where X ∈ ℝ^{p×n} has i.i.d. entries, the spectral density follows:

ρ(λ) = (1/(2πλγσ²)) √((b − λ)(λ − a)), a ≤ λ ≤ b

where γ = p/n, a = σ²(1 − √γ)², b = σ²(1 + √γ)².

```python
def marchenko_pastur(n, p):
    X = np.random.randn(p, n)
    S = X @ X.T / n
    return np.linalg.eigvalsh(S)
```

## Tracy–Widom Law

The largest eigenvalue of a random matrix follows the Tracy–Widom distribution, with fluctuations of order n^{-2/3}.

## Spiked Covariance Model

When a low-rank signal is added to noise, the top eigenvalues exhibit a phase transition: they "pop out" of the bulk when the signal exceeds a threshold.

## Phase Transitions

For a rank-1 perturbation ρ**uv**ᵀ, the top eigenvalue separates from the bulk only when ρ > 1/√γ.

## What You'll Implement

- Generate Wigner matrices and verify semicircle law
- Generate sample covariance matrices and verify Marchenko–Pastur
- Compute Tracy–Widom limiting distribution
- Spiked covariance model with phase transition
- Visualize eigenvalue distributions
- Detect signal from noise using RMT thresholds
