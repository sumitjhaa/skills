import numpy as np
import matplotlib.pyplot as plt

def hessian_vector_product(grad_f, x, v, sigma=0.01):
    grad_plus = grad_f(x + sigma * v)
    grad_minus = grad_f(x - sigma * v)
    return (grad_plus - grad_minus) / (2 * sigma)

def adahessian(grad_f, x0, lr=0.15, beta1=0.9, beta2=0.999, n_iter=100):
    x = x0.copy()
    m = np.zeros_like(x)
    v = np.zeros_like(x)
    traj = [x.copy()]
    for t in range(1, n_iter + 1):
        g = grad_f(x)
        m = beta1 * m + (1 - beta1) * g
        rademacher = np.random.choice([-1, 1], size=len(x))
        hv = hessian_vector_product(grad_f, x, rademacher)
        d = np.abs(hv * rademacher)
        v = beta2 * v + (1 - beta2) * d**2
        m_hat = m / (1 - beta1**t)
        v_hat = v / (1 - beta2**t)
        x = x - lr * m_hat / (np.sqrt(v_hat) + 1e-8)
        traj.append(x.copy())
    return np.array(traj)

def stochastic_lbfgs(grad_f, x0, m=5, lr=1.0, n_iter=100):
    n = len(x0)
    x = x0.copy()
    s_list = []
    y_list = []
    traj = [x.copy()]

    for k in range(n_iter):
        g = grad_f(x)
        q = g.copy()
        if len(s_list) > 0:
            alphas = []
            for s, y in reversed(s_list):
                rho = 1.0 / max(y @ s, 1e-10)
                alpha = rho * (s @ q)
                alphas.append(alpha)
                q = q - alpha * y
            r = q * (s_list[-1][0] @ y_list[-1][0]) / max(y_list[-1][0] @ y_list[-1][0], 1e-10)
            for (s, y), alpha in zip(s_list, reversed(alphas)):
                rho = 1.0 / max(y @ s, 1e-10)
                beta = rho * (y @ r)
                r = r + (alpha - beta) * s
            d = -r
        else:
            d = -g

        x_new = x + lr * d
        g_new = grad_f(x_new)
        s = x_new - x
        y = g_new - g

        if len(s_list) >= m:
            s_list.pop(0)
            y_list.pop(0)
        s_list.append((s, y))
        x = x_new
        traj.append(x.copy())
    return np.array(traj)

def main():
    print("=" * 60)
    print("SECOND-ORDER STOCHASTIC METHODS")
    print("=" * 60)

    def rosenbrock(x):
        return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

    def grad_rosenbrock(x):
        dx = -2*(1 - x[0]) - 400*x[0]*(x[1] - x[0]**2)
        dy = 200*(x[1] - x[0]**2)
        return np.array([dx, dy])

    x0 = np.array([-1.5, 1.5])

    print("\n--- AdaHessian on Rosenbrock ---")
    traj_ah = adahessian(grad_rosenbrock, x0, lr=0.05, n_iter=100)
    print(f"  Final: ({traj_ah[-1, 0]:.4f}, {traj_ah[-1, 1]:.4f})")
    print(f"  f(x*) = {rosenbrock(traj_ah[-1]):.6f}")

    print(f"\n--- Stochastic L-BFGS on Rosenbrock ---")
    traj_slbfgs = stochastic_lbfgs(grad_rosenbrock, x0, m=5, lr=0.1, n_iter=50)
    print(f"  Final: ({traj_slbfgs[-1, 0]:.4f}, {traj_slbfgs[-1, 1]:.4f})")
    print(f"  f(x*) = {rosenbrock(traj_slbfgs[-1]):.6f}")

    x = x0.copy()
    traj_gd = [x.copy()]
    for _ in range(100):
        x = x - 0.001 * grad_rosenbrock(x)
        traj_gd.append(x.copy())

    ah_loss = [rosenbrock(p) for p in traj_ah]
    slbfgs_loss = [rosenbrock(p) for p in traj_slbfgs]
    gd_loss = [rosenbrock(p) for p in traj_gd]

    print(f"\n  GD final loss:    {gd_loss[-1]:.6f}")
    print(f"  AdaHessian loss:  {ah_loss[-1]:.6f}")
    print(f"  Stoch L-BFGS loss: {slbfgs_loss[-1]:.6f}")

    print(f"\n--- Hessian-Vector Product Test ---")
    x_test = np.array([1.0, 2.0])
    v = np.array([0.5, 0.3])
    hv = hessian_vector_product(grad_rosenbrock, x_test, v)
    print(f"  H(x)v at x=({x_test[0]},{x_test[1]}), v=({v[0]},{v[1]}):")
    print(f"  Result: {hv}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].semilogy(ah_loss, 'r-', label='AdaHessian', linewidth=2)
    axes[0].semilogy(slbfgs_loss, 'g-', label='Stoch L-BFGS', linewidth=2)
    axes[0].semilogy(gd_loss, 'b-', label='GD', alpha=0.7)
    axes[0].set_xlabel('Iteration'); axes[0].set_ylabel('Loss')
    axes[0].set_title('Second-Order Stochastic Methods on Rosenbrock')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    Xc, Yc = np.meshgrid(np.linspace(-2, 2, 80), np.linspace(-1, 3, 80))
    Zc = np.array([[rosenbrock([x, y]) for x in Xc[0]] for y in Yc[:, 0]])
    axes[1].contour(Xc, Yc, Zc, levels=np.logspace(-1, 3, 20), cmap='viridis')
    axes[1].plot(traj_ah[:, 0], traj_ah[:, 1], 'r-', label='AdaHessian')
    axes[1].plot(traj_slbfgs[:, 0], traj_slbfgs[:, 1], 'g-', label='Stoch L-BFGS')
    axes[1].plot(1, 1, 'k*', markersize=12)
    axes[1].set_xlabel('x'); axes[1].set_ylabel('y')
    axes[1].set_title('Trajectories')
    axes[1].legend()
    plt.tight_layout()
    plt.savefig('../../assets/phase02/22_second_order_stochastic.png', dpi=100)
    print(f"\nPlot saved to /tmp/22_second_order_stochastic.png")

if __name__ == "__main__":
    main()
