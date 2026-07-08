"""Isomap and LLE from scratch with visualization."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.csgraph import shortest_path
from sklearn.datasets import make_swiss_roll

def isomap(X, n_components=2, n_neighbors=10):
    n = X.shape[0]
    dists = np.sqrt(np.maximum(np.sum(X**2, axis=1)[:, None] + np.sum(X**2, axis=1)[None, :] - 2 * X @ X.T, 0))

    G = np.full((n, n), np.inf)
    for i in range(n):
        idx = np.argsort(dists[i])[1:n_neighbors + 1]
        G[i, idx] = dists[i, idx]
        G[idx, i] = dists[idx, i]
    np.fill_diagonal(G, 0)

    G = shortest_path(G, directed=False)
    G = np.where(np.isfinite(G), G, np.max(G[np.isfinite(G)]) * 2)

    G_sq = G**2
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ G_sq @ J
    eigvals, eigvecs = np.linalg.eigh(B)
    idx = np.argsort(eigvals)[::-1][:n_components]
    return eigvecs[:, idx] * np.sqrt(np.maximum(eigvals[idx], 0))

def lle(X, n_components=2, n_neighbors=10):
    n, d = X.shape
    dists = np.sum(X**2, axis=1)[:, None] + np.sum(X**2, axis=1)[None, :] - 2 * X @ X.T
    W = np.zeros((n, n))

    for i in range(n):
        idx = np.argsort(dists[i])[1:n_neighbors + 1]
        Z = X[idx] - X[i]
        C = Z @ Z.T + 1e-3 * np.eye(n_neighbors)
        w = np.linalg.solve(C, np.ones(n_neighbors))
        w = w / w.sum()
        W[i, idx] = w

    M = (np.eye(n) - W).T @ (np.eye(n) - W)
    eigvals, eigvecs = np.linalg.eigh(M)
    return eigvecs[:, 1:n_components + 1]

def evaluate_manifold(X, n_neighbors=10):
    Y_iso = isomap(X, n_components=2, n_neighbors=n_neighbors)
    Y_lle = lle(X, n_components=2, n_neighbors=n_neighbors)
    return Y_iso, Y_lle

if __name__ == "__main__":
    X, t = make_swiss_roll(n_samples=200, noise=0.1, random_state=42)

    print("=== Manifold Learning: Isomap & LLE ===")
    Y_iso, Y_lle = evaluate_manifold(X, n_neighbors=10)
    print(f"  Isomap output: {Y_iso.shape}")
    print(f"  LLE output:     {Y_lle.shape}")

    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(2, 4)

    # Original Swiss roll
    ax1 = fig.add_subplot(gs[0, 0], projection='3d')
    ax1.scatter(X[:, 0], X[:, 1], X[:, 2], c=t, cmap='Spectral', s=15, alpha=0.7)
    ax1.set_title("Original Swiss Roll")

    # Isomap
    ax2 = fig.add_subplot(gs[0, 1])
    sc = ax2.scatter(Y_iso[:, 0], Y_iso[:, 1], c=t, cmap='Spectral', s=20, alpha=0.8)
    ax2.set_title("Isomap (ours)")
    ax2.set_xticks([]); ax2.set_yticks([])

    # LLE
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.scatter(Y_lle[:, 0], Y_lle[:, 1], c=t, cmap='Spectral', s=20, alpha=0.8)
    ax3.set_title("LLE (ours)")
    ax3.set_xticks([]); ax3.set_yticks([])

    # sklearn Isomap
    from sklearn.manifold import Isomap, LocallyLinearEmbedding
    sk_iso = Isomap(n_components=2, n_neighbors=10).fit_transform(X)
    ax4 = fig.add_subplot(gs[0, 3])
    ax4.scatter(sk_iso[:, 0], sk_iso[:, 1], c=t, cmap='Spectral', s=20, alpha=0.8)
    ax4.set_title("Isomap (sklearn)")
    ax4.set_xticks([]); ax4.set_yticks([])

    # Neighbors comparison for Isomap
    for col, n_nb in enumerate([5, 10, 20]):
        ax = fig.add_subplot(gs[1, col])
        Y_i, _ = evaluate_manifold(X, n_neighbors=n_nb)
        ax.scatter(Y_i[:, 0], Y_i[:, 1], c=t, cmap='Spectral', s=15, alpha=0.7)
        ax.set_title(f"Isomap k={n_nb}")
        ax.set_xticks([]); ax.set_yticks([])

    # sklearn LLE
    sk_lle = LocallyLinearEmbedding(n_components=2, n_neighbors=10).fit_transform(X)
    ax6 = fig.add_subplot(gs[1, 3])
    ax6.scatter(sk_lle[:, 0], sk_lle[:, 1], c=t, cmap='Spectral', s=20, alpha=0.8)
    ax6.set_title("LLE (sklearn)")
    ax6.set_xticks([]); ax6.set_yticks([])

    plt.tight_layout()
    plt.savefig("../../assets/phase05/23-manifold.png")
    plt.close()
    print("Figure saved to 23-manifold.png")

    # Comparison metrics
    print("\n=== Comparison with sklearn ===")
    from sklearn.manifold import Isomap, LocallyLinearEmbedding
    from sklearn.metrics import pairwise_distances
    d_original = pairwise_distances(X[:, :2])
    d_iso_ours = pairwise_distances(Y_iso)
    d_iso_sk = pairwise_distances(sk_iso)
    corr_ours = np.corrcoef(d_original.ravel(), d_iso_ours.ravel())[0, 1]
    corr_sk = np.corrcoef(d_original.ravel(), d_iso_sk.ravel())[0, 1]
    print(f"  Isomap distance correlation: ours={corr_ours:.4f}, sklearn={corr_sk:.4f}")

    # Neighbors sensitivity
    print("\n=== Neighbors Sensitivity ===")
    for k in [5, 10, 15, 20, 30]:
        Y_i, _ = evaluate_manifold(X, n_neighbors=k)
        d_iso = pairwise_distances(Y_i)
        corr = np.corrcoef(d_original.ravel(), d_iso.ravel())[0, 1]
        print(f"  k={k:2d}: Isomap dist corr={corr:.4f}")

    # Edge case: fewer points than neighbors
    print("\n=== Edge Cases ===")
    X_small = np.random.randn(5, 3)
    try:
        Y_s = isomap(X_small, n_components=2, n_neighbors=3)
        print(f"  Small data (5pts, k=3): output={Y_s.shape}")
    except Exception as e:
        print(f"  Small data error: {e}")
