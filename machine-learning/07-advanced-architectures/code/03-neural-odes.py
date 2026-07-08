"""
07.03 Neural ODE: Solve ODE with Euler method.
Minimal demo of continuous dynamics.
"""
import numpy as np
import matplotlib.pyplot as plt


class NeuralODE:
    def __init__(self, hidden_dim=16):
        self.W1 = np.random.randn(1, hidden_dim) * 0.1
        self.b1 = np.zeros(hidden_dim)
        self.W2 = np.random.randn(hidden_dim, 1) * 0.1
        self.b2 = np.zeros(1)

    def f(self, t, h):
        """dh/dt = NN(h, t)"""
        x = h @ self.W1 + self.b1
        x = np.tanh(x)
        x = x @ self.W2 + self.b2
        return x

    def forward(self, h0, t_span, dt=0.05):
        hs = [h0]
        t = t_span[0]
        while t < t_span[1] - 1e-8:
            h = hs[-1]
            dh = self.f(t, h)
            hs.append(h + dt * dh)
            t += dt
        return np.array(hs)


class ODEAdjoint(NeuralODE):
    """Memory-efficient adjoint gradient (conceptual)."""
    def adjoint(self, h_traj, dL_dhT):
        dh = self.f(0, h_traj[-1:])
        adj = [dL_dhT]
        for h in reversed(h_traj[:-1]):
            da_dt = -adj[-1] @ self.f(0, h) * 0  # simplified
            adj.append(adj[-1] + da_dt * 0.05)
        return np.array(adj)


if __name__ == "__main__":
    np.random.seed(42)
    node = NeuralODE()
    h0 = np.array([[1.0, -0.5]])
    t_span = (0.0, 5.0)
    traj = node.forward(h0, t_span)
    ts = np.linspace(t_span[0], t_span[1], len(traj))

    plt.figure(figsize=(10, 4))
    plt.subplot(121)
    plt.plot(ts, traj[:, 0, 0], label='h1')
    plt.plot(ts, traj[:, 0, 1], label='h2')
    plt.xlabel('t')
    plt.ylabel('h(t)')
    plt.legend()
    plt.title('Neural ODE trajectory')
    plt.subplot(122)
    plt.plot(traj[:, 0, 0], traj[:, 0, 1])
    plt.scatter(traj[0, 0, 0], traj[0, 0, 1], c='g', s=100, label='start')
    plt.scatter(traj[-1, 0, 0], traj[-1, 0, 1], c='r', s=100, label='end')
    plt.xlabel('h1')
    plt.ylabel('h2')
    plt.legend()
    plt.title('Phase portrait')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/neural_ode.png')
    plt.close()
    print("Saved neural_ode.png")
