import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def natural_gradient(grad_log_p, fisher, x0, lr=0.1, n_iter=100):
    x = x0.copy()
    traj = [x.copy()]
    for i in range(n_iter):
        g = grad_log_p(x)
        F = fisher(x)
        reg = 1e-6 * np.eye(len(x))
        x = x - lr * np.linalg.solve(F + reg, g)
        traj.append(x.copy())
    return np.array(traj)

def main():
    print("=" * 60)
    print("NATURAL GRADIENT DESCENT")
    print("=" * 60)

    print("\n--- Bernoulli GLM with Natural Gradient ---")
    np.random.seed(42)
    n, d = 200, 3
    X = np.random.randn(n, d)
    w_true = np.array([1.0, -0.5, 0.3])
    p = 1 / (1 + np.exp(-X @ w_true))
    y = (np.random.rand(n) < p).astype(float)

    def grad_bernoulli(w):
        p_pred = 1 / (1 + np.exp(-X @ w))
        return X.T @ (p_pred - y)

    def fisher_bernoulli(w):
        p_pred = 1 / (1 + np.exp(-X @ w))
        W = np.diag(p_pred * (1 - p_pred))
        return X.T @ W @ X

    w0 = np.zeros(d)
    traj_ng = natural_gradient(grad_bernoulli, fisher_bernoulli, w0, lr=0.5, n_iter=50)

    w_sgd = w0.copy()
    traj_sgd = [w_sgd.copy()]
    for i in range(500):
        idx = np.random.randint(n)
        xi, yi = X[idx], y[idx]
        pi = 1 / (1 + np.exp(-xi @ w_sgd))
        w_sgd = w_sgd - 0.1 * xi * (pi - yi)
        traj_sgd.append(w_sgd.copy())
    traj_sgd = np.array(traj_sgd)

    print(f"  True w: {w_true}")
    print(f"  NG:     {traj_ng[-1]}")
    print(f"  SGD:    {traj_sgd[-1]}")
    print(f"  NG error:  {np.linalg.norm(traj_ng[-1] - w_true):.4f}")
    print(f"  SGD error: {np.linalg.norm(traj_sgd[-1] - w_true):.4f}")

    print(f"\n--- Fisher Information Matrix ---")
    w_test = np.zeros(d)
    F = fisher_bernoulli(w_test)
    print(f"  Fisher at w=0:\n{F}")
    eigvals = np.linalg.eigvalsh(F)
    print(f"  Eigenvalues: {eigvals}")

    print(f"\n--- KL Divergence Approximation ---")
    w1 = np.array([1.0, 0.5, -0.3])
    w2 = w1 + 0.01 * np.random.randn(3)

    def kl_div(p, q):
        return np.sum(p * np.log(p / q) + (1-p) * np.log((1-p) / (1-q)))

    p1 = 1 / (1 + np.exp(-X @ w1))
    p2 = 1 / (1 + np.exp(-X @ w2))
    kl_actual = np.mean(kl_div(p1, p2))
    dw = w2 - w1
    kl_approx = 0.5 * dw @ fisher_bernoulli(w1) @ dw / n
    print(f"  Actual KL:   {kl_actual:.6f}")
    print(f"  Fisher approx: {kl_approx:.6f}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    ng_errors = [np.linalg.norm(w - w_true) for w in traj_ng]
    sgd_errors = [np.linalg.norm(w - w_true) for w in traj_sgd[::10]]
    axes[0].semilogy(ng_errors, 'r-', label='Natural Gradient', linewidth=2)
    axes[0].semilogy(np.arange(len(sgd_errors))*10, sgd_errors, 'b-', alpha=0.7, label='SGD')
    axes[0].set_xlabel('Iteration'); axes[0].set_ylabel('‖w - w*‖')
    axes[0].set_title('Convergence to True Weights')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    methods = ['SGD', 'Natural GD']
    errors = [np.linalg.norm(traj_sgd[-1] - w_true), np.linalg.norm(traj_ng[-1] - w_true)]
    axes[1].bar(methods, errors, color=['blue', 'red'])
    axes[1].set_ylabel('Final Error')
    axes[1].set_title('Final Parameter Recovery')
    axes[1].grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('../../assets/phase02/23_natural_gradient.png', dpi=100)
    print(f"\nPlot saved to /tmp/23_natural_gradient.png")

if __name__ == "__main__":
    main()
