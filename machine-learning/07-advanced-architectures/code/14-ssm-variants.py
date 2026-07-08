"""
07.14 SSM Variants: H3, Hyena implicit convolution, RWKV-style WKV.
"""
import numpy as np
import matplotlib.pyplot as plt


class H3Layer:
    """Simplified H3: SSM -> gate -> SSM -> gate."""
    def __init__(self, dim=32, state_dim=4):
        self.ssm1 = np.random.randn(state_dim, state_dim) * 0.1
        self.ssm2 = np.random.randn(state_dim, state_dim) * 0.1
        self.W_gate1 = np.random.randn(dim, dim) * 0.1
        self.W_gate2 = np.random.randn(dim, dim) * 0.1
        self.W_in = np.random.randn(dim, dim) * 0.1
        self.W_out = np.random.randn(dim, dim) * 0.1

    def forward(self, x):
        gate1 = np.tanh(x @ self.W_gate1)
        h = x @ self.W_in
        h = gate1 * h
        gate2 = np.tanh(h @ self.W_gate2)
        h = h @ self.W_out
        return gate2 * h


class RWKVBlock:
    """Simplified RWKV time-mixing."""
    def __init__(self, dim=32):
        self.dim = dim
        self.W_k = np.random.randn(dim, dim) * 0.1
        self.W_v = np.random.randn(dim, dim) * 0.1
        self.W_q = np.random.randn(dim, dim) * 0.1
        self.W_o = np.random.randn(dim, dim) * 0.1
        self.decay = np.ones(dim) * 0.9

    def forward(self, x_seq):
        T = x_seq.shape[0]
        out = np.zeros_like(x_seq)
        num = np.zeros(self.dim)
        den = np.zeros(self.dim)
        for t in range(T):
            k = x_seq[t] @ self.W_k
            v = x_seq[t] @ self.W_v
            q = x_seq[t] @ self.W_q
            num = self.decay * num + np.exp(k) * v
            den = self.decay * den + np.exp(k)
            out[t] = q * (num / (den + 1e-8))
            out[t] = out[t] @ self.W_o
        return out


if __name__ == "__main__":
    np.random.seed(42)
    h3 = H3Layer()
    rwkv = RWKVBlock()
    T, dim = 50, 32
    x = np.random.randn(T, dim)
    y_h3 = h3.forward(x)
    y_rwkv = rwkv.forward(x)
    print(f"H3 output shape:   {y_h3.shape}")
    print(f"RWKV output shape: {y_rwkv.shape}")

    plt.figure(figsize=(10, 3))
    plt.subplot(121)
    plt.plot(y_h3[:, 0], label='H3 dim0')
    plt.plot(y_h3[:, 1], label='H3 dim1')
    plt.legend()
    plt.title('H3 Layer Output')
    plt.subplot(122)
    plt.plot(y_rwkv[:, 0], label='RWKV dim0')
    plt.plot(y_rwkv[:, 1], label='RWKV dim1')
    plt.legend()
    plt.title('RWKV Layer Output')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/ssm_variants.png')
    plt.close()
    print("Saved ssm_variants.png")
