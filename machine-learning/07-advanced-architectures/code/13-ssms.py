"""
07.13 SSMs: Structured State Space (S4) & Mamba-style selective scan.
"""
import numpy as np
import matplotlib.pyplot as plt


class SSM:
    """State Space Model: h' = Ah + Bx, y = Ch + Dx."""
    def __init__(self, state_dim=4):
        self.A = np.random.randn(state_dim, state_dim) * 0.1
        self.A = self.A - 0.5 * np.eye(state_dim)  # ensure stability
        self.B = np.random.randn(state_dim, 1) * 0.1
        self.C = np.random.randn(1, state_dim) * 0.1
        self.D = np.random.randn(1, 1) * 0.1
        self.h = np.zeros((state_dim, 1))

    def discretize(self, dt):
        Ad = np.eye(len(self.A)) + dt * self.A
        Bd = dt * self.B
        return Ad, Bd

    def step(self, x, dt=0.1):
        Ad, Bd = self.discretize(dt)
        self.h = Ad @ self.h + Bd @ x
        y = self.C @ self.h + self.D @ x
        return y

    def scan(self, xs, dt=0.1):
        outputs = []
        for x in xs:
            y = self.step(x.reshape(-1, 1), dt)
            outputs.append(y.ravel())
        return np.array(outputs)


class MambaBlock:
    """Simplified Mamba-style SSM with input-dependent dynamics."""
    def __init__(self, dim=16, state_dim=4):
        self.dim = dim
        self.state_dim = state_dim
        self.W_B = np.random.randn(dim, state_dim) * 0.1
        self.W_C = np.random.randn(dim, state_dim) * 0.1
        self.W_A = np.random.randn(state_dim, state_dim) * 0.1
        self.W_in = np.random.randn(dim, dim) * 0.1
        self.W_out = np.random.randn(dim, dim) * 0.1
        self.h = np.zeros(state_dim)

    def forward(self, x_seq):
        outs = []
        for x in x_seq:
            B = x @ self.W_B
            C = x @ self.W_C
            A = self.W_A
            dh = A @ self.h + B.reshape(-1, 1)
            self.h += dh * 0.1
            y = (C.reshape(1, -1) @ self.h).ravel()
            outs.append(y)
        return np.array(outs)


if __name__ == "__main__":
    np.random.seed(42)
    ssm = SSM(state_dim=4)
    T = 100
    xs = np.sin(np.linspace(0, 4 * np.pi, T))
    ys = ssm.scan(xs)

    mamba = MambaBlock()
    x_seq = np.random.randn(T, 16)
    y_seq = mamba.forward(x_seq)

    plt.figure(figsize=(12, 4))
    plt.subplot(121)
    plt.plot(xs, label='Input')
    plt.plot(ys, label='SSM Output')
    plt.legend()
    plt.title('SSM: State Space Model')
    plt.subplot(122)
    plt.plot(y_seq[:, 0], label='Mamba dim 0')
    plt.plot(y_seq[:, 1], label='Mamba dim 1')
    plt.legend()
    plt.title('Mamba: Selective SSM output')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/ssm.png')
    plt.close()
    print("Saved ssm.png")
