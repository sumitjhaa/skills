import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def lqr_riccati(A, B, Q, R, T, n_steps=1000):
    n = A.shape[0]
    m = B.shape[1]
    dt = T / n_steps
    P = np.zeros((n, n, n_steps + 1))
    for k in range(n_steps - 1, -1, -1):
        P_t = P[:, :, k + 1]
        P_dot = -(A.T @ P_t + P_t @ A - P_t @ B @ np.linalg.solve(R, B.T) @ P_t + Q)
        P[:, :, k] = P_t - dt * P_dot
    return P

def simulate_lqr(A, B, Q, R, x0, T, n_steps=100):
    P = lqr_riccati(A, B, Q, R, T, n_steps)
    dt = T / n_steps
    n = A.shape[0]
    m = B.shape[1]

    x = x0.copy()
    traj = [x.copy()]
    controls = []
    costs = []

    for k in range(n_steps):
        u = -np.linalg.solve(R, B.T @ P[:, :, k] @ x)
        controls.append(u.copy())
        x = x + dt * (A @ x + B @ u)
        traj.append(x.copy())
        costs.append(x @ Q @ x + u @ R @ u)

    return np.array(traj), np.array(controls), np.array(costs)

def main():
    print("=" * 60)
    print("OPTIMAL CONTROL")
    print("=" * 60)

    print("\n--- Linear Quadratic Regulator (LQR) ---")
    A = np.array([[0, 1], [0, 0]])
    B = np.array([[0], [1]])
    Q = np.eye(2)
    R = np.array([[0.1]])
    x0 = np.array([2.0, 0.0])
    T = 5.0

    traj, controls, costs = simulate_lqr(A, B, Q, R, x0, T)
    print(f"  Initial state: [{x0[0]:.2f}, {x0[1]:.2f}]")
    print(f"  Final state:   [{traj[-1, 0]:.4f}, {traj[-1, 1]:.4f}]")
    print(f"  Total cost:    {np.sum(costs):.4f}")
    print(f"  First control: {controls[0, 0]:.4f}")
    print(f"  Final control: {controls[-1, 0]:.4f}")

    print(f"\n--- LQR with Different Weights ---")
    x0 = np.array([2.0, 0.0])
    for R_val in [0.01, 0.1, 1.0, 10.0]:
        R_test = np.array([[R_val]])
        traj_r, ctrl_r, cost_r = simulate_lqr(A, B, Q, R_test, x0, T)
        print(f"  R={R_val:.2f}: |x(T)|={np.linalg.norm(traj_r[-1]):.4f}, total control effort={np.sum(np.abs(ctrl_r)):.2f}")

    print(f"\n--- Pontryagin's Maximum Principle Check ---")
    def dynamics(t, state_ctrl):
        x, lam = state_ctrl[:2], state_ctrl[2:4]
        u = -np.linalg.solve(R, B.T @ lam.reshape(-1, 1)).flatten() if lam.ndim == 1 else -np.linalg.solve(R, B.T @ lam)
        dx = A @ x + B @ u.flatten()
        dlam = -2 * Q @ x - A.T @ lam
        return np.hstack([dx, dlam])

    x0_pmp = np.array([2.0, 0.0, 0.0, 0.0])
    sol = solve_ivp(dynamics, [0, T], np.hstack([x0_pmp[:2], [0, 0]]), max_step=0.01)
    print(f"  PMP simulation steps: {len(sol.t)}")

    print(f"\n--- Direct Transcription (Optimization-based) ---")
    N = 30
    dt = T / N
    n_states, n_controls = 2, 1

    def obj(z):
        x = z[:N * n_states].reshape(N, n_states)
        u = z[N * n_states:].reshape(N, n_controls)
        cost = np.sum(x @ Q @ x.T) + np.sum(u @ R @ u.T)
        return cost

    def dyn_con(z):
        x = z[:N * n_states].reshape(N, n_states)
        u = z[N * n_states:].reshape(N, n_controls)
        cons = []
        for k in range(N - 1):
            x_next = x[k] + dt * np.array([x[k, 1], u[k, 0]])
            cons.extend(x[k+1] - x_next)
        cons.extend(x[0] - x0)
        return np.array(cons)

    z0 = np.zeros(N * (n_states + n_controls))
    cons = {'type': 'eq', 'fun': dyn_con}
    result = minimize(obj, z0, constraints=cons, method='SLSQP', options={'maxiter': 500})
    print(f"  Direct transcription success: {result.success}")
    if result.success:
        x_dt = result.x[:N * n_states].reshape(N, n_states)
        print(f"  Final state: [{x_dt[-1, 0]:.4f}, {x_dt[-1, 1]:.4f}]")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    time = np.linspace(0, T, len(traj))
    axes[0].plot(time, traj[:, 0], 'b-', label='Position (x₁)')
    axes[0].plot(time, traj[:, 1], 'r-', label='Velocity (x₂)')
    axes[0].plot(time[:-1], controls, 'g-', label='Control (u)')
    axes[0].set_xlabel('Time'); axes[0].set_ylabel('State / Control')
    axes[0].set_title('LQR Optimal Control')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    for R_val, color in zip([0.01, 0.1, 1.0, 10.0], ['r', 'g', 'b', 'm']):
        traj_r, _, _ = simulate_lqr(A, B, Q, np.array([[R_val]]), x0, T)
        axes[1].plot(traj_r[:, 0], traj_r[:, 1], color=color, label=f'R={R_val}')
    axes[1].plot(x0[0], x0[1], 'ko', markersize=8)
    axes[1].set_xlabel('Position'); axes[1].set_ylabel('Velocity')
    axes[1].set_title('Phase Portrait for Different R Values')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/25_optimal_control.png', dpi=100)
    print(f"\nPlot saved to /tmp/25_optimal_control.png")

if __name__ == "__main__":
    main()
