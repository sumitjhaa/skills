"""Factor Analysis, CCA, and PLS from scratch."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs, make_regression

class FactorAnalysis:
    def __init__(self, n_components=2, max_iter=500, tol=1e-4):
        self.n_components = n_components
        self.max_iter = max_iter
        self.tol = tol

    def fit(self, X):
        n, d = X.shape
        self.mean_ = X.mean(axis=0)
        Xc = X - self.mean_

        L = np.random.randn(d, self.n_components) * 0.1
        Psi = np.ones(d) * 0.5

        for iteration in range(self.max_iter):
            Psi_inv = 1.0 / (Psi + 1e-10)
            LP = L * Psi_inv[:, None]
            M = np.linalg.inv(np.eye(self.n_components) + L.T @ LP)

            L_new = Xc.T @ (Xc @ (LP @ M)) / n
            L_new /= np.sqrt(np.sum(L_new**2, axis=0, keepdims=True) + 1e-10)

            XLML = Xc @ (L_new @ M @ L_new.T)
            resid = Xc - XLML
            Psi_new = np.mean(resid**2, axis=0)
            Psi_new = np.maximum(Psi_new, 1e-6)

            diff = np.max(np.abs(L_new - L))
            L = L_new
            Psi = Psi_new
            if diff < self.tol:
                print(f"  FA converged in {iteration + 1} iterations")
                break

        self.components_ = L
        self.noise_variance_ = Psi
        return self

    def transform(self, X):
        Xc = X - self.mean_
        Psi_inv = 1.0 / (self.noise_variance_ + 1e-10)
        M = np.linalg.inv(np.eye(self.n_components) + self.components_.T @ (self.components_ * Psi_inv[:, None]))
        return Xc @ ((self.components_ * Psi_inv[:, None]) @ M)

def cca(X, Y, n_components=2):
    """Canonical Correlation Analysis from scratch."""
    Xc = X - X.mean(axis=0)
    Yc = Y - Y.mean(axis=0)
    n = X.shape[0]

    C_xx = Xc.T @ Xc / n
    C_yy = Yc.T @ Yc / n
    C_xy = Xc.T @ Yc / n

    C_xx_inv = np.linalg.inv(C_xx + 1e-6 * np.eye(C_xx.shape[0]))
    C_yy_inv = np.linalg.inv(C_yy + 1e-6 * np.eye(C_yy.shape[0]))

    M = C_xx_inv @ C_xy @ C_yy_inv @ C_xy.T
    eigvals, eigvecs = np.linalg.eigh(M)
    idx = np.argsort(eigvals)[::-1][:n_components]
    A = eigvecs[:, idx]
    B = C_yy_inv @ C_xy.T @ A

    for i in range(n_components):
        A[:, i] /= np.sqrt(A[:, i].T @ C_xx @ A[:, i] + 1e-10)
        B[:, i] /= np.sqrt(B[:, i].T @ C_yy @ B[:, i] + 1e-10)

    X_c = Xc @ A
    Y_c = Yc @ B
    corrs = np.array([np.corrcoef(X_c[:, i], Y_c[:, i])[0, 1] for i in range(n_components)])
    return X_c, Y_c, corrs, A, B

def pls(X, Y, n_components=2):
    """Partial Least Squares from scratch (SIMPLS)."""
    Xc = X - X.mean(axis=0)
    Yc = Y - Y.mean(axis=0)
    n, d = X.shape

    W = np.zeros((d, n_components))
    T = np.zeros((n, n_components))
    P = np.zeros((d, n_components))
    Q = np.zeros((Yc.shape[1], n_components))

    Xi = Xc.copy()
    Yi = Yc.copy()

    for k in range(n_components):
        w = Xi.T @ Yi
        w = w[:, 0] if w.ndim > 1 else w
        w = w / np.linalg.norm(w)
        t = Xi @ w
        p = Xi.T @ t / (t @ t)
        q = Yi.T @ t / (t @ t)
        Xi = Xi - np.outer(t, p)
        Yi = Yi - np.outer(t, q)
        W[:, k] = w
        T[:, k] = t
        P[:, k] = p
        Q[:, k] = q if q.ndim > 0 else q

    return T, W, P, Q

if __name__ == "__main__":
    np.random.seed(42)
    print("=== Factor Analysis ===")
    X, y = make_blobs(n_samples=200, n_features=10, centers=3, random_state=42)

    fa = FactorAnalysis(n_components=3)
    fa.fit(X)
    X_fa = fa.transform(X)
    print(f"  FA transformed: {X_fa.shape}")

    from sklearn.decomposition import FactorAnalysis as SKFA
    sk = SKFA(n_components=3, random_state=42).fit(X)
    print(f"  sklearn FA components: {sk.components_.shape}")

    print("\n=== Canonical Correlation Analysis ===")
    X_c, Y = make_regression(n_samples=200, n_features=5, n_targets=3, noise=0.5, random_state=42)
    X_c2 = np.random.randn(200, 4)
    Y2 = X_c[:, :2] @ np.random.randn(2, 3) + X_c2[:, :2] @ np.random.randn(2, 3) + np.random.randn(200, 3) * 0.1

    X_cc, Y_cc, corrs, A, B = cca(X_c, Y2, n_components=3)
    print(f"  Canonical correlations: {[f'{c:.4f}' for c in corrs]}")

    from sklearn.cross_decomposition import CCA
    sk_cca = CCA(n_components=3)
    sk_cca.fit(X_c, Y2)
    print(f"  sklearn CCA correlations computed")

    print("\n=== Partial Least Squares ===")
    X_pls, Y_pls = make_regression(n_samples=200, n_features=10, n_targets=2, noise=0.3, random_state=42)
    T, W, P, Q = pls(X_pls, Y_pls, n_components=5)
    print(f"  PLS scores: {T.shape}, X-loadings: {P.shape}, Y-loadings: {Q.shape}")
    var_ratios = np.var(T, axis=0)[:3] / np.var(T).sum()
    print(f"  Variance explained (first 3 comps): {[f'{r:.3f}' for r in var_ratios]}")

    # Visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # FA: factor loadings heatmap
    im = axes[0, 0].imshow(fa.components_, aspect='auto', cmap='RdBu')
    axes[0, 0].set_xlabel("Factor")
    axes[0, 0].set_ylabel("Feature")
    axes[0, 0].set_title("FA Factor Loadings")
    plt.colorbar(im, ax=axes[0, 0])

    # FA: noise variance
    axes[0, 1].bar(range(len(fa.noise_variance_)), fa.noise_variance_)
    axes[0, 1].set_xlabel("Feature")
    axes[0, 1].set_ylabel("Noise variance (ψ)")
    axes[0, 1].set_title("FA Unique Variances")
    axes[0, 1].grid(True, axis='y', alpha=0.3)

    # CCA: canonical variates
    axes[1, 0].scatter(X_cc[:, 0], Y_cc[:, 0], alpha=0.6, s=20)
    axes[1, 0].set_xlabel("First canonical variate (X)")
    axes[1, 0].set_ylabel("First canonical variate (Y)")
    axes[1, 0].set_title(f"CCA: ρ₁={corrs[0]:.4f}")
    axes[1, 0].grid(True, alpha=0.3)

    # PLS: scores
    axes[1, 1].scatter(T[:, 0], T[:, 1], alpha=0.6, s=20)
    axes[1, 1].set_xlabel("PLS component 1")
    axes[1, 1].set_ylabel("PLS component 2")
    axes[1, 1].set_title("PLS Scores")
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("../../assets/phase05/25-factor-cca-pls.png")
    plt.close()
    print("\nFigure saved to 25-factor-cca-pls.png")
