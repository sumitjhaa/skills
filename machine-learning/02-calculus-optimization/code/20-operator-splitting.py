import numpy as np
import matplotlib.pyplot as plt

def douglas_rachford(prox_A, prox_B, z0, n_iter=100):
    z = z0.copy()
    traj = [prox_A(z)]
    for k in range(n_iter):
        x = prox_A(z)
        y = prox_B(2 * x - z)
        z = z + (y - x)
        traj.append(prox_A(z))
    return np.array(traj)

def forward_backward(grad_f, prox_g, x0, gamma=0.1, n_iter=100):
    x = x0.copy()
    traj = [x.copy()]
    for k in range(n_iter):
        x = prox_g(x - gamma * grad_f(x), gamma)
        traj.append(x.copy())
    return np.array(traj)

def main():
    print("=" * 60)
    print("OPERATOR SPLITTING METHODS")
    print("=" * 60)

    print("\n--- Forward-Backward Splitting (Proximal Gradient) ---")
    f = lambda x: 0.5 * (x - 3)**2
    grad_f = lambda x: x - 3
    prox_l1 = lambda x, eta: np.sign(x) * np.maximum(np.abs(x) - eta, 0)

    x0 = np.array([10.0])
    traj_fb = forward_backward(grad_f, prox_l1, x0, gamma=0.5)
    print(f"  x* = {traj_fb[-1, 0]:.6f}")

    print(f"\n--- Douglas-Rachford Splitting for LASSO ---")
    np.random.seed(42)
    n, d = 20, 30
    A = np.random.randn(n, d)
    x_true = np.zeros(d)
    x_true[:4] = np.random.randn(4)
    b = A @ x_true + 0.05 * np.random.randn(n)
    lam = 0.1

    prox_A = lambda z: np.linalg.solve(A.T @ A + np.eye(d), A.T @ b + z)
    prox_B = lambda z: np.sign(z) * np.maximum(np.abs(z) - lam, 0)

    z0 = np.zeros(d)
    traj_dr = douglas_rachford(prox_A, prox_B, z0, n_iter=100)
    x_dr = traj_dr[-1]

    print(f"  Recovery error: {np.linalg.norm(x_dr - x_true):.4f}")
    print(f"  Final objective: {0.5*np.linalg.norm(A@x_dr-b)**2 + lam*np.linalg.norm(x_dr, 1):.6f}")

    print(f"\n--- Peaceman-Rachford Splitting ---")
    def peaceman_rachford(prox_A, prox_B, z0, n_iter=100):
        z = z0.copy()
        for k in range(n_iter):
            x = prox_A(z)
            y = prox_B(2 * x - z)
            z = 2 * y - x
        return prox_A(z)

    x_pr = peaceman_rachford(prox_A, prox_B, z0)
    print(f"  PR recovery error: {np.linalg.norm(x_pr - x_true):.4f}")

    print(f"\n--- Splitting for L1 + L2 (Elastic Net) ---")
    def elastic_net_prox(x, lam1=0.1, lam2=0.05):
        return soft_threshold(x, lam1) / (1 + lam2)

    def soft_threshold(x, lam):
        return np.sign(x) * np.maximum(np.abs(x) - lam, 0)

    x_en = forward_backward(lambda x: A.T @ (A @ x - b),
                            lambda x, eta: elastic_net_prox(x, eta*lam, 0.05),
                            np.zeros(d), gamma=0.5)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    xs = np.linspace(-3, 3, 100)

    def prox_l1_l2(x, lam1, lam2):
        return soft_threshold(x, lam1) / (1 + lam2)

    for lam1, color in zip([0.2, 0.5, 1.0], ['r', 'g', 'b']):
        y = prox_l1_l2(xs, lam1, 0.1)
        axes[0].plot(xs, y, color=color, label=f'λ₁={lam1}')
    axes[0].set_xlabel('x'); axes[0].set_ylabel('prox(x)')
    axes[0].set_title('Elastic Net Proximal Operator')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    dr_loss = [0.5*np.linalg.norm(A@p-b)**2 + lam*np.linalg.norm(p, 1) for p in traj_dr]
    fb_loss = [0.5*np.linalg.norm(A@p-b)**2 + lam*np.linalg.norm(p, 1) for p in
               forward_backward(lambda x: A.T @ (A @ x - b),
                                lambda x, eta: soft_threshold(x, eta*lam),
                                np.zeros(d), gamma=0.5)]
    min_len = min(len(dr_loss), len(fb_loss))
    axes[1].semilogy(dr_loss[:min_len], 'b-', label='Douglas-Rachford')
    axes[1].semilogy(fb_loss[:min_len], 'r--', label='Forward-Backward')
    axes[1].set_xlabel('Iteration'); axes[1].set_ylabel('Objective')
    axes[1].set_title('Splitting Methods Comparison')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/20_operator_splitting.png', dpi=100)
    print(f"\nPlot saved to /tmp/20_operator_splitting.png")

if __name__ == "__main__":
    main()
