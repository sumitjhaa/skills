#!/usr/bin/env python3
"""03.26 Multivariate Methods: PCA, CCA, and Factor Analysis concepts."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
n = 500

# Generate correlated data
Z = np.random.normal(0, 1, (n, 2))
X = Z @ np.array([[1, 0.7], [0.7, 1]]) + np.random.normal(0, 0.1, (n, 2))
Y = Z @ np.array([[0.5, -0.3], [-0.3, 0.8]]) + np.random.normal(0, 0.1, (n, 2))

# PCA on X
X_centered = X - X.mean(axis=0)
cov_X = X_centered.T @ X_centered / (n - 1)
eigvals, eigvecs = np.linalg.eigh(cov_X)
# Sort descending
idx = np.argsort(eigvals)[::-1]
eigvals = eigvals[idx]
eigvecs = eigvecs[:, idx]
X_proj = X_centered @ eigvecs

# Explained variance
var_exp = eigvals / eigvals.sum()

# CCA between X and Y (simplified)
X_cent = X - X.mean(axis=0)
Y_cent = Y - Y.mean(axis=0)
Qx, Rx = np.linalg.qr(X_cent)
Qy, Ry = np.linalg.qr(Y_cent)
_, S, _ = np.linalg.svd(Qx.T @ Qy)
cca_corrs = np.diag(S)

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].scatter(X[:, 0], X[:, 1], alpha=0.5)
for i in range(2):
    axes[0, 0].arrow(0, 0, eigvecs[0, i]*3, eigvecs[1, i]*3, 
                     color=f'C{i+1}', width=0.05, label=f"PC{i+1}")
axes[0, 0].set_title(f"PCA: Explained Variance {var_exp[0]:.1%}, {var_exp[1]:.1%}")
axes[0, 0].set_xlabel("X₁")
axes[0, 0].set_ylabel("X₂")
axes[0, 0].legend()
axes[0, 0].axis('equal')

axes[0, 1].bar([1, 2], eigvals, alpha=0.6)
axes[0, 1].set_xlabel("Component")
axes[0, 1].set_ylabel("Eigenvalue")
axes[0, 1].set_title("Scree Plot")
axes[0, 1].set_xticks([1, 2])

axes[1, 0].scatter(X_proj[:, 0], X_proj[:, 1], alpha=0.5)
axes[1, 0].set_xlabel("PC1")
axes[1, 0].set_ylabel("PC2")
axes[1, 0].set_title("Projection onto Principal Components")
axes[1, 0].axis('equal')

axes[1, 1].bar([1, 2], cca_corrs, alpha=0.6)
axes[1, 1].set_ylim(0, 1)
axes[1, 1].set_xticks([1, 2])
axes[1, 1].set_ylabel("Canonical Correlation")
axes[1, 1].set_title("CCA: X vs Y")
plt.tight_layout()
plt.savefig("../../assets/phase03/26-multivariate-methods.png")
plt.close()

print("PCA eigenvalues:", np.round(eigvals, 3))
print("PCA explained variance:", np.round(var_exp, 3))
print("CCA canonical correlations:", np.round(cca_corrs, 3))
