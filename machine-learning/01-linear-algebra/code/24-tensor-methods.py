import numpy as np
import matplotlib.pyplot as plt


def cp_als_regression(X_list, y, rank, lr=0.01, max_iter=200):
    """Tensor regression using CP decomposition."""
    I, J, K = X_list[0].shape

    A = np.random.randn(I, rank) * 0.01
    B = np.random.randn(J, rank) * 0.01
    C = np.random.randn(K, rank) * 0.01
    w = np.random.randn(rank)
    b = 0.0
    losses = []

    for it in range(max_iter):
        y_pred = np.zeros(len(X_list))
        for t, X in enumerate(X_list):
            pred = b
            for r in range(rank):
                pred += w[r] * np.tensordot(X, np.tensordot(A[:, r],
                            np.tensordot(B[:, r], C[:, r], axes=0), axes=0), axes=3)
            y_pred[t] = pred

        loss = np.mean((y - y_pred) ** 2)
        losses.append(loss)

        grad = -2 * (y - y_pred) / len(X_list)

        for t, X in enumerate(X_list):
            for r in range(rank):
                A[:, r] -= lr * grad[t] * w[r] * np.tensordot(
                    X, np.tensordot(B[:, r], C[:, r], axes=0), axes=([1, 2], [0, 1]))
                B[:, r] -= lr * grad[t] * w[r] * np.tensordot(
                    X, np.tensordot(A[:, r], C[:, r], axes=0), axes=([0, 2], [0, 1]))
                C[:, r] -= lr * grad[t] * w[r] * np.tensordot(
                    X, np.tensordot(A[:, r], B[:, r], axes=0), axes=([0, 1], [0, 1]))
                w[r] -= lr * grad[t] * np.tensordot(X, np.tensordot(
                    A[:, r], np.tensordot(B[:, r], C[:, r], axes=0), axes=0), axes=3)

        b -= lr * np.mean(grad)

    return A, B, C, w, b, losses


def tensor_completion_cp(X_obs, mask, rank, max_iter=200, tol=1e-6):
    """Tensor completion via CP decomposition."""
    I, J, K = X_obs.shape
    A = np.random.randn(I, rank) * 0.01
    B = np.random.randn(J, rank) * 0.01
    C = np.random.randn(K, rank) * 0.01
    errors = []

    for it in range(max_iter):
        X_recon = np.zeros((I, J, K))
        for r in range(rank):
            X_recon += np.tensordot(A[:, r], np.tensordot(B[:, r], C[:, r], axes=0), axes=0)

        err = np.linalg.norm((X_recon - X_obs)[mask]) / np.linalg.norm(X_obs[mask])
        errors.append(err)

        if it > 0 and abs(errors[-2] - err) < tol:
            break

        grad = 2 * (X_recon - X_obs)
        grad[~mask] = 0

        lr = 0.01
        for r in range(rank):
            BC = np.tensordot(B[:, r], C[:, r], axes=0)
            A[:, r] -= lr * np.tensordot(grad, BC, axes=([1, 2], [0, 1]))

            AC = np.tensordot(A[:, r], C[:, r], axes=0)
            B[:, r] -= lr * np.tensordot(grad, AC, axes=([0, 2], [0, 1]))

            AB = np.tensordot(A[:, r], B[:, r], axes=0)
            C[:, r] -= lr * np.tensordot(grad, AB, axes=([0, 1], [0, 1]))

    X_completed = np.zeros((I, J, K))
    for r in range(rank):
        X_completed += np.tensordot(A[:, r], np.tensordot(B[:, r], C[:, r], axes=0), axes=0)

    return X_completed, errors, A, B, C


def main():
    print("=" * 60)
    print("TENSOR METHODS FOR ML")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- Tensor Regression ---")
    I, J, K, rank, n_samples = 5, 4, 3, 3, 50

    A_true = np.random.randn(I, rank)
    B_true = np.random.randn(J, rank)
    C_true = np.random.randn(K, rank)
    w_true = np.random.randn(rank)
    b_true = 0.5

    X_list = []
    y = np.zeros(n_samples)
    for t in range(n_samples):
        X = np.random.randn(I, J, K)
        X_list.append(X)
        pred = b_true
        for r in range(rank):
            pred += w_true[r] * np.tensordot(X, np.tensordot(
                A_true[:, r], np.tensordot(B_true[:, r], C_true[:, r], axes=0), axes=0), axes=3)
        y[t] = pred + 0.1 * np.random.randn()

    A, B, C, w, b, losses = cp_als_regression(X_list, y, rank, lr=0.01, max_iter=200)

    y_pred = np.zeros(n_samples)
    for t, X in enumerate(X_list):
        pred = b
        for r in range(rank):
            pred += w[r] * np.tensordot(X, np.tensordot(
                A[:, r], np.tensordot(B[:, r], C[:, r], axes=0), axes=0), axes=3)
        y_pred[t] = pred

    print(f"Final loss: {losses[-1]:.4f}")
    print(f"R^2: {1 - np.sum((y - y_pred)**2) / np.sum((y - y.mean())**2):.4f}")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.semilogy(losses)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('MSE Loss')
    ax.set_title('Tensor Regression Convergence')
    ax.grid(True, alpha=0.3)
    plt.show()

    print("\n--- Tensor Completion ---")
    I_c, J_c, K_c, rank_c = 8, 6, 4, 2

    A_true_c = np.random.randn(I_c, rank_c)
    B_true_c = np.random.randn(J_c, rank_c)
    C_true_c = np.random.randn(K_c, rank_c)
    X_full = np.zeros((I_c, J_c, K_c))
    for r in range(rank_c):
        X_full += np.tensordot(A_true_c[:, r], np.tensordot(
            B_true_c[:, r], C_true_c[:, r], axes=0), axes=0)

    obs_ratio = 0.3
    mask = np.random.rand(I_c, J_c, K_c) < obs_ratio
    X_obs = np.zeros_like(X_full)
    X_obs[mask] = X_full[mask]

    print(f"Tensor shape: {X_full.shape}, rank={rank_c}, observed={obs_ratio*100:.0f}%")
    print(f"Observed entries: {mask.sum()} / {X_full.size}")

    X_completed, comp_errors, A_c, B_c, C_c = tensor_completion_cp(X_obs, mask, rank_c)

    comp_err = np.linalg.norm(X_completed - X_full) / np.linalg.norm(X_full)
    obs_err = np.linalg.norm((X_completed - X_full)[mask]) / np.linalg.norm(X_full[mask])
    print(f"Completion error: {comp_err:.4f}")
    print(f"Observed error:   {obs_err:.4f}")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.semilogy(comp_errors)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Relative Error')
    ax.set_title('Tensor Completion via CP')
    ax.grid(True, alpha=0.3)
    plt.show()

    print("\n--- Comparison: Tensor vs Matrix Completion ---")
    X_mat = X_full.reshape(I_c, J_c * K_c)
    mask_mat = mask.reshape(I_c, J_c * K_c)
    X_obs_mat = X_obs.reshape(I_c, J_c * K_c)

    U_m, s_m, Vt_m = np.linalg.svd(X_obs_mat, full_matrices=False)
    s_m[rank_c:] = 0
    X_mat_completed = U_m @ np.diag(s_m) @ Vt_m

    mat_err = np.linalg.norm(X_mat_completed - X_mat, 'fro') / np.linalg.norm(X_mat, 'fro')
    print(f"Matrix completion error:  {mat_err:.4f}")
    print(f"Tensor completion error:  {comp_err:.4f}")
    print(f"Tensor outperforms matrix: {comp_err < mat_err}")

    print("\n--- Missing Ratio Sensitivity ---")
    for obs_r in [0.1, 0.2, 0.3, 0.4, 0.5, 0.7]:
        mask_r = np.random.rand(I_c, J_c, K_c) < obs_r
        X_obs_r = np.zeros_like(X_full)
        X_obs_r[mask_r] = X_full[mask_r]
        X_comp_r, _, _, _, _ = tensor_completion_cp(X_obs_r, mask_r, rank_c, max_iter=150)
        err_r = np.linalg.norm(X_comp_r - X_full) / np.linalg.norm(X_full)
        print(f"  Observed {obs_r*100:.0f}%: error = {err_r:.4f}")


if __name__ == "__main__":
    main()
