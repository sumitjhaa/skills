import numpy as np
import matplotlib.pyplot as plt

def gradient_descent(grad_f, x0, lr=0.1, n_iter=100):
    x = x0.copy()
    trajectory = [x.copy()]
    values = [f(x) if 'f' in dir() else None]
    for i in range(n_iter):
        x = x - lr * grad_f(x)
        trajectory.append(x.copy())
    return np.array(trajectory)

def main():
    print("=" * 60)
    print("GRADIENT DESCENT")
    print("=" * 60)

    f = lambda x: x**2 + 3*x + 2
    grad_f = lambda x: 2*x + 3

    x_opt = -1.5
    for lr in [0.01, 0.1, 0.5, 0.9]:
        x = 10.0
        traj = [x]
        for _ in range(50):
            x = x - lr * grad_f(x)
            traj.append(x)
        print(f"lr={lr:.2f}: final x={x:.4f}, f(x)={f(x):.4f}, steps to converge: {np.argmin(np.abs(np.array(traj) - x_opt) < 1e-4) if any(np.abs(np.array(traj) - x_opt) < 1e-4) else '>50'}")

    print(f"\n--- Linear Regression via GD ---")
    np.random.seed(42)
    n, d = 100, 5
    X = np.random.randn(n, d)
    w_true = np.random.randn(d)
    y = X @ w_true + 0.1 * np.random.randn(n)

    def grad_ols(w):
        return X.T @ (X @ w - y) / n

    def mse(w):
        return np.mean((X @ w - y)**2)

    w = np.zeros(d)
    lr = 0.1
    losses = []
    for i in range(200):
        w = w - lr * grad_ols(w)
        losses.append(mse(w))

    print(f"True weights:    {w_true}")
    print(f"Estimated:       {w}")
    print(f"Final MSE:       {losses[-1]:.6f}")
    print(f"Recovery error:  {np.linalg.norm(w - w_true):.6f}")

    print(f"\n--- Quadratic Convergence ---")
    f_quad = lambda x: (x - 2)**2
    g_quad = lambda x: 2*(x - 2)
    x0 = np.array([0.0])
    lrs = np.logspace(-3, 0, 6)
    final_losses = []
    for lr in lrs:
        x = x0.copy()
        for _ in range(50):
            x = x - lr * g_quad(x)
        final_losses.append(f_quad(x))
    print(f"Learning rate sweep:")
    for lr, loss in zip(lrs, final_losses):
        print(f"  lr={lr:.4f}: final loss={loss:.6e}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    xs = np.linspace(-5, 5, 100)
    axes[0].plot(xs, f(xs), 'b-', linewidth=2)
    for lr, color in zip([0.01, 0.1, 0.5], ['r', 'g', 'm']):
        x = 5.0
        traj_x, traj_f = [x], [f(x)]
        for _ in range(20):
            x = x - lr * grad_f(x)
            traj_x.append(x); traj_f.append(f(x))
        axes[0].plot(traj_x, traj_f, 'o-', color=color, label=f'lr={lr}', markersize=4)
    axes[0].axvline(x_opt, color='k', linestyle=':', alpha=0.5)
    axes[0].set_xlabel('x'); axes[0].set_ylabel('f(x)')
    axes[0].set_title('Gradient Descent on f(x) = x² + 3x + 2')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    axes[1].semilogy(losses, 'b-', linewidth=2)
    axes[1].set_xlabel('Iteration'); axes[1].set_ylabel('MSE')
    axes[1].set_title('GD for Linear Regression')
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/07_gradient_descent.png', dpi=100)
    print(f"\nPlot saved to /tmp/07_gradient_descent.png")

if __name__ == "__main__":
    main()
