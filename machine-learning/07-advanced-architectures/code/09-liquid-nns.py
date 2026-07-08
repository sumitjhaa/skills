"""
07.09 Liquid Neural Networks: LTC (Liquid Time-Constant) simulation.
"""
import numpy as np
import matplotlib.pyplot as plt


class LTCNeuron:
    """Liquid Time-Constant neuron."""
    def __init__(self, tau_min=0.1, tau_max=5.0):
        self.tau_min = tau_min
        self.tau_max = tau_max
        self.h = 0.0
        self.W_input = np.random.randn(1, 1) * 0.5
        self.b_input = np.zeros(1)
        self.W_hidden = np.random.randn(1, 1) * 0.5
        self.W_tau = np.random.randn(1, 1) * 0.5

    def f(self, x, h):
        """Dynamics."""
        return np.tanh(x @ self.W_input + h @ self.W_hidden + self.b_input)

    def tau(self, x):
        """Input-dependent time constant."""
        return self.tau_min + (self.tau_max - self.tau_min) * sigmoid(x @ self.W_tau)

    def step(self, x, dt=0.1):
        tau = self.tau(x)
        dh = (-self.h + self.f(x, self.h.reshape(1, -1))) / tau
        self.h += dt * dh.ravel()
        return self.h


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


if __name__ == "__main__":
    np.random.seed(42)
    neuron = LTCNeuron()
    T = 500
    hs = np.zeros(T)
    inputs = np.zeros((T, 1))
    inputs[100:300] = 1.0

    for t in range(T):
        h = neuron.step(inputs[t:t+1])
        hs[t] = h

    plt.figure(figsize=(12, 4))
    plt.subplot(121)
    plt.plot(hs, label='h(t)')
    plt.plot(inputs, '--', label='input', alpha=0.5)
    plt.xlabel('Time')
    plt.ylabel('State')
    plt.legend()
    plt.title('LTC Neuron Dynamics')

    # Phase portrait
    tau_vals = np.linspace(0.1, 5.0, 100)
    plt.subplot(122)
    h_vals = np.linspace(-1, 1, 100)
    tau_val = 2.0
    plt.plot(h_vals, -h_vals + np.tanh(h_vals * 0.5), label=f'tau={tau_val}')
    plt.plot(h_vals, np.zeros_like(h_vals), 'k--', alpha=0.3)
    plt.xlabel('h')
    plt.ylabel('dh/dt')
    plt.legend()
    plt.title('Phase portrait')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/liquid_nn.png')
    plt.close()
    print("Saved liquid_nn.png")
