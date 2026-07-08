"""
07.15 Hybrid SSM-Attention: Jamba / MambaFormer style.
"""
import numpy as np
import matplotlib.pyplot as plt


class Attention:
    def __init__(self, dim=32):
        self.W_q = np.random.randn(dim, dim) * 0.02
        self.W_k = np.random.randn(dim, dim) * 0.02
        self.W_v = np.random.randn(dim, dim) * 0.02
        self.W_o = np.random.randn(dim, dim) * 0.02

    def forward(self, x):
        T = x.shape[0]
        Q = x @ self.W_q
        K = x @ self.W_k
        V = x @ self.W_v
        scores = Q @ K.T / np.sqrt(self.W_q.shape[0])
        attn = np.exp(scores) / np.sum(np.exp(scores), axis=-1, keepdims=True)
        return attn @ V @ self.W_o


class SSMBlock:
    def __init__(self, dim=32, state_dim=4):
        self.A = np.random.randn(state_dim, state_dim) * 0.1 - 0.5 * np.eye(state_dim)
        self.B = np.random.randn(dim, state_dim) * 0.1
        self.C = np.random.randn(dim, state_dim) * 0.1
        self.W_in = np.random.randn(dim, dim) * 0.02
        self.W_out = np.random.randn(dim, dim) * 0.02
        self.h = np.zeros(state_dim)

    def forward(self, x_seq):
        outs = []
        for x in x_seq:
            h_in = x @ self.W_in
            self.h = self.A @ self.h + self.B.T @ h_in
            y = self.C @ self.h
            y = y @ self.W_out
            outs.append(y)
        return np.array(outs)


class HybridLayer:
    """SSM + Attention in one layer (simplified)."""
    def __init__(self, dim=32, state_dim=4):
        self.ssm = SSMBlock(dim, state_dim)
        self.attn = Attention(dim)
        self.W_gate = np.random.randn(dim, dim) * 0.02

    def forward(self, x):
        ssm_out = self.ssm.forward(x)
        attn_out = self.attn.forward(x)
        gate = np.tanh(x @ self.W_gate)
        return gate * ssm_out + (1 - gate) * attn_out


if __name__ == "__main__":
    np.random.seed(42)
    hybrid = HybridLayer()
    T, dim = 32, 32
    x = np.random.randn(T, dim)
    y = hybrid.forward(x)
    print(f"Hybrid (SSM+Attn): {x.shape} -> {y.shape}")

    plt.plot(y[:, 0], label='Hybrid out dim0')
    plt.plot(y[:, 1], label='Hybrid out dim1')
    plt.legend()
    plt.title('Hybrid SSM-Attention Layer')
    plt.savefig('../../assets/phase07/hybrid_ssm_attention.png')
    plt.close()
    print("Saved hybrid_ssm_attention.png")
