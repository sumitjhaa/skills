import numpy as np
import matplotlib.pyplot as plt

def soft_threshold(x, lam):
    return np.sign(x) * np.maximum(np.abs(x) - lam, 0)

def prox_l2(x, lam):
    norm = np.linalg.norm(x)
    if norm <= lam:
        return np.zeros_like(x)
    return (1 - lam / norm) * x

def proximal_gradient_descent(grad_f, prox_g, x0, lr=0.1, n_iter=200):
    x = x0.copy()
    traj = [x.copy()]
    for i in range(n_iter):
        x = prox_g(x - lr * grad_f(x), lr)
        traj.append(x.copy())
    return np.array(traj)

def ista(A, b, lam, x0, lr=0.5, n_iter=200):
    grad_f = lambda x: A.T @ (A @ x - b)
    prox_g = lambda x, eta: soft_threshold(x, eta * lam)
    return proximal_gradient_descent(grad_f, prox_g, x0, lr, n_iter)

def fista(A, b, lam, x0, lr=0.5, n_iter=200):
    x = x0.copy()
    y = x0.copy()
    t = 1.0
    traj = [x.copy()]
    for i in range(n_iter):
        x_old = x.copy()
        grad = A.T @ (A @ y - b)
        x = soft_threshold(y - lr * grad, lr * lam)
        t_new = (1 + np.sqrt(1 + 4*t**2)) / 2
        y = x + ((t - 1) / t_new) * (x - x_old)
        t = t_new
        traj.append(x.copy())
    return np.array(traj)

def main():
    print("=" * 60)
    print("PROXIMAL OPERATORS")
    print("=" * 60)

    print("\n--- Soft Thresholding (Prox of L1) ---")
    x = np.array([1.5, -0.5, 0.3, -2.0, 0.0])
    for lam in [0.0, 0.5, 1.0, 2.0]:
        result = soft_threshold(x, lam)
        print(f"  λ={lam:.1f}: {result}")

    print(f"\n--- Proximal Operator of L2 Norm ---")
    x_l2 = np.array([3.0, 4.0])
    for lam in [2.0, 5.0, 10.0]:
        result = prox_l2(x_l2, lam)
        print(f"  λ={lam:.1f}: {result}, norm={np.linalg.norm(result):.4f}")

    print(f"\n--- ISTA for LASSO ---")
    np.random.seed(42)
    n, d = 30, 50
    A = np.random.randn(n, d)
    x_true = np.zeros(d)
    x_true[:5] = np.random.randn(5)
    b = A @ x_true + 0.05 * np.random.randn(n)

    lam = 0.1
    x0 = np.zeros(d)

    traj_ista = ista(A, b, lam, x0)
    traj_fista = fista(A, b, lam, x0)

    x_ista = traj_ista[-1]
    x_fista = traj_fista[-1]

    print(f"  True non-zeros: {np.sum(np.abs(x_true) > 1e-4)}")
    print(f"  ISTA non-zeros:  {np.sum(np.abs(x_ista) > 1e-4)}")
    print(f"  FISTA non-zeros: {np.sum(np.abs(x_fista) > 1e-4)}")
    print(f"  ISTA error:  {np.linalg.norm(x_ista - x_true):.4f}")
    print(f"  FISTA error: {np.linalg.norm(x_fista - x_true):.4f}")
    print(f"  ISTA final obj: {0.5*np.linalg.norm(A@x_ista-b)**2 + lam*np.linalg.norm(x_ista, 1):.6f}")
    print(f"  FISTA final obj: {0.5*np.linalg.norm(A@x_fista-b)**2 + lam*np.linalg.norm(x_fista, 1):.6f}")

    print(f"\n--- Proximal Gradient on 1D ---")
    f_smooth = lambda x: 0.5 * (x - 2)**2
    grad_f = lambda x: x - 2
    prox_l1 = lambda x, eta: soft_threshold(x, eta * 0.5)

    traj_pgd = proximal_gradient_descent(grad_f, prox_l1, np.array([5.0]))
    print(f"  Proximal GD: x*={traj_pgd[-1, 0]:.6f}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    xs = np.linspace(-3, 3, 100)
    for lam, color in zip([0.2, 0.5, 1.0, 2.0], ['r', 'g', 'b', 'm']):
        y = soft_threshold(xs, lam)
        axes[0].plot(xs, y, color=color, label=f'λ={lam}')
    axes[0].plot(xs, xs, 'k--', alpha=0.5, label='identity')
    axes[0].set_xlabel('x'); axes[0].set_ylabel('prox(x)')
    axes[0].set_title('Soft Thresholding (L1 Prox)')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    ista_loss = [0.5*np.linalg.norm(A@p-b)**2 + lam*np.linalg.norm(p, 1) for p in traj_ista]
    fista_loss = [0.5*np.linalg.norm(A@p-b)**2 + lam*np.linalg.norm(p, 1) for p in traj_fista]
    axes[1].semilogy(ista_loss, 'b-', label='ISTA')
    axes[1].semilogy(fista_loss, 'r-', label='FISTA')
    axes[1].set_xlabel('Iteration'); axes[1].set_ylabel('Objective')
    axes[1].set_title('ISTA vs FISTA for LASSO')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/18_proximal_operators.png', dpi=100)
    print(f"\nPlot saved to /tmp/18_proximal_operators.png")

if __name__ == "__main__":
    main()
