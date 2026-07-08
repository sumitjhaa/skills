import numpy as np
import matplotlib.pyplot as plt

def admm_lasso(A, b, lam=0.1, rho=1.0, max_iter=200):
    m, n = A.shape
    x = np.zeros(n)
    z = np.zeros(n)
    u = np.zeros(n)

    AtA = A.T @ A
    Atb = A.T @ b
    I = np.eye(n)

    primal_residuals = []
    dual_residuals = []
    objectives = []

    for k in range(max_iter):
        z_old = z.copy()

        x = np.linalg.solve(AtA + rho * I, Atb + rho * (z - u))
        z = np.sign(x + u) * np.maximum(np.abs(x + u) - lam / rho, 0)
        u = u + (x - z)

        primal_res = np.linalg.norm(x - z)
        dual_res = np.linalg.norm(-rho * (z - z_old))
        obj = 0.5 * np.linalg.norm(A @ x - b)**2 + lam * np.linalg.norm(x, 1)

        primal_residuals.append(primal_res)
        dual_residuals.append(dual_res)
        objectives.append(obj)

    return x, z, u, {'primal': primal_residuals, 'dual': dual_residuals, 'obj': objectives}

def admm_consensus(grad_f_list, prox_f_list, x0_list, rho=1.0, max_iter=100):
    N = len(x0_list)
    n = len(x0_list[0])
    x = np.array(x0_list)
    z = np.mean(x, axis=0)
    u = np.zeros((N, n))

    traj = [z.copy()]
    for k in range(max_iter):
        for i in range(N):
            x[i] = prox_f_list[i](x[i] - u[i], 1.0)
        z = np.mean(x + u, axis=0)
        for i in range(N):
            u[i] = u[i] + (x[i] - z)
        traj.append(z.copy())
    return np.array(traj)

def main():
    print("=" * 60)
    print("ADMM - ALTERNATING DIRECTION METHOD OF MULTIPLIERS")
    print("=" * 60)

    print("\n--- ADMM for LASSO ---")
    np.random.seed(42)
    n, d = 20, 50
    A = np.random.randn(n, d)
    x_true = np.zeros(d)
    x_true[:5] = np.random.randn(5)
    b = A @ x_true + 0.05 * np.random.randn(n)

    lam = 0.1
    x_admm, z_admm, u_admm, history = admm_lasso(A, b, lam, rho=1.0)

    print(f"  True non-zeros: {np.sum(np.abs(x_true) > 1e-4)}")
    print(f"  ADMM non-zeros: {np.sum(np.abs(z_admm) > 1e-4)}")
    print(f"  Recovery error: {np.linalg.norm(z_admm - x_true):.4f}")
    print(f"  Final primal residual: {history['primal'][-1]:.6e}")
    print(f"  Final dual residual:   {history['dual'][-1]:.6e}")

    print(f"\n--- ADMM for Consensus Optimization ---")
    np.random.seed(42)
    n_agents = 5
    n_dim = 3

    true_w = np.random.randn(n_dim)
    X_list = [np.random.randn(10, n_dim) for _ in range(n_agents)]
    y_list = [X_list[i] @ true_w + 0.1 * np.random.randn(10) for i in range(n_agents)]

    grad_f_list = [lambda w, i=i: X_list[i].T @ (X_list[i] @ w - y_list[i]) for i in range(n_agents)]
    prox_f_list = [lambda w, eta: w - eta * grad_f_list[i](w) for i in range(n_agents)]
    x0_list = [np.zeros(n_dim) for _ in range(n_agents)]

    traj = admm_consensus(grad_f_list, prox_f_list, x0_list)
    consensus = traj[-1]
    print(f"  True weights: {true_w}")
    print(f"  Consensus:    {consensus}")
    print(f"  Error:        {np.linalg.norm(consensus - true_w):.4f}")

    print(f"\n--- Effect of ρ (penalty parameter) ---")
    for rho in [0.1, 1.0, 10.0]:
        _, _, _, hist = admm_lasso(A, b, lam, rho=rho, max_iter=100)
        print(f"  ρ={rho:.1f}: final primal res={hist['primal'][-1]:.2e}, final obj={hist['obj'][-1]:.4f}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].semilogy(history['primal'], 'b-', label='Primal residual')
    axes[0].semilogy(history['dual'], 'r-', label='Dual residual')
    axes[0].set_xlabel('Iteration'); axes[0].set_ylabel('Residual')
    axes[0].set_title('ADMM Convergence: Primal & Dual Residuals')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    axes[1].semilogy(history['obj'], 'g-', linewidth=2)
    axes[1].set_xlabel('Iteration'); axes[1].set_ylabel('Objective')
    axes[1].set_title('ADMM Objective Convergence')
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/19_admm.png', dpi=100)
    print(f"\nPlot saved to /tmp/19_admm.png")

if __name__ == "__main__":
    main()
