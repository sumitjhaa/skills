"""
07.21 Flow Matching & Rectified Flow.
"""
import numpy as np
import matplotlib.pyplot as plt


class FlowMatching:
    """Conditional flow matching with linear interpolation."""
    def __init__(self, dim=2):
        self.dim = dim
        self.v_W1 = np.random.randn(dim + 1, 64) * 0.1  # +1 for time
        self.v_b1 = np.zeros(64)
        self.v_W2 = np.random.randn(64, 64) * 0.1
        self.v_b2 = np.zeros(64)
        self.v_W3 = np.random.randn(64, dim) * 0.1
        self.v_b3 = np.zeros(dim)

    def vector_field(self, x, t):
        xt = np.hstack([x, t.reshape(-1, 1)])
        h = np.tanh(xt @ self.v_W1 + self.v_b1)
        h = np.tanh(h @ self.v_W2 + self.v_b2)
        return h @ self.v_W3 + self.v_b3

    def sample_conditional(self, x0, x1, t):
        xt = (1 - t) * x0 + t * x1
        ut = x1 - x0
        return xt, ut

    def odefy(self, x_start, n_steps=50):
        x = x_start.copy()
        dt = 1.0 / n_steps
        for i in range(n_steps):
            t = np.full(len(x), i * dt)
            v = self.vector_field(x, t)
            x = x + dt * v
        return x


if __name__ == "__main__":
    np.random.seed(42)
    fm = FlowMatching(dim=2)
    x1 = np.random.randn(500, 2)
    x1[:250] += np.array([3, 0])
    x1[250:] += np.array([-3, 0])
    x0 = np.random.randn(500, 2)

    for epoch in range(500):
        t = np.random.uniform(0, 1, len(x1))
        xt, ut = fm.sample_conditional(x0, x1, t)
        vt = fm.vector_field(xt, t)
        loss = np.mean((vt - ut) ** 2)
        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss:.6f}")

    x_gen = fm.odefy(np.random.randn(500, 2))

    plt.figure(figsize=(12, 4))
    plt.subplot(131)
    plt.scatter(x1[:, 0], x1[:, 1], alpha=0.5)
    plt.title('Target distribution')
    plt.subplot(132)
    plt.scatter(x_gen[:, 0], x_gen[:, 1], alpha=0.5)
    plt.title('Generated (flow matching)')
    plt.subplot(133)
    ts = np.linspace(0, 1, 10)
    for i in range(5):
        traj = [np.random.randn(2)]
        for t in ts[1:]:
            v = fm.vector_field(np.array([traj[-1]]), np.array([t]))
            traj.append(traj[-1] + v[0] * 0.1)
        traj = np.array(traj)
        plt.plot(traj[:, 0], traj[:, 1], 'o-', alpha=0.5)
    plt.title('Flow trajectories')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/flow_matching.png')
    plt.close()
    print("Saved flow_matching.png")
