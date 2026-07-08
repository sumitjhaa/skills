"""PCA (classical, kernel) from scratch."""
import numpy as np
from sklearn.datasets import make_blobs

class PCA:
    def __init__(self, n_components=2):
        self.n_components = n_components

    def fit(self, X):
        X_centered = X - X.mean(axis=0)
        cov = X_centered.T @ X_centered / (X.shape[0] - 1)
        eigvals, eigvecs = np.linalg.eigh(cov)
        idx = np.argsort(eigvals)[::-1][:self.n_components]
        self.components_ = eigvecs[:, idx]
        self.explained_variance_ = eigvals[idx]
        self.mean_ = X.mean(axis=0)
        return self

    def transform(self, X):
        return (X - self.mean_) @ self.components_

class KernelPCA:
    def __init__(self, n_components=2, gamma=1.0):
        self.n_components = n_components
        self.gamma = gamma

    def fit(self, X):
        n = X.shape[0]
        K = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                K[i, j] = np.exp(-self.gamma * np.sum((X[i] - X[j])**2))
        one_n = np.ones((n, n)) / n
        K_centered = K - one_n @ K - K @ one_n + one_n @ K @ one_n
        eigvals, eigvecs = np.linalg.eigh(K_centered)
        idx = np.argsort(eigvals)[::-1][:self.n_components]
        self.alphas_ = eigvecs[:, idx] / np.sqrt(np.abs(eigvals[idx]) + 1e-10)
        self.X_fit_ = X
        return self

    def transform(self, X):
        K = np.zeros((X.shape[0], self.X_fit_.shape[0]))
        for i in range(X.shape[0]):
            for j in range(self.X_fit_.shape[0]):
                K[i, j] = np.exp(-self.gamma * np.sum((X[i] - self.X_fit_[j])**2))
        return K @ self.alphas_

if __name__ == "__main__":
    X, _ = make_blobs(n_samples=100, n_features=10, random_state=42)

    pca = PCA(n_components=2)
    pca.fit(X)
    X_pca = pca.transform(X)
    print(f"PCA explained variance: {pca.explained_variance_}")
    print(f"Transformed shape: {X_pca.shape}")

    kpca = KernelPCA(n_components=2, gamma=0.1)
    kpca.fit(X)
    X_kpca = kpca.transform(X)
    print(f"Kernel PCA transformed shape: {X_kpca.shape}")

    from sklearn.decomposition import PCA as SKPCA
    sk = SKPCA(n_components=2).fit(X)
    print(f"sklearn PCA explained variance: {sk.explained_variance_}")
