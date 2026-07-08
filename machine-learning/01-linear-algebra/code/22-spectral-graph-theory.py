import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csgraph


def graph_fourier_transform(L, x):
    """Graph Fourier Transform: x_hat = U^T x."""
    eigvals, U = np.linalg.eigh(L)
    x_hat = U.T @ x
    return x_hat, eigvals, U


def inverse_graph_fourier_transform(x_hat, U):
    """Inverse GFT: x = U x_hat."""
    return U @ x_hat


def spectral_filter(L, x, filter_func):
    """Apply spectral filter g(Lambda) to signal x."""
    eigvals, U = np.linalg.eigh(L)
    x_hat = U.T @ x
    x_filtered = U @ (filter_func(eigvals) * x_hat)
    return x_filtered


def low_pass_filter(eigvals, cutoff=0.5):
    """Ideal low-pass filter."""
    return (eigvals / eigvals.max() <= cutoff).astype(float)


def high_pass_filter(eigvals, cutoff=0.5):
    """Ideal high-pass filter."""
    return (eigvals / eigvals.max() > cutoff).astype(float)


def chebyshev_polynomials(x, K):
    """Compute Chebyshev polynomials T_0(x) through T_K(x)."""
    T = [np.ones_like(x), x.copy()]
    for k in range(2, K + 1):
        T.append(2 * x * T[k - 1] - T[k - 2])
    return T


def chebyshev_filter(L, x, coeffs):
    """Apply Chebyshev polynomial filter to x."""
    eigvals, U = np.linalg.eigh(L)
    lambda_max = eigvals.max()
    x_tilde = x / lambda_max if lambda_max > 0 else x

    T = chebyshev_polynomials(L / lambda_max - np.eye(L.shape[0]), len(coeffs) - 1)

    y = coeffs[0] * x
    for k in range(1, len(coeffs)):
        y += coeffs[k] * (T[k] @ x)

    return y


def path_graph(n):
    """Create path graph Laplacian."""
    A = np.zeros((n, n))
    for i in range(n - 1):
        A[i, i + 1] = A[i + 1, i] = 1
    D = np.diag(A.sum(axis=1))
    return D - A


def random_graph(n, p=0.3):
    """Create random graph Laplacian."""
    A = (np.random.rand(n, n) < p).astype(float)
    A = np.triu(A, 1) + np.triu(A, 1).T
    D = np.diag(A.sum(axis=1))
    return D - A


def main():
    print("=" * 60)
    print("SPECTRAL GRAPH THEORY")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- Graph Fourier Transform ---")
    n_nodes = 20
    L = path_graph(n_nodes)

    x = np.zeros(n_nodes)
    x[n_nodes // 2] = 1.0

    x_hat, eigvals, U = graph_fourier_transform(L, x)
    x_recovered = inverse_graph_fourier_transform(x_hat, U)

    print(f"Signal: impulse at node {n_nodes // 2}")
    print(f"GFT coefficients (first 5): {np.round(x_hat[:5], 4)}")
    print(f"Recovery error: {np.linalg.norm(x - x_recovered):.2e}")

    print("\n--- Spectral Filtering ---")
    x_smooth = np.sin(np.linspace(0, 4 * np.pi, n_nodes))
    x_noisy = x_smooth + 0.5 * np.random.randn(n_nodes)

    x_low = spectral_filter(L, x_noisy, lambda ev: low_pass_filter(ev, cutoff=0.3))
    x_high = spectral_filter(L, x_noisy, lambda ev: high_pass_filter(ev, cutoff=0.3))

    fig, axes = plt.subplots(2, 2, figsize=(14, 8))

    axes[0, 0].plot(x_smooth, 'b-', label='Clean')
    axes[0, 0].plot(x_noisy, 'r-', alpha=0.5, label='Noisy')
    axes[0, 0].set_title('Graph Signal: Clean vs Noisy')
    axes[0, 0].legend()

    axes[0, 1].plot(x_low, 'g-', label='Low-pass filtered')
    axes[0, 1].set_title('Low-Pass Filtered Signal')
    axes[0, 1].legend()

    axes[1, 0].plot(x_high, 'm-', label='High-pass filtered')
    axes[1, 0].set_title('High-Pass Filtered Signal')
    axes[1, 0].legend()

    axes[1, 1].plot(eigvals, 'bo-', markersize=4)
    axes[1, 1].axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    axes[1, 1].set_title('Laplacian Spectrum')
    axes[1, 1].set_xlabel('Index')
    axes[1, 1].set_ylabel('Eigenvalue')

    for ax in axes.flat:
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("\n--- Chebyshev Polynomial Filter ---")
    L_rand = random_graph(15, 0.4)
    x_rand = np.random.randn(15)

    coeffs = [0.5, 0.3, 0.1, -0.05]
    x_cheb = chebyshev_filter(L_rand, x_rand, coeffs)

    eigvals_rand, U_rand = np.linalg.eigh(L_rand)
    lambda_max = eigvals_rand.max()
    filter_vals = coeffs[0] * np.ones_like(eigvals_rand)
    for k in range(1, len(coeffs)):
        T_k = chebyshev_polynomials(eigvals_rand / lambda_max, k)[k]
        filter_vals += coeffs[k] * T_k

    x_exact = U_rand @ (filter_vals * (U_rand.T @ x_rand))
    print(f"Chebyshev vs exact filter error: {np.linalg.norm(x_cheb - x_exact):.2e}")

    print("\n--- Graph Fourier Basis Visualization ---")
    fig, ax = plt.subplots(figsize=(12, 6))
    for i in range(min(4, n_nodes)):
        ax.plot(U[:, i], label=f'Eigenvector {i+1} (lambda={eigvals[i]:.2f})')
    ax.set_xlabel('Node index')
    ax.set_ylabel('Eigenvector value')
    ax.set_title('First 4 Laplacian Eigenvectors (Path Graph)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()

    print("\n--- Spectrum of Different Graphs ---")
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    names = ['Path (10)', 'Complete (10)', 'Random (10, p=0.4)']
    graphs = [path_graph(10),
              np.eye(10) * 9 - np.ones((10, 10)) + np.eye(10) * 10,
              random_graph(10, 0.4)]

    for ax, L_g, name in zip(axes, graphs, names):
        ev = np.linalg.eigvalsh(L_g)
        ax.bar(range(len(ev)), ev)
        ax.set_title(f'{name}')
        ax.set_xlabel('Index')
        ax.set_ylabel('Eigenvalue')
        ax.grid(True, alpha=0.3)

    plt.suptitle('Laplacian Spectra of Different Graphs')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
