import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh as scipy_eigh
from sklearn.datasets import make_classification
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def generalized_eigenvalues(A, B):
    """Solve generalized eigenvalue problem A v = lambda B v.

    Assumes A symmetric, B symmetric positive definite.
    """
    L = np.linalg.cholesky(B)
    L_inv = np.linalg.solve(L, np.eye(B.shape[0]))
    A_tilde = L_inv.T @ A @ L_inv
    eigvals, eigvecs = np.linalg.eigh(A_tilde)
    eigvecs = L_inv.T @ eigvecs
    return eigvals, eigvecs


def gsvd_simple(A, B):
    """Simplified GSVD for two matrices with same number of columns."""
    m, n = A.shape
    p, n2 = B.shape
    assert n == n2

    C = np.vstack([A, B])

    Uc, sc, Vct = np.linalg.svd(C, full_matrices=False)

    Q = Vct[:n].T

    U1, s1, V1t = np.linalg.svd(A @ Q)
    U2, s2, V2t = np.linalg.svd(B @ Q)

    return s1, s2, Q


def lda_fit(X, y, k=None):
    """LDA via generalized eigenvalue problem."""
    classes = np.unique(y)
    n_classes = len(classes)
    n_features = X.shape[1]

    if k is None:
        k = n_classes - 1

    overall_mean = X.mean(axis=0)
    class_means = []
    S_W = np.zeros((n_features, n_features))
    S_B = np.zeros((n_features, n_features))

    for c in classes:
        X_c = X[y == c]
        n_c = len(X_c)
        mean_c = X_c.mean(axis=0)
        class_means.append(mean_c)

        S_W += (X_c - mean_c).T @ (X_c - mean_c)
        mean_diff = (mean_c - overall_mean).reshape(-1, 1)
        S_B += n_c * mean_diff @ mean_diff.T

    eigvals, eigvecs = generalized_eigenvalues(S_B, S_W)

    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]

    return eigvecs[:, :k], eigvals[:k], class_means


def cca_simple(X, Y, k=2):
    """CCA via generalized eigenvalue problem."""
    n = X.shape[0]
    X_centered = X - X.mean(axis=0)
    Y_centered = Y - Y.mean(axis=0)

    C_xx = X_centered.T @ X_centered / (n - 1)
    C_yy = Y_centered.T @ Y_centered / (n - 1)
    C_xy = X_centered.T @ Y_centered / (n - 1)

    C_xx_reg = C_xx + 1e-6 * np.eye(C_xx.shape[0])
    C_yy_reg = C_yy + 1e-6 * np.eye(C_yy.shape[0])

    Lx = np.linalg.cholesky(C_xx_reg)
    Ly = np.linalg.cholesky(C_yy_reg)

    Lx_inv = np.linalg.solve(Lx, np.eye(Lx.shape[0]))
    Ly_inv = np.linalg.solve(Ly, np.eye(Ly.shape[0]))

    K = Lx_inv.T @ C_xy @ Ly_inv
    Uk, sk, Vkt = np.linalg.svd(K)

    A = Lx_inv @ Uk[:, :k]
    B = Ly_inv @ Vkt[:k].T

    return A, B, sk[:k]


def main():
    print("=" * 60)
    print("GENERALIZED EIGENVALUE PROBLEMS AND GSVD")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- Generalized Eigenvalues ---")
    A = np.array([[4.0, 1.0], [1.0, 3.0]])
    B = np.array([[2.0, 0.5], [0.5, 1.0]])

    eigvals, eigvecs = generalized_eigenvalues(A, B)
    print(f"A =\n{A}")
    print(f"B =\n{B}")
    print(f"Generalized eigenvalues: {np.round(eigvals, 4)}")

    for i, (lam, v) in enumerate(zip(eigvals, eigvecs.T)):
        Av = A @ v
        lBv = lam * (B @ v)
        print(f"  lambda_{i} = {lam:.4f}, |Av - lambda Bv| = {np.linalg.norm(Av - lBv):.2e}")

    ref_eigvals = scipy_eigh(A, B, eigvals_only=True)
    print(f"Reference: {np.round(ref_eigvals, 4)}")

    print("\n--- GSVD ---")
    m, p, n = 8, 6, 5
    A_gsvd = np.random.randn(m, n)
    B_gsvd = np.random.randn(p, n)
    s1, s2, Q = gsvd_simple(A_gsvd, B_gsvd)
    print(f"GSVD singular values (A): {np.round(s1[:n], 3)}")
    print(f"GSVD singular values (B): {np.round(s2[:n], 3)}")

    print("\n--- LDA (Generalized Eigenvalue) ---")
    X, y = make_classification(n_samples=200, n_features=10,
                                n_classes=3, n_informative=5,
                                n_redundant=2, random_state=42)

    W_lda, evals, means = lda_fit(X, y, k=2)
    print(f"LDA weight matrix shape: {W_lda.shape}")
    print(f"Generalized eigenvalues: {np.round(evals, 4)}")

    X_lda = X @ W_lda

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    colors = ['r', 'b', 'g']
    for c in np.unique(y):
        mask = y == c
        axes[0].scatter(X[mask, 0], X[mask, 1], c=colors[c], label=f'Class {c}', alpha=0.6)
    axes[0].set_title('Original Data (first 2 features)')
    axes[0].legend()

    for c in np.unique(y):
        mask = y == c
        axes[1].scatter(X_lda[mask, 0], X_lda[mask, 1], c=colors[c],
                        label=f'Class {c}', alpha=0.6)
    axes[1].set_title('LDA (via Generalized Eigenvalues)')
    axes[1].legend()
    plt.tight_layout()
    plt.show()

    sklearn_lda = LinearDiscriminantAnalysis(n_components=2)
    sklearn_lda.fit(X, y)
    X_sklearn = sklearn_lda.transform(X)
    print(f"Scikit-learn LDA projection match: "
          f"{np.allclose(np.abs(X_lda), np.abs(X_sklearn), atol=1e-2)}")

    print("\n--- CCA (Canonical Correlation Analysis) ---")
    n_samples = 200
    n_features_x = 5
    n_features_y = 4

    z = np.random.randn(n_samples, 2)
    X_cca = z @ np.random.randn(2, n_features_x) + 0.1 * np.random.randn(n_samples, n_features_x)
    Y_cca = z @ np.random.randn(2, n_features_y) + 0.1 * np.random.randn(n_samples, n_features_y)

    A_cca, B_cca, can_corrs = cca_simple(X_cca, Y_cca, k=2)
    print(f"CCA canonical correlations: {np.round(can_corrs, 4)}")
    print(f"First canonical correlation: {can_corrs[0]:.4f}")

    X_c = X_cca - X_cca.mean(axis=0)
    Y_c = Y_cca - Y_cca.mean(axis=0)
    X_scores = X_c @ A_cca
    Y_scores = Y_c @ B_cca
    for i in range(min(2, len(can_corrs))):
        corr = np.corrcoef(X_scores[:, i], Y_scores[:, i])[0, 1]
        print(f"  Canonical variate {i+1}: correlation = {corr:.4f}")

    print("\n--- Rayleigh Quotient for Generalized Problems ---")
    n_rand = 10
    A_rand = np.random.randn(n_rand, n_rand)
    A_rand = A_rand.T @ A_rand
    B_rand = np.random.randn(n_rand, n_rand)
    B_rand = B_rand.T @ B_rand + np.eye(n_rand)

    ev, _ = generalized_eigenvalues(A_rand, B_rand)
    print(f"Random generalized eigenvalues: min={ev[0]:.4f}, max={ev[-1]:.4f}")


if __name__ == "__main__":
    main()
