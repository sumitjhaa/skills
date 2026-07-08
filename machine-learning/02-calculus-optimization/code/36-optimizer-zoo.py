import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def create_optimizers(grad_f, hess_f=None):
    def sgd(x, g, t, lr=0.01):
        return x - lr * g

    def momentum(x, g, t, lr=0.01, beta=0.9):
        if not hasattr(momentum, 'v'):
            momentum.v = np.zeros_like(x)
        momentum.v = beta * momentum.v + g
        return x - lr * momentum.v

    def adam(x, g, t, lr=0.01, beta1=0.9, beta2=0.999):
        if not hasattr(adam, 'm'):
            adam.m = np.zeros_like(x)
            adam.v = np.zeros_like(x)
        adam.m = beta1 * adam.m + (1 - beta1) * g
        adam.v = beta2 * adam.v + (1 - beta2) * g**2
        m_hat = adam.m / (1 - beta1**t)
        v_hat = adam.v / (1 - beta2**t)
        return x - lr * m_hat / (np.sqrt(v_hat) + 1e-8)

    def rmsprop(x, g, t, lr=0.01, beta=0.9):
        if not hasattr(rmsprop, 's'):
            rmsprop.s = np.zeros_like(x)
        rmsprop.s = beta * rmsprop.s + (1 - beta) * g**2
        return x - lr * g / (np.sqrt(rmsprop.s) + 1e-8)

    return {'SGD': sgd, 'Momentum': momentum, 'Adam': adam, 'RMSprop': rmsprop}

def benchmark_optimizers(problem, x0, optimizers, n_iter=100):
    results = {}
    grads_called = {}

    for name, opt_fn in optimizers.items():
        if hasattr(opt_fn, 'v'): del opt_fn.v
        if hasattr(opt_fn, 'm'): del opt_fn.m
        if hasattr(opt_fn, 's'): del opt_fn.s

        x = x0.copy()
        losses = []
        for t in range(1, n_iter + 1):
            g = problem['grad'](x)
            x = opt_fn(x, g, t)
            losses.append(problem['f'](x))

        results[name] = np.array(losses)
    return results

def main():
    print("=" * 60)
    print("FULL OPTIMIZER ZOO")
    print("=" * 60)

    print("\n--- Benchmark on Rosenbrock ---")
    rosenbrock = lambda x: (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2
    grad_rosen = lambda x: np.array([-2*(1-x[0]) - 400*x[0]*(x[1]-x[0]**2), 200*(x[1]-x[0]**2)])

    problem = {'f': rosenbrock, 'grad': grad_rosen}
    x0 = np.array([-1.5, 1.5])

    opt_fns = create_optimizers(grad_rosen)
    results = benchmark_optimizers(problem, x0, opt_fns, n_iter=200)

    for name, losses in results.items():
        print(f"  {name:10s}: final loss = {losses[-1]:.4e}")

    print(f"\n--- Benchmark on Beale ---")
    beale = lambda x: (1.5 - x[0] + x[0]*x[1])**2 + (2.25 - x[0] + x[0]*x[1]**2)**2 + (2.625 - x[0] + x[0]*x[1]**3)**2
    grad_beale = lambda x: np.array([
        2*(1.5-x[0]+x[0]*x[1])*(-1+x[1]) + 2*(2.25-x[0]+x[0]*x[1]**2)*(-1+x[1]**2) + 2*(2.625-x[0]+x[0]*x[1]**3)*(-1+x[1]**3),
        2*(1.5-x[0]+x[0]*x[1])*x[0] + 2*(2.25-x[0]+x[0]*x[1]**2)*2*x[0]*x[1] + 2*(2.625-x[0]+x[0]*x[1]**3)*3*x[0]*x[1]**2
    ])

    problem_beale = {'f': beale, 'grad': grad_beale}
    x0_beale = np.array([0.5, 0.5])

    opt_fns2 = create_optimizers(grad_beale)
    for key in opt_fns2:
        for attr in ['v', 'm', 's']:
            if hasattr(opt_fns2[key], attr):
                delattr(opt_fns2[key], attr)
    results_beale = benchmark_optimizers(problem_beale, x0_beale, opt_fns2, n_iter=200)

    for name, losses in results_beale.items():
        print(f"  {name:10s}: final loss = {losses[-1]:.4e}")

    print(f"\n--- Scipy Optimizers ---")
    res_bfgs = minimize(rosenbrock, x0, method='BFGS')
    res_nelder = minimize(rosenbrock, x0, method='Nelder-Mead')
    res_cg = minimize(rosenbrock, x0, method='CG')
    print(f"  BFGS:       f({res_bfgs.x}) = {res_bfgs.fun:.4e}, iter={res_bfgs.nit}")
    print(f"  Nelder-Mead: f({res_nelder.x}) = {res_nelder.fun:.4e}, iter={res_nelder.nit}")
    print(f"  CG:         f({res_cg.x}) = {res_cg.fun:.4e}, iter={res_cg.nit}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for name, losses in results.items():
        axes[0].semilogy(losses, label=name, linewidth=2)
    axes[0].set_xlabel('Iteration'); axes[0].set_ylabel('Loss')
    axes[0].set_title('Optimizer Comparison on Rosenbrock')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    for name, losses in results_beale.items():
        axes[1].semilogy(losses, label=name, linewidth=2)
    axes[1].set_xlabel('Iteration'); axes[1].set_ylabel('Loss')
    axes[1].set_title('Optimizer Comparison on Beale')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/36_optimizer_zoo.png', dpi=100)
    print(f"\nPlot saved to /tmp/36_optimizer_zoo.png")

if __name__ == "__main__":
    main()
