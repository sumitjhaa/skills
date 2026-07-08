import numpy as np
import matplotlib.pyplot as plt

def adagrad(grad_f, x0, lr=1.0, epsilon=1e-8, n_iter=100):
    x = x0.copy()
    G = np.zeros_like(x)
    traj = [x.copy()]
    for t in range(1, n_iter + 1):
        g = grad_f(x)
        G += g**2
        x = x - lr * g / (np.sqrt(G) + epsilon)
        traj.append(x.copy())
    return np.array(traj)

def rmsprop(grad_f, x0, lr=0.01, beta=0.9, epsilon=1e-8, n_iter=100):
    x = x0.copy()
    s = np.zeros_like(x)
    traj = [x.copy()]
    for t in range(1, n_iter + 1):
        g = grad_f(x)
        s = beta * s + (1 - beta) * g**2
        x = x - lr * g / (np.sqrt(s) + epsilon)
        traj.append(x.copy())
    return np.array(traj)

def adam(grad_f, x0, lr=0.01, beta1=0.9, beta2=0.999, epsilon=1e-8, n_iter=100):
    x = x0.copy()
    m = np.zeros_like(x)
    v = np.zeros_like(x)
    traj = [x.copy()]
    for t in range(1, n_iter + 1):
        g = grad_f(x)
        m = beta1 * m + (1 - beta1) * g
        v = beta2 * v + (1 - beta2) * g**2
        m_hat = m / (1 - beta1**t)
        v_hat = v / (1 - beta2**t)
        x = x - lr * m_hat / (np.sqrt(v_hat) + epsilon)
        traj.append(x.copy())
    return np.array(traj)

def main():
    print("=" * 60)
    print("ADAPTIVE OPTIMIZATION METHODS")
    print("=" * 60)

    def rosenbrock(x):
        return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

    def grad_rosenbrock(x):
        dx = -2*(1 - x[0]) - 400*x[0]*(x[1] - x[0]**2)
        dy = 200*(x[1] - x[0]**2)
        return np.array([dx, dy])

    x0 = np.array([-1.5, 1.5])
    n_iter = 200

    traj_adagrad = adagrad(grad_rosenbrock, x0, lr=0.5, n_iter=n_iter)
    traj_rmsprop = rmsprop(grad_rosenbrock, x0, lr=0.01, n_iter=n_iter)
    traj_adam = adam(grad_rosenbrock, x0, lr=0.01, n_iter=n_iter)

    print(f"Rosenbrock from ({x0[0]}, {x0[1]}):")
    print(f"  AdaGrad final: ({traj_adagrad[-1, 0]:.4f}, {traj_adagrad[-1, 1]:.4f})")
    print(f"  RMSprop final: ({traj_rmsprop[-1, 0]:.4f}, {traj_rmsprop[-1, 1]:.4f})")
    print(f"  Adam    final: ({traj_adam[-1, 0]:.4f}, {traj_adam[-1, 1]:.4f})")

    adam_loss = [rosenbrock(p) for p in traj_adam]
    print(f"  Adam best loss: {min(adam_loss):.6f} at iter {np.argmin(adam_loss)}")

    print(f"\n--- Sparse Gradients Demo ---")
    np.random.seed(42)
    n, d = 1000, 50
    X = np.random.randn(n, d)
    X[np.random.rand(n, d) < 0.95] = 0
    w_true = np.zeros(d)
    w_true[:5] = np.random.randn(5)
    y = X @ w_true + 0.1 * np.random.randn(n)

    def grad_logistic(w, i=None):
        if i is not None:
            xi, yi = X[i], y[i]
            pred = 1 / (1 + np.exp(-xi @ w))
            return xi * (pred - yi)
        pred = 1 / (1 + np.exp(-X @ w))
        return X.T @ (pred - y) / n

    w_adagrad = np.zeros(d)
    G = np.zeros(d)
    lr = 0.5
    for t in range(1, 201):
        g = grad_logistic(w_adagrad)
        G += g**2
        w_adagrad = w_adagrad - lr * g / (np.sqrt(G) + 1e-8)

    w_adam = np.zeros(d)
    m, v = np.zeros(d), np.zeros(d)
    for t in range(1, 201):
        g = grad_logistic(w_adam)
        m = 0.9 * m + 0.1 * g
        v = 0.999 * v + 0.001 * g**2
        m_hat = m / (1 - 0.9**t)
        v_hat = v / (1 - 0.999**t)
        w_adam = w_adam - 0.01 * m_hat / (np.sqrt(v_hat) + 1e-8)

    print(f"AdaGrad recovery error: {np.linalg.norm(w_adagrad - w_true):.4f}")
    print(f"Adam recovery error:    {np.linalg.norm(w_adam - w_true):.4f}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for traj, label, color in [(traj_adagrad, 'AdaGrad', 'r'),
                                 (traj_rmsprop, 'RMSprop', 'g'),
                                 (traj_adam, 'Adam', 'b')]:
        loss = [rosenbrock(p) for p in traj]
        axes[0].semilogy(loss, color=color, label=label)
    axes[0].set_xlabel('Iteration'); axes[0].set_ylabel('Loss')
    axes[0].set_title('Rosenbrock Convergence')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    Xc, Yc = np.meshgrid(np.linspace(-2, 2, 80), np.linspace(-1, 3, 80))
    Zc = np.array([[rosenbrock([x, y]) for x in Xc[0]] for y in Yc[:, 0]])
    axes[1].contour(Xc, Yc, Zc, levels=np.logspace(-1, 3, 20), cmap='viridis')
    axes[1].plot(traj_adam[:, 0], traj_adam[:, 1], 'b-', alpha=0.7, label='Adam')
    axes[1].plot(1, 1, 'k*', markersize=12)
    axes[1].set_xlabel('x'); axes[1].set_ylabel('y')
    axes[1].set_title('Adam Trajectory')
    axes[1].legend()
    plt.tight_layout()
    plt.savefig('../../assets/phase02/09_adaptive_methods.png', dpi=100)
    print(f"\nPlot saved to /tmp/09_adaptive_methods.png")

if __name__ == "__main__":
    main()
