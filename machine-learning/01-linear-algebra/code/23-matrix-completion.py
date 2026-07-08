import numpy as np
import matplotlib.pyplot as plt


def svt(A_obs, mask, tau, delta=1.0, max_iter=500, tol=1e-7):
    """Singular Value Thresholding for matrix completion."""
    X = np.zeros_like(A_obs, dtype=float)
    errors = []

    for it in range(max_iter):
        U, s, Vt = np.linalg.svd(X, full_matrices=False)
        s_shrunk = np.maximum(s - tau, 0)
        X_new = U @ np.diag(s_shrunk) @ Vt

        X_new[mask] += delta * (A_obs[mask] - X_new[mask])

        change = np.linalg.norm(X_new - X, 'fro') / max(1, np.linalg.norm(X, 'fro'))
        errors.append(change)

        if change < tol:
            break
        X = X_new

    return X, errors


def riemannian_completion(A_obs, mask, rank, lr=0.01, max_iter=500, tol=1e-7):
    """Matrix completion via Riemannian optimization on low-rank manifold."""
    m, n = A_obs.shape
    U = np.random.randn(m, rank) * 0.01
    V = np.random.randn(n, rank) * 0.01
    errors = []

    for it in range(max_iter):
        X = U @ V.T
        grad = np.zeros((m, n))
        grad[mask] = X[mask] - A_obs[mask]

        grad_U = grad @ V
        grad_V = grad.T @ U

        U_new = U - lr * grad_U
        V_new = V - lr * grad_V

        change = np.linalg.norm(U_new @ V_new.T - X, 'fro') / max(1, np.linalg.norm(X, 'fro'))
        errors.append(change)

        if change < tol:
            break
        U, V = U_new, V_new

    return U @ V.T, errors


def nuclear_norm(A):
    """Compute nuclear norm."""
    return np.sum(np.linalg.svd(A, compute_uv=False))


def phase_transition(m, n, rank, obs_ratios, n_trials=5):
    """Phase transition: success rate vs observation ratio."""
    success_rates = []

    for obs_ratio in obs_ratios:
        successes = 0
        for _ in range(n_trials):
            U = np.random.randn(m, rank)
            V = np.random.randn(rank, n)
            A_true = U @ V

            mask = np.random.rand(m, n) < obs_ratio
            A_obs = np.zeros((m, n))
            A_obs[mask] = A_true[mask]

            X_completed, _ = svt(A_obs, mask, tau=1.0, max_iter=200)

            err = np.linalg.norm(X_completed - A_true, 'fro') / np.linalg.norm(A_true, 'fro')
            if err < 0.1:
                successes += 1

        success_rates.append(successes / n_trials)

    return success_rates


def main():
    print("=" * 60)
    print("MATRIX COMPLETION - SVT and Riemannian")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- Basic Matrix Completion ---")
    m, n, rank = 20, 20, 3
    U = np.random.randn(m, rank)
    V = np.random.randn(rank, n)
    A_true = U @ V

    obs_ratio = 0.4
    mask = np.random.rand(m, n) < obs_ratio
    A_obs = np.zeros((m, n))
    A_obs[mask] = A_true[mask]

    print(f"Matrix size: {m}x{n}, rank={rank}, observed={obs_ratio*100:.0f}%")
    print(f"Observed entries: {mask.sum()} / {m*n}")

    X_svt, errors_svt = svt(A_obs, mask, tau=1.0, max_iter=500)
    svt_err = np.linalg.norm(X_svt - A_true, 'fro') / np.linalg.norm(A_true, 'fro')
    print(f"SVT completion error: {svt_err:.4f}")

    X_riem, errors_riem = riemannian_completion(A_obs, mask, rank, max_iter=1000)
    riem_err = np.linalg.norm(X_riem - A_true, 'fro') / np.linalg.norm(A_true, 'fro')
    print(f"Riemannian completion error: {riem_err:.4f}")

    print("\n--- Convergence Comparison ---")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].semilogy(errors_svt, 'b-', label='SVT')
    axes[0].semilogy(errors_riem, 'r-', label='Riemannian')
    axes[0].set_xlabel('Iteration')
    axes[0].set_ylabel('Relative change')
    axes[0].set_title('Convergence')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.imshow(np.abs(X_svt - A_true), cmap='Reds')
    ax.set_title('|Completed - True|')
    plt.tight_layout()
    plt.show()

    print("\n--- Effect of Observation Ratio ---")
    for obs_ratio_test in [0.2, 0.3, 0.4, 0.5, 0.6]:
        mask_t = np.random.rand(m, n) < obs_ratio_test
        A_obs_t = np.zeros((m, n))
        A_obs_t[mask_t] = A_true[mask_t]
        X_t, _ = svt(A_obs_t, mask_t, tau=1.0, max_iter=300)
        err_t = np.linalg.norm(X_t - A_true, 'fro') / np.linalg.norm(A_true, 'fro')
        print(f"  Observed {obs_ratio_test*100:.0f}%: error = {err_t:.4f}")

    print("\n--- Phase Transition ---")
    obs_ratios = np.linspace(0.1, 0.8, 8)
    rates = phase_transition(30, 30, 5, obs_ratios, n_trials=3)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(obs_ratios, rates, 'bo-', linewidth=2)
    ax.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='50% success')
    ax.set_xlabel('Observation ratio')
    ax.set_ylabel('Success rate')
    ax.set_title('Phase Transition: Matrix Completion')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()

    print("\n--- Nuclear Norm Behavior ---")
    nuc_true = nuclear_norm(A_true)
    nuc_completed_svt = nuclear_norm(X_svt)
    nuc_completed_riem = nuclear_norm(X_riem)
    print(f"Nuclear norm: true={nuc_true:.2f}, SVT={nuc_completed_svt:.2f}, "
          f"Riemannian={nuc_completed_riem:.2f}")

    print("\n--- Noise Robustness ---")
    for noise_level in [0.01, 0.05, 0.1, 0.2]:
        A_noisy = A_true + noise_level * np.random.randn(m, n)
        A_obs_noisy = np.zeros((m, n))
        A_obs_noisy[mask] = A_noisy[mask]
        X_noisy, _ = svt(A_obs_noisy, mask, tau=1.0, max_iter=300)
        err_noisy = np.linalg.norm(X_noisy - A_true, 'fro') / np.linalg.norm(A_true, 'fro')
        print(f"  Noise {noise_level}: error = {err_noisy:.4f}")


if __name__ == "__main__":
    main()
