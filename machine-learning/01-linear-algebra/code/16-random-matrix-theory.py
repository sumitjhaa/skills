import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def wigner_matrix(n, sigma=1.0):
    """Generate Wigner matrix (GOE)."""
    X = np.random.randn(n, n) * sigma / np.sqrt(n)
    return (X + X.T) / np.sqrt(2)


def semicircle_pdf(x, sigma=1.0):
    """Semicircle law pdf."""
    R = 2 * sigma
    return np.where(np.abs(x) <= R, np.sqrt(R**2 - x**2) / (2 * np.pi * sigma**2), 0)


def sample_covariance(p, n, sigma=1.0):
    """Generate sample covariance matrix."""
    X = np.random.randn(p, n) * sigma
    return X @ X.T / n


def marchenko_pastur_pdf(x, gamma, sigma=1.0):
    """Marchenko-Pastur pdf."""
    a = sigma**2 * (1 - np.sqrt(gamma))**2
    b = sigma**2 * (1 + np.sqrt(gamma))**2
    return np.where((x >= a) & (x <= b),
                    np.sqrt((b - x) * (x - a)) / (2 * np.pi * gamma * sigma**2 * x), 0)


def spiked_covariance(n, p, rho, k=1):
    """Spiked covariance model."""
    X = np.random.randn(p, n) / np.sqrt(n)
    S = X @ X.T

    u = np.random.randn(p)
    u = u / np.linalg.norm(u)
    S += rho * np.outer(u, u)

    return S


def phase_transition_experiment():
    """Demonstrate the phase transition in spiked covariance."""
    n = 500
    p = 200
    gamma = p / n
    threshold = 1 / np.sqrt(gamma)

    rhos = np.linspace(0, 3, 20)
    top_eigs = []

    for rho in rhos:
        S = spiked_covariance(n, p, rho)
        eigvals = np.linalg.eigvalsh(S)
        top_eigs.append(eigvals[-1])

    return rhos, top_eigs, threshold


def main():
    print("=" * 60)
    print("RANDOM MATRIX THEORY")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- Wigner Semicircle Law ---")
    n = 1000
    W = wigner_matrix(n)
    eigvals_wig = np.linalg.eigvalsh(W)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(eigvals_wig, bins=50, density=True, alpha=0.7, label='Empirical')
    x_grid = np.linspace(-2.5, 2.5, 200)
    ax.plot(x_grid, semicircle_pdf(x_grid), 'r-', linewidth=2, label='Semicircle')
    ax.set_xlabel('Eigenvalue')
    ax.set_ylabel('Density')
    ax.set_title(f'Wigner Semicircle Law (n={n})')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()

    print(f"n={n}, max eigenvalue = {eigvals_wig.max():.4f} (expected ~2)")

    print("\n--- Marchenko-Pastur Law ---")
    p, n_mp = 200, 1000
    gamma = p / n_mp
    S = sample_covariance(p, n_mp)
    eigvals_mp = np.linalg.eigvalsh(S)

    print(f"p={p}, n={n_mp}, gamma={gamma:.2f}")
    print(f"Min eigenvalue: {eigvals_mp.min():.4f}, Max: {eigvals_mp.max():.4f}")
    a_mp = (1 - np.sqrt(gamma))**2
    b_mp = (1 + np.sqrt(gamma))**2
    print(f"MP bounds: [{a_mp:.4f}, {b_mp:.4f}]")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(eigvals_mp, bins=50, density=True, alpha=0.7, label='Empirical')
    x_grid = np.linspace(max(0, a_mp - 0.2), b_mp + 0.2, 200)
    ax.plot(x_grid, marchenko_pastur_pdf(x_grid, gamma), 'r-', linewidth=2, label='MP Law')
    ax.set_xlabel('Eigenvalue')
    ax.set_ylabel('Density')
    ax.set_title(f'Marchenko-Pastur Law (p={p}, n={n_mp})')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()

    print("\n--- Spiked Covariance and Phase Transition ---")
    rhos, top_eigs, threshold = phase_transition_experiment()
    print(f"Phase transition threshold (1/sqrt(gamma)): {threshold:.4f}")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(rhos, top_eigs, 'bo-', label='Largest eigenvalue')
    ax.axvline(x=threshold, color='r', linestyle='--', label=f'Threshold = {threshold:.2f}')
    ax.set_xlabel('Signal strength rho')
    ax.set_ylabel('Largest eigenvalue')
    ax.set_title('Phase Transition in Spiked Covariance Model')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()

    print("\n--- Tracy-Widom Distribution (Top Eigenvalue) ---")
    n_trials = 200
    n_tw = 100
    scaled_max = []

    for _ in range(n_trials):
        W = wigner_matrix(n_tw)
        eigvals = np.linalg.eigvalsh(W)
        lam_max = eigvals[-1]
        scaled = (lam_max - 2) * n_tw**(2/3)
        scaled_max.append(scaled)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(scaled_max, bins=30, density=True, alpha=0.7, label='Empirical')
    x_grid = np.linspace(min(scaled_max), max(scaled_max), 200)
    ax.set_xlabel('Scaled largest eigenvalue')
    ax.set_ylabel('Density')
    ax.set_title('Tracy-Widom Distribution (Top Eigenvalue Fluctuations)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()

    print(f"Mean of scaled max: {np.mean(scaled_max):.4f} (TW_1 mean ~ -1.21)")
    print(f"Std of scaled max: {np.std(scaled_max):.4f}")

    print("\n--- Eigenvalue Spacing Distribution ---")
    spacings = np.diff(np.sort(eigvals_wig)) * n * np.pi / 2
    spacings = spacings[spacings < 5]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(spacings, bins=40, density=True, alpha=0.7, label='Empirical')
    x_grid = np.linspace(0, 5, 200)
    ax.plot(x_grid, (np.pi / 2) * x_grid * np.exp(-np.pi * x_grid**2 / 4),
            'r-', linewidth=2, label='Wigner surmise')
    ax.set_xlabel('Spacing (unfolded)')
    ax.set_ylabel('Density')
    ax.set_title('Eigenvalue Spacing Distribution (GOE)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()


if __name__ == "__main__":
    main()
