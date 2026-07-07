"""PCA — dimensionality reduction, explained variance, reconstruction."""
import numpy as np
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler


print("=== PCA ===\n")

iris = load_iris()
X, y, feature_names = iris.data, iris.target, iris.feature_names

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca_full = PCA()
pca_full.fit(X_scaled)

print("Explained variance ratio:")
cumsum = 0
for i, (var, name) in enumerate(zip(pca_full.explained_variance_ratio_, feature_names)):
    cumsum += var
    print(f"  PC{i+1} ({name}): {var:.4f} (cumulative: {cumsum:.4f})")

print(f"\nPCA to 2 components:")
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X_scaled)
print(f"  Reduced shape: {X_reduced.shape}")
print(f"  Explained variance (2 PCs): {pca.explained_variance_ratio_.sum():.4f}")

print(f"\nComponent loadings:")
components = pca.components_
for i, comp in enumerate(components):
    print(f"  PC{i+1}: {dict(zip(feature_names, comp.round(3)))}")

print(f"\nReconstruction error:")
pca_2 = PCA(n_components=2)
X_reduced_2 = pca_2.fit_transform(X_scaled)
X_reconstructed = pca_2.inverse_transform(X_reduced_2)
recon_error = np.mean((X_scaled - X_reconstructed) ** 2)
print(f"  MSE (2 components): {recon_error:.6f}")

pca_3 = PCA(n_components=3)
X_reduced_3 = pca_3.fit_transform(X_scaled)
X_reconstructed_3 = pca_3.inverse_transform(X_reduced_3)
recon_error_3 = np.mean((X_scaled - X_reconstructed_3) ** 2)
print(f"  MSE (3 components): {recon_error_3:.6f}")

print(f"\nAuto-select n_components (95% variance):")
pca_95 = PCA(n_components=0.95)
X_reduced_95 = pca_95.fit_transform(X_scaled)
print(f"  Components needed: {X_reduced_95.shape[1]}")
