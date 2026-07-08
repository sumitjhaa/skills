"""
07.25 Differentiable Programming: differentiable physics, AD examples.
"""
import numpy as np
import matplotlib.pyplot as plt


class DiffSim:
    """Differentiable physics simulation (mass-spring)."""
    def __init__(self, k=1.0, mass=1.0):
        self.k = k
        self.mass = mass

    def simulate(self, x0, v0, dt=0.01, steps=100):
        x = np.array(x0)
        v = np.array(v0)
        traj = [x.copy()]
        for _ in range(steps):
            a = -self.k * x / self.mass
            v += a * dt
            x += v * dt
            traj.append(x.copy())
        return np.array(traj)

    def grad_via_fd(self, x0, param='k', eps=1e-4):
        """Gradient of final position wrt parameter via finite differences."""
        orig = getattr(self, param)
        setattr(self, param, orig + eps)
        traj_p = self.simulate(x0, 0.0)
        setattr(self, param, orig - eps)
        traj_m = self.simulate(x0, 0.0)
        setattr(self, param, orig)
        return (traj_p - traj_m) / (2 * eps)


class DiffOpt:
    """Differentiable optimization (gradient descent as layer)."""
    @staticmethod
    def solve_lsq(A, b, lr=0.1, n_iter=100):
        x = np.zeros(A.shape[1])
        xs = [x.copy()]
        for _ in range(n_iter):
            grad = 2 * A.T @ (A @ x - b)
            x -= lr * grad
            xs.append(x.copy())
        return np.array(xs)


if __name__ == "__main__":
    np.random.seed(42)
    print("=== Differentiable Physics ===")
    sim = DiffSim(k=1.0, mass=1.0)
    traj = sim.simulate(1.0, 0.0, dt=0.05, steps=200)
    grad_k = sim.grad_via_fd(1.0, 'k')
    print(f"Final position: {traj[-1, 0]:.4f}")
    print(f"Gradient of final pos wrt k: {grad_k[-1, 0]:.4f}")

    print("\n=== Differentiable Optimization ===")
    A = np.random.randn(5, 3)
    x_true = np.array([1.0, -0.5, 2.0])
    b = A @ x_true + 0.05 * np.random.randn(5)
    xs = DiffOpt.solve_lsq(A, b, lr=0.1, n_iter=100)
    print(f"Final solution error: {np.linalg.norm(xs[-1] - x_true):.6f}")

    plt.figure(figsize=(12, 4))
    plt.subplot(131)
    plt.plot(traj)
    plt.title('Mass-spring trajectory')
    plt.xlabel('Step')
    plt.ylabel('Position')
    plt.subplot(132)
    plt.plot(grad_k)
    plt.title(f'dx_final/dk (FD approx) = {grad_k[-1, 0]:.4f}')
    plt.subplot(133)
    for i in range(3):
        plt.plot(xs[:, i], label=f'x{i}')
    plt.legend()
    plt.title('Differentiable LSQ optimization')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/differentiable_programming.png')
    plt.close()
    print("Saved differentiable_programming.png")
