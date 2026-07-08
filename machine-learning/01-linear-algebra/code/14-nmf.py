import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import nnls


def nmf_multiplicative(V, k, max_iter=500, tol=1e-8):
    """NMF via multiplicative update rules."""
    m, n = V.shape
    W = np.abs(np.random.randn(m, k)) + 0.01
    H = np.abs(np.random.randn(k, n)) + 0.01

    errors = []

    for i in range(max_iter):
        H *= (W.T @ V) / (W.T @ (W @ H) + 1e-10)
        W *= (V @ H.T) / (W @ (H @ H.T) + 1e-10)

        err = np.linalg.norm(V - W @ H, 'fro')
        errors.append(err)

        if i > 0 and abs(errors[-2] - err) / max(1, err) < tol:
            break

    return W, H, errors


def nmf_als(V, k, max_iter=200):
    """NMF via alternating least squares."""
    m, n = V.shape
    W = np.abs(np.random.randn(m, k)) + 0.01
    H = np.abs(np.random.randn(k, n)) + 0.01

    errors = []

    for it in range(max_iter):
        for i in range(m):
            sol, _ = nnls(H.T, V[i])
            W[i] = np.maximum(sol, 0)

        for j in range(n):
            sol, _ = nnls(W, V[:, j])
            H[:, j] = np.maximum(sol, 0)

        err = np.linalg.norm(V - W @ H, 'fro')
        errors.append(err)

    return W, H, errors


def nmf_als_fast(V, k, max_iter=200):
    """ALS with NNLS using the full matrix (faster)."""
    m, n = V.shape
    W = np.abs(np.random.randn(m, k)) + 0.01
    H = np.abs(np.random.randn(k, n)) + 0.01

    for _ in range(max_iter):
        H = np.maximum(
            np.linalg.solve(W.T @ W + 1e-10 * np.eye(k), W.T @ V),
            0)
        W = np.maximum(
            np.linalg.solve(H @ H.T + 1e-10 * np.eye(k), V @ H.T).T,
            0)

    return W, H


def nmf_topic_model(V, k, n_top_words=5):
    """Simple topic modeling via NMF."""
    W, H, errors = nmf_multiplicative(V, k)

    topics = []
    for topic_idx in range(k):
        top_indices = np.argsort(W[:, topic_idx])[-n_top_words:][::-1]
        topics.append(top_indices)

    return W, H, topics, errors


def compare_nmf_algorithms():
    """Compare multiplicative vs ALS NMF."""
    m, n, k = 30, 20, 5
    V = np.abs(np.random.randn(m, n))

    W1, H1, err1 = nmf_multiplicative(V, k)
    W2, H2, err2 = nmf_als(V, k)

    final_err1 = np.linalg.norm(V - W1 @ H1, 'fro')
    final_err2 = np.linalg.norm(V - W2 @ H2, 'fro')

    print(f"Multiplicative final error: {final_err1:.4f}")
    print(f"ALS final error:            {final_err2:.4f}")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(err1, label='Multiplicative')
    ax.plot(err2, label='ALS')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Frobenius Error')
    ax.set_title('NMF Convergence Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()

    return W1, H1, W2, H2


def main():
    print("=" * 60)
    print("NON-NEGATIVE MATRIX FACTORIZATION")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- Basic NMF ---")
    m, n, k = 10, 8, 3
    W_true = np.abs(np.random.randn(m, k))
    H_true = np.abs(np.random.randn(k, n))
    V = W_true @ H_true

    print(f"V shape: {V.shape}, k={k}")
    print(f"V min: {V.min():.4f}, V max: {V.max():.4f}")

    W, H, errors = nmf_multiplicative(V, k)
    final_error = np.linalg.norm(V - W @ H, 'fro')
    print(f"Reconstruction error: {final_error:.4f}")
    print(f"W min: {W.min():.4f}, H min: {H.min():.4f}")
    print(f"All non-negative: {W.min() >= -1e-10 and H.min() >= -1e-10}")

    print("\n--- Multiplicative Updates Convergence ---")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.semilogy(errors)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Frobenius Error')
    ax.set_title('NMF Convergence (Multiplicative Updates)')
    ax.grid(True, alpha=0.3)
    plt.show()

    print("\n--- ALS NMF ---")
    W_als, H_als, err_als = nmf_als(V, k)
    err_als_final = np.linalg.norm(V - W_als @ H_als, 'fro')
    print(f"ALS reconstruction error: {err_als_final:.4f}")

    print("\n--- Comparison: Multiplicative vs ALS ---")
    compare_nmf_algorithms()

    print("\n--- Topic Modeling Demo ---")
    n_docs = 10
    n_terms = 50
    n_topics = 3

    V_docs = np.abs(np.random.randn(n_terms, n_docs))
    W_docs, H_docs, topics, _ = nmf_topic_model(V_docs, n_topics, n_top_words=5)

    print("Learned topics (top term indices per topic):")
    for i, topic in enumerate(topics):
        print(f"  Topic {i+1}: {topic}")

    print(f"\nDocument topic proportions (H):")
    print(np.round(H_docs.T, 3))

    print("\n--- Random Initialization Effects ---")
    for trial in range(5):
        W_rand, H_rand, _ = nmf_multiplicative(V, k, max_iter=200)
        err_rand = np.linalg.norm(V - W_rand @ H_rand, 'fro')
        print(f"  Trial {trial+1}: error = {err_rand:.4f}")

    print("\n--- Non-negativity Enforcement Check ---")
    V_sparse = np.maximum(np.random.randn(20, 15), 0)
    W_s, H_s, _ = nmf_multiplicative(V_sparse, k=4)
    neg_W = (W_s < 0).sum()
    neg_H = (H_s < 0).sum()
    print(f"Negative entries in W: {neg_W}, in H: {neg_H}")


if __name__ == "__main__":
    main()
