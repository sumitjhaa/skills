import numpy as np
import matplotlib.pyplot as plt

def all_reduce(gradients):
    return np.mean(gradients, axis=0)

def distributed_sgd(grad_f, x0, n_workers=4, lr=0.01, n_iter=100):
    x = x0.copy()
    traj = [x.copy()]
    for t in range(n_iter):
        local_grads = []
        for w in range(n_workers):
            local_grads.append(grad_f(x, w))
        avg_grad = all_reduce(np.array(local_grads))
        x = x - lr * avg_grad
        traj.append(x.copy())
    return np.array(traj)

def gossip_sgd(grad_f, x0, adjacency, lr=0.01, n_iter=100):
    n_workers = len(adjacency)
    x = np.array([x0.copy() for _ in range(n_workers)])
    W = np.zeros((n_workers, n_workers))
    for i in range(n_workers):
        deg = len(adjacency[i])
        for j in adjacency[i]:
            W[i, j] = 1 / (max(deg, len(adjacency[j])) + 1)
        W[i, i] = 1 - W[i].sum()
    traj = [x.mean(axis=0)]
    for t in range(n_iter):
        for i in range(n_workers):
            g = grad_f(x[i], i)
            consensus = W[i] @ x
            x[i] = consensus - lr * g
        traj.append(x.mean(axis=0))
    return np.array(traj)

def local_sgd(grad_f, x0, n_workers=4, local_steps=5, lr=0.01, n_rounds=20):
    x = np.array([x0.copy() for _ in range(n_workers)])
    x_global = x0.copy()
    traj = [x_global.copy()]
    for r in range(n_rounds):
        for i in range(n_workers):
            x[i] = x_global.copy()
            for _ in range(local_steps):
                x[i] = x[i] - lr * grad_f(x[i], i)
        x_global = x.mean(axis=0)
        traj.append(x_global.copy())
    return np.array(traj)

def top_k_sparsification(grad, k=0.01):
    flat = grad.flatten()
    n = len(flat)
    k_keep = max(1, int(n * k))
    idx = np.argsort(np.abs(flat))[-k_keep:]
    sparse = np.zeros_like(flat)
    sparse[idx] = flat[idx]
    return sparse.reshape(grad.shape)

def main():
    print("=" * 60)
    print("DISTRIBUTED OPTIMIZATION")
    print("=" * 60)

    print("\n--- Distributed SGD on Quadratic ---")
    np.random.seed(42)
    d = 5
    true_w = np.random.randn(d)
    n_per_worker = 50
    n_workers = 4
    X = [np.random.randn(n_per_worker, d) for _ in range(n_workers)]
    y = [X[i] @ true_w + 0.1 * np.random.randn(n_per_worker) for i in range(n_workers)]

    grad_f = lambda w, i: X[i].T @ (X[i] @ w - y[i]) / n_per_worker

    x0 = np.zeros(d)
    traj_dist = distributed_sgd(grad_f, x0, n_workers, lr=0.1, n_iter=50)
    final_w = traj_dist[-1]
    print(f"  True weights: {true_w}")
    print(f"  Distributed SGD: {final_w}")
    print(f"  Error: {np.linalg.norm(final_w - true_w):.4f}")

    print(f"\n--- Communication Topologies ---")
    ring = [[1], [0, 2], [1, 3], [2]]
    fully_connected = [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]]

    traj_ring = gossip_sgd(grad_f, x0, ring, lr=0.05, n_iter=100)
    traj_fc = gossip_sgd(grad_f, x0, fully_connected, lr=0.05, n_iter=100)

    print(f"  Ring graph error: {np.linalg.norm(traj_ring[-1] - true_w):.4f}")
    print(f"  Fully connected error: {np.linalg.norm(traj_fc[-1] - true_w):.4f}")

    print(f"\n--- Local SGD (Federated Averaging) ---")
    traj_local = local_sgd(grad_f, x0, n_workers=4, local_steps=5, lr=0.1, n_rounds=20)
    print(f"  Local SGD error: {np.linalg.norm(traj_local[-1] - true_w):.4f}")

    print(f"\n--- Gradient Compression (Top-k Sparsification) ---")
    grad_test = np.random.randn(100)
    sparsity_ratios = [0.001, 0.01, 0.05, 0.1]
    for k in sparsity_ratios:
        sparse = top_k_sparsification(grad_test, k=k)
        compression = 1 - np.count_nonzero(sparse) / len(sparse)
        norm_error = np.linalg.norm(sparse - grad_test) / np.linalg.norm(grad_test)
        print(f"  k={k:.3f}: compression={compression:.1%}, relative error={norm_error:.4f}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    dist_loss = [np.linalg.norm(w - true_w) for w in traj_dist]
    ring_loss = [np.linalg.norm(w - true_w) for w in traj_ring]
    fc_loss = [np.linalg.norm(w - true_w) for w in traj_fc]
    axes[0].semilogy(dist_loss, 'b-', label='All-Reduce (Sync SGD)')
    axes[0].semilogy(ring_loss, 'r-', label='Gossip (Ring)')
    axes[0].semilogy(fc_loss, 'g-', label='Gossip (Full)')
    axes[0].set_xlabel('Iteration'); axes[0].set_ylabel('‖w - w*‖')
    axes[0].set_title('Distributed Optimization Convergence')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    methods = ['All-Reduce', 'Gossip Ring', 'Gossip FC', 'Local SGD']
    errors = [np.linalg.norm(traj_dist[-1] - true_w),
              np.linalg.norm(traj_ring[-1] - true_w),
              np.linalg.norm(traj_fc[-1] - true_w),
              np.linalg.norm(traj_local[-1] - true_w)]
    axes[1].bar(methods, errors, color=['blue', 'red', 'green', 'orange'])
    axes[1].set_ylabel('Final Error')
    axes[1].set_title('Method Comparison')
    axes[1].grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('../../assets/phase02/35_distributed_optimization.png', dpi=100)
    print(f"\nPlot saved to /tmp/35_distributed_optimization.png")

if __name__ == "__main__":
    main()
