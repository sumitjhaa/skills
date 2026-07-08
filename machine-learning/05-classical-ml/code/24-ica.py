"""ICA (FastICA) from scratch with comparison and visualization."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def fastica(X, n_components=None, max_iter=1000, tol=1e-6):
    X = X - X.mean(axis=0)
    n, d = X.shape
    cov = X.T @ X / n
    eigvals, eigvecs = np.linalg.eigh(cov)
    Dinv = np.diag(1.0 / np.sqrt(np.maximum(eigvals, 0) + 1e-10))
    Z = X @ eigvecs @ Dinv

    if n_components is None:
        n_components = d
    n_components = min(n_components, d)

    rng = np.random.RandomState(42)
    if n_components == 1:
        w = rng.randn(d)
        w = w / np.linalg.norm(w)
        for _ in range(max_iter):
            w_old = w.copy()
            wx = Z @ w
            w_new = (Z * np.tanh(wx)[:, None]).mean(axis=0) - (1 - np.tanh(wx)**2).mean() * w
            w_new = w_new / (np.linalg.norm(w_new) + 1e-10)
            w = w_new
            if np.abs(np.abs(w @ w_old) - 1) < tol:
                break
        S = Z @ w
        return S[:, None], w[None, :]

    W = rng.randn(n_components, d)
    W_u, _, W_vh = np.linalg.svd(W, full_matrices=False)
    W = W_u @ W_vh

    lrate = 0.5
    for iteration in range(max_iter):
        W_old = W.copy()
        Y = Z @ W.T
        G = np.tanh(Y)
        GP = 1 - np.tanh(Y)**2
        grad = (Z.T @ G).T / n - GP.mean(axis=0)[:, None] * W
        W = W + lrate * grad
        inner = W @ W.T
        eigvals_w, eigvecs_w = np.linalg.eigh(inner)
        eigvals_w = np.maximum(eigvals_w, 1e-10)
        W = eigvecs_w @ np.diag(1.0 / np.sqrt(eigvals_w)) @ eigvecs_w.T @ W
        change = np.min(np.abs(np.diag(W @ W_old.T)))
        if np.abs(1 - change) < tol:
            break

    S = Z @ W.T
    return S, W

def match_sources(S_est, S_true):
    """Find best correlation match between estimated and true sources."""
    n_est = S_est.shape[1]
    n_true = S_true.shape[1]
    corr_matrix = np.abs(np.corrcoef(S_est.T, S_true.T))
    corrs = corr_matrix[:n_est, n_est:]
    matches = []
    used_true = set()
    for i in range(n_est):
        best_j = max((j for j in range(n_true) if j not in used_true),
                     key=lambda j: corrs[i, j], default=None)
        if best_j is not None:
            matches.append((i, best_j, corrs[i, best_j]))
            used_true.add(best_j)
    return matches

if __name__ == "__main__":
    np.random.seed(42)
    print("=== ICA: FastICA from scratch ===\n")

    # Test 1: Laplace sources
    print("Test 1: Laplace sources, 3 sources mixed into 5 observations")
    S_true = np.random.laplace(size=(1000, 3))
    A = np.random.randn(3, 5)
    X = S_true @ A
    S_est, W = fastica(X, n_components=3)
    matches = match_sources(S_est, S_true)
    print(f"  Source correlations: {[f'{c:.3f}' for _, _, c in matches]}")
    # Debug: full correlation matrix
    corr_full = np.abs(np.corrcoef(S_est.T, S_true.T))
    n_est = S_est.shape[1]
    print(f"  Full corr matrix (est x true):\n{np.array2string(corr_full[:n_est, n_est:], precision=3, suppress_small=True)}")

    # Test 2: Uniform sources (non-Gaussian)
    print("\nTest 2: Uniform sources")
    S_true2 = np.random.uniform(-2, 2, size=(1000, 2))
    A2 = np.random.randn(2, 4)
    X2 = S_true2 @ A2
    S_est2, W2 = fastica(X2, n_components=2)
    matches2 = match_sources(S_est2, S_true2)
    print(f"  Source correlations: {[f'{c:.3f}' for _, _, c in matches2]}")

    # Test 3: Compare with sklearn
    print("\nComparison with sklearn FastICA:")
    from sklearn.decomposition import FastICA
    ica_sk = FastICA(n_components=3, random_state=42, max_iter=500)
    S_sk = ica_sk.fit_transform(X)
    matches_sk = match_sources(S_sk, S_true)
    matches_ours = match_sources(S_est, S_true)
    ours_mean = np.mean([c for _, _, c in matches_ours])
    sk_mean = np.mean([c for _, _, c in matches_sk])
    print(f"  Ours: mean corr={ours_mean:.3f}")
    print(f"  sklearn: mean corr={sk_mean:.3f}")

    # Visualization
    fig, axes = plt.subplots(3, 3, figsize=(14, 12))

    # Original sources
    for i in range(3):
        axes[0, i].plot(S_true[:200, i], lw=1)
        axes[0, i].set_title(f"True source {i + 1}")
        axes[0, i].set_xlim(0, 200)

    # Mixed signals
    for i in range(3):
        axes[1, i].plot(X[:200, i], lw=1)
        axes[1, i].set_title(f"Mixed signal {i + 1}")
        axes[1, i].set_xlim(0, 200)

    # Recovered sources
    for i in range(3):
        axes[2, i].plot(S_est[:200, i], lw=1)
        axes[2, i].set_title(f"Recovered source {i + 1}")
        axes[2, i].set_xlim(0, 200)

    plt.tight_layout()
    plt.savefig("../../assets/phase05/24-ica.png")
    plt.close()
    print("\nFigure saved to 24-ica.png")

    # Edge case: Gaussian sources (should fail - ICA needs non-Gaussian)
    print("\n=== Edge Case: Gaussian Sources ===")
    S_gauss = np.random.randn(500, 2)
    A_g = np.random.randn(2, 4)
    X_g = S_gauss @ A_g
    S_est_g, _ = fastica(X_g, n_components=2)
    matches_g = match_sources(S_est_g, S_gauss)
    print(f"  Gaussian source correlations: {[f'{c:.3f}' for _, _, c in matches_g]}")

    # Edge case: single component
    print("\n=== Edge Case: Single Component ===")
    S_single = np.random.laplace(size=(500, 1))
    A_s = np.random.randn(1, 1).ravel()
    X_s = S_single * A_s
    X_s = X_s + np.random.randn(500, 1) * 0.1
    S_est_s, _ = fastica(X_s, n_components=1)
    c = np.abs(np.corrcoef(S_est_s.ravel(), S_single.ravel())[0, 1])
    print(f"  Single source correlation: {c:.3f}")
