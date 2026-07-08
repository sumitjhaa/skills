import numpy as np
import matplotlib.pyplot as plt

def coordinate_wise_gradient(f, x, sigma=1e-6):
    grad = np.zeros_like(x)
    for i in range(len(x)):
        e = np.zeros_like(x)
        e[i] = 1
        grad[i] = (f(x + sigma * e) - f(x - sigma * e)) / (2 * sigma)
    return grad

def spsa_gradient(f, x, sigma=1e-3):
    delta = np.random.choice([-1, 1], size=len(x))
    f_plus = f(x + sigma * delta)
    f_minus = f(x - sigma * delta)
    return (f_plus - f_minus) / (2 * sigma) * delta

def evolution_strategies(f, x0, sigma=0.1, lr=0.01, n_samples=50, n_iter=100):
    x = x0.copy()
    traj = [x.copy()]
    for t in range(n_iter):
        noise = sigma * np.random.randn(n_samples, len(x))
        rewards = np.array([f(x + n) for n in noise])
        rewards = (rewards - rewards.mean()) / (rewards.std() + 1e-8)
        grad = (noise.T @ rewards) / (n_samples * sigma)
        x = x + lr * grad
        traj.append(x.copy())
    return np.array(traj)

def main():
    print("=" * 60)
    print("ZEROTH-ORDER OPTIMIZATION")
    print("=" * 60)

    print("\n--- Finite Difference Gradient Accuracy ---")
    f = lambda x: np.sin(x[0]) + x[0]**2
    x0 = np.array([1.0])
    analytical = np.cos(1.0) + 2.0

    for sigma in [1e-2, 1e-4, 1e-6, 1e-8]:
        num_grad = coordinate_wise_gradient(f, x0, sigma)
        err = abs(num_grad[0] - analytical)
        print(f"  σ={sigma:.0e}: grad={num_grad[0]:.8f}, error={err:.2e}")

    print(f"\n--- SPSA Efficiency (2 evaluations, any dimension) ---")
    np.random.seed(42)
    errs_spsa = []
    for _ in range(100):
        spsa_g = spsa_gradient(f, x0)
        errs_spsa.append(abs(spsa_g[0] - analytical))
    print(f"  SPSA error (mean): {np.mean(errs_spsa):.4e}")

    print(f"\n--- Evolution Strategies on Quadratic ---")
    f_quad = lambda x: np.sum(x**2)
    x0 = np.array([3.0, 2.0, 1.0])
    traj_es = evolution_strategies(f_quad, x0, sigma=0.1, lr=0.05, n_samples=30, n_iter=100)
    print(f"  Starting: f({x0}) = {f_quad(x0)}")
    print(f"  Final: f({traj_es[-1]}) = {f_quad(traj_es[-1]):.6f}")

    print(f"\n--- Rosenbrock via SPSA-based GD ---")
    rosenbrock = lambda x: (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2
    x0_rosen = np.array([-1.5, 1.5])
    x = x0_rosen.copy()
    traj_spsa = [x.copy()]
    for i in range(200):
        g = spsa_gradient(rosenbrock, x, sigma=0.01)
        x = x - 0.001 * g
        traj_spsa.append(x.copy())
    traj_spsa = np.array(traj_spsa)
    print(f"  Final: f({traj_spsa[-1]}) = {rosenbrock(traj_spsa[-1]):.6f}")
    print(f"  Expected optimum: f((1,1)) = 0")

    print(f"\n--- Coordinate-wise vs SPSA Comparison ---")
    n_dims = [2, 5, 10, 20]
    for d in n_dims:
        f_d = lambda x: np.sum(x**2)
        x_d = np.ones(d)
        evals_cw = d * 2
        evals_spsa = 2
        print(f"  d={d:2d}: coordinate-wise uses {evals_cw:3d} evals, SPSA uses {evals_spsa} evals")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    xs = np.linspace(-3, 3, 100)
    f_sin = lambda x: np.sin(x) + 0.1 * x**2
    axes[0].plot(xs, f_sin(xs), 'k-', linewidth=2, label='f(x) = sin(x) + 0.1x²')

    x_test = 1.5
    for sigma, color in zip([0.5, 0.1, 0.01], ['r', 'g', 'b']):
        grad_est = coordinate_wise_gradient(f_sin, np.array([x_test]), sigma)
        tangent = f_sin(x_test) + grad_est[0] * (xs - x_test)
        axes[0].plot(xs, tangent, '--', color=color, label=f'σ={sigma}')
    axes[0].plot(x_test, f_sin(x_test), 'ko', markersize=8)
    axes[0].set_xlabel('x'); axes[0].set_ylabel('f(x)')
    axes[0].set_title('Finite Difference Gradient Estimates')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    es_loss = [np.sum(p**2) for p in traj_es]
    axes[1].semilogy(es_loss, 'b-', linewidth=2)
    axes[1].set_xlabel('Iteration'); axes[1].set_ylabel('f(x)')
    axes[1].set_title('Evolution Strategies on Σx²')
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/30_zeroth_order.png', dpi=100)
    print(f"\nPlot saved to /tmp/30_zeroth_order.png")

if __name__ == "__main__":
    main()
