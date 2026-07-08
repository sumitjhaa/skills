"""t-SNE and UMAP-style embedding from scratch."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs, make_s_curve

def tsne(X, n_components=2, perplexity=30, n_iter=500, lr=200):
    n = X.shape[0]
    dists = np.sum(X**2, axis=1)[:, None] + np.sum(X**2, axis=1)[None, :] - 2 * X @ X.T
    np.fill_diagonal(dists, 0)

    sigma = np.ones(n)
    P = np.zeros((n, n))
    target_entropy = np.log(perplexity)
    for i in range(n):
        sigma_i = sigma[i]
        for _ in range(50):
            p = np.exp(-dists[i] / (2 * sigma_i**2))
            p[i] = 0
            p = p / (p.sum() + 1e-10)
            entropy = -np.sum(p * np.log(p + 1e-15))
            if abs(entropy - target_entropy) < 1e-5:
                break
            sigma_i *= (entropy / target_entropy) ** 0.5
        P[i] = p
    P = (P + P.T) / (2 * n)
    P = np.maximum(P, 1e-12)

    Y = np.random.randn(n, n_components) * 1e-4
    Y_momentum = np.zeros_like(Y)
    kl_history = []

    for iteration in range(n_iter):
        dist_y = np.sum(Y**2, axis=1)[:, None] + np.sum(Y**2, axis=1)[None, :] - 2 * Y @ Y.T
        Q = 1.0 / (1.0 + dist_y)
        np.fill_diagonal(Q, 0)
        Q = Q / (Q.sum() + 1e-10)
        Q = np.maximum(Q, 1e-12)

        PQ_diff = P - Q
        grad = np.zeros_like(Y)
        for i in range(n):
            grad[i] = 4 * np.sum((PQ_diff[i, :, None]) * (Y[i] - Y), axis=0)

        if iteration < 250:
            Y_momentum = 0.5 * Y_momentum - lr * grad
        else:
            Y_momentum = 0.8 * Y_momentum - lr * grad
        Y += Y_momentum
        Y = Y - Y.mean(axis=0)

        kl = np.sum(P * np.log(np.maximum(P, 1e-15) / np.maximum(Q, 1e-15)))
        kl_history.append(kl)

    return Y, kl_history

def umap_simplified(X, n_components=2, n_neighbors=15, n_iter=200, lr=1.0):
    n = X.shape[0]
    X = X.astype(np.float64)
    sq_dists = np.sum(X**2, axis=1)[:, None] + np.sum(X**2, axis=1)[None, :] - 2 * X @ X.T
    dists = np.sqrt(np.maximum(sq_dists, 0))

    sigma = np.ones(n)
    rho = np.zeros(n)
    for i in range(n):
        sorted_d = np.sort(dists[i])
        rho[i] = sorted_d[1]
        idx = min(n_neighbors, n - 1)
        sigma[i] = max(sorted_d[idx], 1e-10)

    P = np.zeros((n, n))
    for i in range(n):
        p = np.exp(-np.maximum(dists[i] - rho[i], 0) / sigma[i])
        p[i] = 0
        P[i] = p
    P = (P + P.T) - P * P.T
    P = np.maximum(P, 1e-12)

    Y = np.random.randn(n, n_components).astype(np.float64) * 0.01

    for iteration in range(n_iter):
        sq = np.sum(Y**2, axis=1)[:, None] + np.sum(Y**2, axis=1)[None, :] - 2 * Y @ Y.T
        dist_y = np.sqrt(np.maximum(sq, 0))
        Q = 1.0 / (1.0 + dist_y**2)
        np.fill_diagonal(Q, 0)

        grad = 4 * (P - Q)[:, :, None] * (Y[None, :, :] - Y[:, None, :])
        if np.isnan(grad).any() or np.isinf(grad).any():
            break
        grad = grad.sum(axis=1)
        lr_step = lr * (0.9 ** (iteration // 50))
        Y -= lr_step * grad
        Y = Y - Y.mean(axis=0)

    return Y

if __name__ == "__main__":
    np.random.seed(42)

    # Dataset: S-curve with 2 blobs in high-d
    X, color = make_s_curve(n_samples=300, noise=0.1, random_state=42)
    color = color[:, 0] if color.ndim > 1 else color

    print("Running t-SNE...")
    Y_tsne, kl_hist = tsne(X, n_components=2, perplexity=30, n_iter=300)
    print(f"  t-SNE output: {Y_tsne.shape}, final KL={kl_hist[-1]:.4f}")

    print("Running simplified UMAP...")
    Y_umap = umap_simplified(X, n_components=2, n_neighbors=15, n_iter=200)
    print(f"  UMAP output: {Y_umap.shape}")

    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(2, 4)

    # t-SNE scatter
    ax1 = fig.add_subplot(gs[0, 0])
    sc1 = ax1.scatter(Y_tsne[:, 0], Y_tsne[:, 1], c=color, cmap='Spectral', s=20, alpha=0.8)
    ax1.set_title("t-SNE (ours)")
    ax1.set_xticks([]); ax1.set_yticks([])

    # UMAP scatter
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.scatter(Y_umap[:, 0], Y_umap[:, 1], c=color, cmap='Spectral', s=20, alpha=0.8)
    ax2.set_title("UMAP-simplified (ours)")
    ax2.set_xticks([]); ax2.set_yticks([])

    # sklearn t-SNE
    from sklearn.manifold import TSNE
    sk_tsne = TSNE(n_components=2, perplexity=30, random_state=42).fit_transform(X)
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.scatter(sk_tsne[:, 0], sk_tsne[:, 1], c=color, cmap='Spectral', s=20, alpha=0.8)
    ax3.set_title("t-SNE (sklearn)")
    ax3.set_xticks([]); ax3.set_yticks([])

    # 3D original
    ax4 = fig.add_subplot(gs[0, 3], projection='3d')
    ax4.scatter(X[:, 0], X[:, 1], X[:, 2], c=color, cmap='Spectral', s=15, alpha=0.7)
    ax4.set_title("Original 3D S-curve")

    # KL divergence
    ax5 = fig.add_subplot(gs[1, 0])
    ax5.plot(kl_hist)
    ax5.set_xlabel("Iteration")
    ax5.set_ylabel("KL(Q||P)")
    ax5.set_title("t-SNE KL Divergence")
    ax5.grid(True, alpha=0.3)

    # Perplexity comparison
    for ppx, ax in zip([5, 15, 30], [gs[1, 1], gs[1, 2], gs[1, 3]]):
        Yp, _ = tsne(X, n_components=2, perplexity=ppx, n_iter=200)
        ax_obj = fig.add_subplot(ax)
        ax_obj.scatter(Yp[:, 0], Yp[:, 1], c=color, cmap='Spectral', s=15, alpha=0.7)
        ax_obj.set_title(f"t-SNE ppx={ppx}")
        ax_obj.set_xticks([]); ax_obj.set_yticks([])

    plt.tight_layout()
    plt.savefig("../../assets/phase05/22-tsne-umap.png")
    plt.close()
    print("Figure saved to 22-tsne-umap.png")

    # Convergence analysis
    print("\n=== Convergence Analysis ===")
    for ppx in [5, 15, 30]:
        _, kl = tsne(X, n_components=2, perplexity=ppx, n_iter=200)
        print(f"  perplexity={ppx}: final KL={kl[-1]:.4f}")

    # Edge case: fewer points than perplexity
    print("\n=== Edge Cases ===")
    X_small = np.random.randn(10, 5)
    Y_small, _ = tsne(X_small, n_components=2, perplexity=5, n_iter=100)
    print(f"  Small data (10 pts): output shape={Y_small.shape}")
