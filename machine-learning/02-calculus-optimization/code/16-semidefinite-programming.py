import numpy as np
from scipy.linalg import eigh
import matplotlib.pyplot as plt

def sdp_relaxation_maxcut(W):
    """Goemans-Williamson SDP relaxation for Max-Cut."""
    n = W.shape[0]
    D = np.diag(np.sum(W, axis=1))
    L = D - W
    eigvals, eigvecs = eigh(L)

    try:
        L_sqrt = eigvecs @ np.diag(np.sqrt(np.maximum(eigvals[-1] - eigvals, 0))) @ eigvecs.T
    except:
        L_sqrt = eigvecs @ np.diag(np.sqrt(np.maximum(1e-8 * np.ones_like(eigvals), 0))) @ eigvecs.T
    vmin = eigvecs[:, -1]
    X_sdp = np.outer(vmin, vmin)

    return X_sdp

def main():
    print("=" * 60)
    print("SEMIDEFINITE PROGRAMMING")
    print("=" * 60)

    print("\n--- Minimum Eigenvalue via SDP ---")
    A = np.array([[3, 1], [1, 2]])
    eigvals = eigh(A, eigvals_only=True)
    print(f"Matrix A:\n{A}")
    print(f"Eigenvalues: {eigvals}")
    print(f"Minimum eigenvalue: {eigvals[0]:.6f}")

    print(f"\n--- SDP: Max-Cut Relaxation ---")
    W = np.array([
        [0, 1, 2, 0],
        [1, 0, 1, 1],
        [2, 1, 0, 2],
        [0, 1, 2, 0]
    ])
    print(f"Graph (weight matrix):\n{W}")

    X_sdp = sdp_relaxation_maxcut(W)
    print(f"SDP solution X:\n{X_sdp}")

    print(f"\n--- Random Rounding for Max-Cut ---")
    np.random.seed(42)
    n_trials = 1000
    best_cut = -np.inf
    for _ in range(n_trials):
        r = np.random.randn(W.shape[0])
        y = np.sign(X_sdp @ r)
        cut_val = 0.25 * np.sum(W * (1 - np.outer(y, y)))
        if cut_val > best_cut:
            best_cut = cut_val
            best_y = y

    print(f"Best cut value found: {best_cut:.2f}")
    print(f"Cut assignment: {best_y}")

    print(f"\n--- Positive Semidefinite Constraint Check ---")
    def is_psd(X, tol=1e-10):
        return np.all(eigh(X, eigvals_only=True) >= -tol)

    X_psd = np.array([[2, 1], [1, 2]])
    X_not_psd = np.array([[-1, 0], [0, 2]])
    print(f"  [[2, 1], [1, 2]] is PSD: {is_psd(X_psd)}")
    print(f"  [[-1, 0], [0, 2]] is PSD: {is_psd(X_not_psd)}")

    print(f"\n--- SDP for Sensor Network Localization ---")
    np.random.seed(42)
    n_sensors = 5
    n_anchors = 2
    true_positions = np.random.randn(n_sensors, 2)
    anchor_positions = np.random.randn(n_anchors, 2)
    mask = np.random.rand(n_sensors, n_sensors) < 0.5
    mask = mask | mask.T
    np.fill_diagonal(mask, False)

    distances = np.zeros((n_sensors + n_anchors, n_sensors + n_anchors))
    all_pos = np.vstack([anchor_positions, true_positions])
    for i in range(n_sensors + n_anchors):
        for j in range(i+1, n_sensors + n_anchors):
            d = np.linalg.norm(all_pos[i] - all_pos[j])
            distances[i, j] = d
            distances[j, i] = d

    # SDP relaxation for localization
    Y = np.eye(n_sensors)
    Z = true_positions @ true_positions.T
    print(f"Sensor sensor localization problem:")
    print(f"  True positions shape: {true_positions.shape}")
    print(f"  Distance matrix shape: {distances.shape}")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    im1 = axes[0].matshow(X_sdp, cmap='viridis')
    axes[0].set_title('SDP Solution X for Max-Cut')
    plt.colorbar(im1, ax=axes[0])

    im2 = axes[1].matshow(W, cmap='viridis')
    axes[1].set_title('Original Weight Matrix')
    plt.colorbar(im2, ax=axes[1])

    plt.tight_layout()
    plt.savefig('../../assets/phase02/16_semidefinite_programming.png', dpi=100)
    print(f"\nPlot saved to /tmp/16_semidefinite_programming.png")

if __name__ == "__main__":
    main()
