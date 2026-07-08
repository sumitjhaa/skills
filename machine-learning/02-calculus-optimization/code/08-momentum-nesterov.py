import numpy as np
import matplotlib.pyplot as plt

def momentum_gd(grad_f, x0, lr=0.01, beta=0.9, n_iter=100):
    x = x0.copy()
    v = np.zeros_like(x)
    traj = [x.copy()]
    for i in range(n_iter):
        v = beta * v + grad_f(x)
        x = x - lr * v
        traj.append(x.copy())
    return np.array(traj)

def nesterov_gd(grad_f, x0, lr=0.01, beta=0.9, n_iter=100):
    x = x0.copy()
    v = np.zeros_like(x)
    traj = [x.copy()]
    for i in range(n_iter):
        lookahead = x - lr * beta * v
        v = beta * v + grad_f(lookahead)
        x = x - lr * v
        traj.append(x.copy())
    return np.array(traj)

def main():
    print("=" * 60)
    print("MOMENTUM & NESTEROV ACCELERATED GRADIENT")
    print("=" * 60)

    def rosenbrock(x):
        return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

    def grad_rosenbrock(x):
        dx = -2*(1 - x[0]) - 400*x[0]*(x[1] - x[0]**2)
        dy = 200*(x[1] - x[0]**2)
        return np.array([dx, dy])

    x0 = np.array([-1.5, 1.5])
    n_iter = 200

    sgd_traj = np.zeros((n_iter + 1, 2))
    sgd_traj[0] = x0
    x = x0.copy()
    lr = 0.001
    for i in range(n_iter):
        x = x - lr * grad_rosenbrock(x)
        sgd_traj[i + 1] = x

    mom_traj = momentum_gd(grad_rosenbrock, x0, lr=0.001, beta=0.9, n_iter=n_iter)
    nag_traj = nesterov_gd(grad_rosenbrock, x0, lr=0.001, beta=0.9, n_iter=n_iter)

    print(f"\nRosenbrock minimization from x0=({x0[0]}, {x0[1]})")
    print(f"SGD final:    x=({sgd_traj[-1, 0]:.4f}, {sgd_traj[-1, 1]:.4f}), f={rosenbrock(sgd_traj[-1]):.6f}")
    print(f"Momentum:     x=({mom_traj[-1, 0]:.4f}, {mom_traj[-1, 1]:.4f}), f={rosenbrock(mom_traj[-1]):.6f}")
    print(f"NAG:          x=({nag_traj[-1, 0]:.4f}, {nag_traj[-1, 1]:.4f}), f={rosenbrock(nag_traj[-1]):.6f}")

    sgd_loss = [rosenbrock(p) for p in sgd_traj]
    mom_loss = [rosenbrock(p) for p in mom_traj]
    nag_loss = [rosenbrock(p) for p in nag_traj]
    print(f"\nSGD best loss: {min(sgd_loss):.6f} at iter {np.argmin(sgd_loss)}")
    print(f"Momentum best loss: {min(mom_loss):.6f} at iter {np.argmin(mom_loss)}")
    print(f"NAG best loss: {min(nag_loss):.6f} at iter {np.argmin(nag_loss)}")

    f_quad = lambda x: x**4 - 3*x**2 + 2
    g_quad = lambda x: 4*x**3 - 6*x
    x0_quad = np.array([2.0])

    for beta in [0, 0.5, 0.9, 0.99]:
        x = x0_quad.copy()
        v = 0.0
        for t in range(50):
            v = beta * v + g_quad(x)
            x = x - 0.01 * v
        print(f"\nQuadratic f(x)=x⁴-3x²+2, beta={beta}: x_final={x[0]:.4f}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].semilogy(sgd_loss, 'r-', label='SGD', linewidth=1.5)
    axes[0].semilogy(mom_loss, 'g-', label='Momentum', linewidth=1.5)
    axes[0].semilogy(nag_loss, 'b-', label='NAG', linewidth=1.5)
    axes[0].set_xlabel('Iteration'); axes[0].set_ylabel('Loss')
    axes[0].set_title('Rosenbrock Convergence')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    X, Y = np.meshgrid(np.linspace(-2, 2, 100), np.linspace(-1, 3, 100))
    Z = np.array([[rosenbrock([x, y]) for x in X[0]] for y in Y[:, 0]])
    axes[1].contour(X, Y, Z, levels=np.logspace(-1, 3, 20), cmap='viridis')
    axes[1].plot(sgd_traj[:, 0], sgd_traj[:, 1], 'r-', alpha=0.7, label='SGD')
    axes[1].plot(mom_traj[:, 0], mom_traj[:, 1], 'g-', alpha=0.7, label='Momentum')
    axes[1].plot(nag_traj[:, 0], nag_traj[:, 1], 'b-', alpha=0.7, label='NAG')
    axes[1].plot(1, 1, 'k*', markersize=12)
    axes[1].set_xlabel('x'); axes[1].set_ylabel('y')
    axes[1].set_title('Optimizer Trajectories on Rosenbrock')
    axes[1].legend(); axes[1].set_xlim(-2, 2); axes[1].set_ylim(-1, 3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/08_momentum_nesterov.png', dpi=100)
    print(f"\nPlot saved to /tmp/08_momentum_nesterov.png")

if __name__ == "__main__":
    main()
