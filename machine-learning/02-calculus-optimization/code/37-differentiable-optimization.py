import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def qp_forward(Q, q, A, b):
    n = Q.shape[0]
    def objective(z):
        return 0.5 * z @ Q @ z + q @ z
    cons = [{'type': 'eq', 'fun': lambda z: A @ z - b}] if A is not None else []
    result = minimize(objective, np.zeros(n), constraints=cons, method='SLSQP')
    return result.x

def qp_backward(Q, q, A, z_star, dl_dz):
    n = len(z_star)
    KKT = np.block([
        [Q + Q.T, A.T],
        [A, np.zeros((A.shape[0], A.shape[0]))]
    ]) if A is not None else Q + Q.T

    rhs = np.hstack([-dl_dz, np.zeros(A.shape[0])]) if A is not None else -dl_dz

    if A is not None:
        sol = np.linalg.solve(KKT, rhs)
        return sol[:n]
    return np.linalg.solve(KKT, rhs)

def deq_fixed_point(f, x, theta, max_iter=50):
    z_shape = f(np.zeros(2), x, theta).shape
    z = np.zeros(z_shape)
    for i in range(max_iter):
        z_next = f(z, x, theta)
        if np.linalg.norm(z_next - z) < 1e-6:
            break
        z = z_next
    return z

def main():
    print("=" * 60)
    print("DIFFERENTIABLE OPTIMIZATION LAYERS")
    print("=" * 60)

    print("\n--- Differentiable QP Layer (Forward) ---")
    Q = np.array([[2, 0.5], [0.5, 2]])
    q = np.array([-1, -2])
    A = np.array([[1, 1]])
    b = np.array([1])

    z_star = qp_forward(Q, q, A, b)
    print(f"  QP: minimize ½zᵀQz + qᵀz s.t. z₁+z₂=1")
    print(f"  Solution: z* = {z_star}")

    print(f"\n--- Backward Pass (Implicit Diff) ---")
    dl_dz = np.array([1.0, 0.0])
    dz_dparams = qp_backward(Q, q, A, z_star, dl_dz)
    print(f"  dl/dz = {dl_dz}")
    print(f"  Sensitivities dz*/d(⋅) = {dz_dparams}")

    print(f"\n--- Deep Equilibrium Model (DEQ) ---")
    def deq_layer(z, x, theta):
        W, b = theta
        return np.tanh(W @ z + x + b)

    np.random.seed(42)
    W = 0.1 * np.random.randn(2, 2)
    b = np.zeros(2)
    theta = (W, b)
    x_input = np.array([1.0, 0.5])

    z_star_deq = deq_fixed_point(deq_layer, x_input, theta)
    print(f"  DEQ fixed point z* = {z_star_deq}")

    print(f"\n--- Gradient Through DEQ via Implicit Diff ---")
    eps = 1e-6
    J = np.zeros((2, 2))
    for i in range(2):
        e = np.zeros(2); e[i] = eps
        J[:, i] = (deq_layer(z_star_deq + e, x_input, theta) - deq_layer(z_star_deq - e, x_input, theta)) / (2 * eps)

    dl_dz_deq = np.array([1.0, 1.0])
    I_minus_J = np.eye(2) - J
    dz_star_dx = np.linalg.solve(I_minus_J, W)  # ∂f/∂x = W
    print(f"  dz*/dx = {dz_star_dx}")

    print(f"\n--- Sensitivity Analysis of QP Parameters ---")
    for q1 in [-3, -2, -1, 0, 1]:
        q_test = np.array([q1, -2])
        z = qp_forward(Q, q_test, A, b)
        print(f"  q₁={q1:3d}: z* = ({z[0]:.4f}, {z[1]:.4f})")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    q1_vals = np.linspace(-3, 1, 50)
    z1_vals = []
    for q1 in q1_vals:
        z = qp_forward(Q, np.array([q1, -2]), A, b)
        z1_vals.append(z[0])
    axes[0].plot(q1_vals, z1_vals, 'b-', linewidth=2)
    axes[0].set_xlabel('q₁'); axes[0].set_ylabel('z₁*')
    axes[0].set_title('QP Solution as Function of q₁')
    axes[0].grid(True, alpha=0.3)

    zs = np.linspace(-2, 2, 100)
    f_vals = deq_layer(np.array([zs, zs]).T, x_input, theta)
    axes[1].plot(zs, f_vals[:, 0], 'b-', label='f(z) component 0')
    axes[1].plot(zs, f_vals[:, 1], 'r-', label='f(z) component 1')
    axes[1].plot(zs, zs, 'k--', alpha=0.5, label='z = f(z) (fixed point)')
    axes[1].axvline(z_star_deq[0], color='b', linestyle=':', alpha=0.5)
    axes[1].set_xlabel('z'); axes[1].set_ylabel('f(z)')
    axes[1].set_title('DEQ Fixed Point')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/37_differentiable_optimization.png', dpi=100)
    print(f"\nPlot saved to /tmp/37_differentiable_optimization.png")

if __name__ == "__main__":
    main()
