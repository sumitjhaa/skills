import numpy as np
import matplotlib.pyplot as plt


def cp_als_simple(X, rank, max_iter=200, tol=1e-8):
    """Simple CP-ALS for tensor completion."""
    I, J, K = X.shape
    A = np.random.randn(I, rank) * 0.01
    B = np.random.randn(J, rank) * 0.01
    C = np.random.randn(K, rank) * 0.01
    errors = []

    for it in range(max_iter):
        A = np.linalg.lstsq((B.T @ B) * (C.T @ C),
            np.tensordot(X, B, axes=([1], [0])).reshape(I, J*K) @ np.kron(C, B),
            rcond=None)[0].reshape(I, rank)
        B = np.linalg.lstsq((A.T @ A) * (C.T @ C),
            np.tensordot(X.transpose(1, 0, 2), A, axes=([1], [0])).reshape(J, I*K) @ np.kron(C, A),
            rcond=None)[0].reshape(J, rank)
        C = np.linalg.lstsq((A.T @ A) * (B.T @ B),
            np.tensordot(X.transpose(2, 0, 1), A, axes=([1], [0])).reshape(K, I*J) @ np.kron(B, A),
            rcond=None)[0].reshape(K, rank)

        X_recon = np.zeros((I, J, K))
        for r in range(rank):
            X_recon += np.tensordot(A[:, r], np.tensordot(B[:, r], C[:, r], axes=0), axes=0)

        err = np.linalg.norm(X - X_recon) / np.linalg.norm(X)
        errors.append(err)

        if it > 0 and abs(errors[-2] - err) < tol:
            break

    return A, B, C, errors


def predict_ratings(A, B, C):
    """Predict all ratings from CP factors."""
    I, R = A.shape
    J, _ = B.shape
    K, _ = C.shape
    X = np.zeros((I, J, K))
    for r in range(R):
        X += np.tensordot(A[:, r], np.tensordot(B[:, r], C[:, r], axes=0), axes=0)
    return X


def tensor_collaborative_filtering(X_obs, mask, rank, max_iter=200):
    """Tensor collaborative filtering via CP decomposition."""
    A, B, C, errors = cp_als_simple(X_obs, rank, max_iter=max_iter)
    X_pred = predict_ratings(A, B, C)
    X_pred_completed = X_pred.copy()
    X_pred_completed[mask] = X_obs[mask]
    return X_pred_completed, A, B, C, errors


def matrix_collaborative_filtering(X_mat, mask_mat, rank, max_iter=200):
    """Matrix collaborative filtering for comparison."""
    m, n = X_mat.shape
    U = np.random.randn(m, rank) * 0.01
    V = np.random.randn(n, rank) * 0.01
    errors = []

    for it in range(max_iter):
        U = np.linalg.lstsq(V.T @ V, (X_mat @ V).T, rcond=None)[0].T
        V = np.linalg.lstsq(U.T @ U, (X_mat.T @ U).T, rcond=None)[0].T

        X_pred = U @ V.T
        err = np.linalg.norm((X_pred - X_mat)[mask_mat]) / np.linalg.norm(X_mat[mask_mat])
        errors.append(err)

        if it > 0 and abs(errors[-2] - err) < tol:
            break

    X_completed = U @ V.T
    X_completed[mask_mat] = X_mat[mask_mat]
    return X_completed, errors


def rmse(y_true, y_pred):
    """Root mean squared error."""
    return np.sqrt(np.mean((y_true - y_pred)**2))


def main():
    print("=" * 60)
    print("TENSOR METHODS FOR RECOMMENDATION")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- Synthetic Recommendation Data ---")
    n_users, n_items, n_contexts = 30, 20, 5
    rank = 3

    A_true = np.random.randn(n_users, rank) * 2
    B_true = np.random.randn(n_items, rank) * 2
    C_true = np.random.randn(n_contexts, rank) * 2

    X_true = predict_ratings(A_true, B_true, C_true)
    print(f"Rating tensor shape: {X_true.shape}")
    print(f"Rating range: [{X_true.min():.2f}, {X_true.max():.2f}]")

    obs_ratio = 0.3
    mask = np.random.rand(n_users, n_items, n_contexts) < obs_ratio
    X_obs = np.zeros_like(X_true)
    X_obs[mask] = X_true[mask]
    print(f"Observed entries: {mask.sum()} / {X_true.size} ({obs_ratio*100:.0f}%)")

    print("\n--- Tensor Collaborative Filtering ---")
    rank_cf = 3
    X_pred, A, B, C, errors = tensor_collaborative_filtering(
        X_obs, mask, rank_cf, max_iter=300)

    test_mask = ~mask
    train_rmse = rmse(X_true[mask], X_pred[mask])
    test_rmse = rmse(X_true[test_mask], X_pred[test_mask])
    print(f"Train RMSE: {train_rmse:.4f}")
    print(f"Test RMSE:  {test_rmse:.4f}")
    print(f"Overall completion error: "
          f"{np.linalg.norm(X_pred - X_true) / np.linalg.norm(X_true):.4f}")

    print("\n--- Comparison: Tensor vs Matrix CF ---")
    X_mat = X_true.reshape(n_users, n_items * n_contexts)
    mask_mat = mask.reshape(n_users, n_items * n_contexts)
    X_obs_mat = X_obs.reshape(n_users, n_items * n_contexts)

    X_mat_pred, mat_errors = matrix_collaborative_filtering(
        X_obs_mat, mask_mat, rank_cf, max_iter=300)

    test_mask_mat = ~mask_mat
    test_rmse_mat = rmse(X_mat[test_mask_mat], X_mat_pred[test_mask_mat])
    print(f"Matrix CF test RMSE: {test_rmse_mat:.4f}")
    print(f"Tensor CF test RMSE: {test_rmse:.4f}")
    print(f"Tensor better: {test_rmse < test_rmse_mat}")

    print("\n--- Rank Selection ---")
    for r in [1, 2, 3, 4, 5, 8]:
        _, _, _, _, e_r = tensor_collaborative_filtering(X_obs, mask, r, max_iter=200)
        test_pred = predict_ratings(*cp_als_simple(X_obs, r, max_iter=200)[:-1])
        test_err = rmse(X_true[~mask], test_pred[~mask])
        print(f"  Rank {r}: train_err={e_r[-1]:.4f}, test_rmse={test_err:.4f}")

    print("\n--- Convergence ---")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].semilogy(errors, 'b-', label='Tensor CP')
    axes[0].semilogy(mat_errors, 'r-', label='Matrix')
    axes[0].set_xlabel('Iteration')
    axes[0].set_ylabel('Relative error')
    axes[0].set_title('Convergence: Tensor vs Matrix CF')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    print("\n--- Context Influence Analysis ---")
    context_factors = C
    print(f"Context factors (shape: {context_factors.shape}):")
    for k in range(n_contexts):
        print(f"  Context {k+1}: {np.round(context_factors[k], 3)}")

    context_correlations = np.corrcoef(context_factors.T)
    print(f"\nContext factor correlations:\n{np.round(context_correlations, 3)}")

    print("\n--- Cold-Start (New User) ---")
    new_user_factors = np.random.randn(1, rank_cf) * 0.1
    new_user_preds = predict_ratings(new_user_factors, B, C)[0]
    avg_rating = X_true.mean(axis=0)
    new_user_rmse = rmse(avg_rating, new_user_preds)
    print(f"New user prediction vs global average: RMSE = {new_user_rmse:.4f}")

    print("\n--- Observation Ratio Sensitivity ---")
    for obs_r in [0.1, 0.2, 0.3, 0.4, 0.5, 0.7]:
        mask_r = np.random.rand(n_users, n_items, n_contexts) < obs_r
        X_obs_r = np.zeros_like(X_true)
        X_obs_r[mask_r] = X_true[mask_r]
        _, _, _, _, _ = tensor_collaborative_filtering(X_obs_r, mask_r, rank_cf, max_iter=150)
        X_pred_r = predict_ratings(*cp_als_simple(X_obs_r, rank_cf, max_iter=150)[:-1])
        test_err_r = rmse(X_true[~mask_r], X_pred_r[~mask_r])
        print(f"  Observed {obs_r*100:.0f}%: test RMSE = {test_err_r:.4f}")


if __name__ == "__main__":
    main()
