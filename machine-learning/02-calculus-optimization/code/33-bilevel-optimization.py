import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def bilevel_hypergradient(F, grad_F_y, hess_f_yy, grad_f_yx, x, y_opt):
    dF_dy = grad_F_y(x, y_opt)
    dF_dx = np.gradient(F(x, y_opt), x)
    H = hess_f_yy(x, y_opt)
    dy_dx = np.linalg.solve(H, -grad_f_yx(x, y_opt))
    return dF_dx + dF_dy @ dy_dx

def unrolled_hypergradient(F, grad_f, x, y0, inner_steps=10, lr=0.1):
    y = y0.copy()
    ys = [y.copy()]
    for t in range(inner_steps):
        y = y - lr * grad_f(x, y)
        ys.append(y.copy())
    dF_dy = np.gradient(F(x, y), y)
    dy_accum = np.zeros_like(y)
    hess = lambda x, y: np.array([[2*x, 0], [0, 2]])  # for f = x*y1² + y2²
    for t in reversed(range(inner_steps)):
        y_t = ys[t]
        dgrad_dy = hess(x, y_t)
        dy_accum = dF_dy + (np.eye(len(y)) - lr * dgrad_dy).T @ dy_accum
    dF_dx = np.gradient(F(x, y), x)
    dgrad_dx = np.array([y[0]**2, 0])  # ∂²f/∂x∂y
    return dy_accum @ dgrad_dx + dF_dx

def main():
    print("=" * 60)
    print("BILEVEL OPTIMIZATION")
    print("=" * 60)

    print("\n--- Toy Bilevel: Hyperparameter Tuning ---")
    inner_f = lambda x, y: x * y[0]**2 + y[1]**2
    outer_F = lambda x, y: (y[0] - 1)**2 + (y[1] - 2)**2 + 0.1 * x**2
    grad_F_y = lambda x, y: np.array([2*(y[0]-1), 2*(y[1]-2)])
    hess_f_yy = lambda x, y: np.array([[2*x, 0], [0, 2]])
    grad_f_yx = lambda x, y: np.array([y[0]**2, 0.0])

    x = 1.0
    y_opt = minimize(lambda y: inner_f(x, y), x0=[0, 0]).x
    print(f"  Inner opt at x={x}: y={y_opt}")

    hypergrad = bilevel_hypergradient(outer_F, grad_F_y, hess_f_yy, grad_f_yx, x, y_opt)
    print(f"  Hypergradient dF/dx: {hypergrad:.4f}")

    print(f"\n--- Hyperparameter Optimization: Ridge Regression ---")
    np.random.seed(42)
    n, d = 30, 10
    X_train = np.random.randn(n, d)
    w_true = np.random.randn(d)
    y_train = X_train @ w_true + 0.1 * np.random.randn(n)
    X_val = np.random.randn(20, d)
    y_val = X_val @ w_true + 0.1 * np.random.randn(20)

    def ridge_solution(lam):
        return np.linalg.solve(X_train.T @ X_train + lam * np.eye(d), X_train.T @ y_train)

    for lam in [0.01, 0.1, 1.0, 10.0]:
        w = ridge_solution(lam)
        val_loss = np.mean((X_val @ w - y_val)**2)
        train_loss = np.mean((X_train @ w - y_train)**2)
        print(f"  λ={lam:.2f}: train_loss={train_loss:.4f}, val_loss={val_loss:.4f}, ||w||={np.linalg.norm(w):.4f}")

    print(f"\n--- MAML-style Meta-Learning ---")
    def maml_update(theta, grad_inner, alpha=0.1):
        return theta - alpha * grad_inner(theta)

    task_gradients = lambda theta: np.array([2*(theta[0]-1), 2*(theta[1]-2)])

    theta = np.array([0.0, 0.0])
    meta_lr = 0.05
    print(f"  Meta-training for 10 iterations:")
    for i in range(10):
        theta_adapted = maml_update(theta, task_gradients)
        meta_grad = task_gradients(theta_adapted)
        theta = theta - meta_lr * meta_grad
        if i % 2 == 0:
            print(f"    Iter {i}: θ={theta}, adapted={theta_adapted}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    lams = np.logspace(-2, 1, 50)
    val_losses = []
    for lam in lams:
        w = ridge_solution(lam)
        val_losses.append(np.mean((X_val @ w - y_val)**2))
    axes[0].semilogx(lams, val_losses, 'b-', linewidth=2)
    axes[0].axvline(lams[np.argmin(val_losses)], color='r', linestyle='--',
                    label=f'Best λ={lams[np.argmin(val_losses)]:.2f}')
    axes[0].set_xlabel('λ'); axes[0].set_ylabel('Validation Loss')
    axes[0].set_title('Hyperparameter Selection via Bilevel Opt')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    xs = np.linspace(-2, 4, 100)
    ys = np.linspace(-2, 4, 100)
    Xg, Yg = np.meshgrid(xs, ys)
    Zg = (Yg - 1)**2 + (Yg - 2)**2 + 0.1 * Xg**2
    axes[1].contourf(Xg, Yg, Zg, levels=20, cmap='viridis')
    axes[1].set_xlabel('Hyperparameter x'); axes[1].set_ylabel('Inner variable y')
    axes[1].set_title('Bilevel Objective Landscape')
    plt.tight_layout()
    plt.savefig('../../assets/phase02/33_bilevel_optimization.png', dpi=100)
    print(f"\nPlot saved to /tmp/33_bilevel_optimization.png")

if __name__ == "__main__":
    main()
