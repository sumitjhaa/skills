"""
07.29 ML for Science: simplified AlphaFold/ESM concepts.
"""
import numpy as np
import matplotlib.pyplot as plt


class ESMBlock:
    """Simplified protein language model (ESM-style transformer block)."""
    def __init__(self, dim=32, n_heads=4):
        self.dim = dim
        self.n_heads = n_heads
        head_dim = dim // n_heads
        self.W_q = np.random.randn(n_heads, dim, head_dim) * 0.02
        self.W_k = np.random.randn(n_heads, dim, head_dim) * 0.02
        self.W_v = np.random.randn(n_heads, dim, head_dim) * 0.02
        self.W_o = np.random.randn(dim, dim) * 0.02
        self.ff_W1 = np.random.randn(dim, dim * 4) * 0.02
        self.ff_b1 = np.zeros(dim * 4)
        self.ff_W2 = np.random.randn(dim * 4, dim) * 0.02
        self.ff_b2 = np.zeros(dim)

    def forward(self, x):
        B, T, D = x.shape
        out = np.zeros_like(x)
        for h in range(self.n_heads):
            Q = x @ self.W_q[h]  # B, T, head_dim
            K = x @ self.W_k[h]
            V = x @ self.W_v[h]
            scores = Q @ K.transpose(0, 2, 1) / np.sqrt(D // self.n_heads)
            attn = np.exp(scores) / np.sum(np.exp(scores), axis=-1, keepdims=True)
            out += (attn @ V) @ self.W_o[:, h*(D//self.n_heads):(h+1)*(D//self.n_heads)].T
        out = out / self.n_heads
        ff = np.maximum(out @ self.ff_W1 + self.ff_b1, 0)
        return out + ff @ self.ff_W2 + self.ff_b2


class StructureModule:
    """Simplified protein structure prediction (AlphaFold style)."""
    def __init__(self, n_residues=10, coord_dim=3):
        self.W_pos = np.random.randn(n_residues, n_residues) * 0.02
        self.W_coord = np.random.randn(n_residues, coord_dim) * 0.02

    def forward(self, features):
        coords = features @ self.W_coord
        dists = np.sqrt(((coords[:, np.newaxis, :] - coords[np.newaxis, :, :]) ** 2).sum(-1) + 1e-8)
        return coords, dists


if __name__ == "__main__":
    np.random.seed(42)
    print("=== ESM Protein LM Block ===")
    esm = ESMBlock(dim=32)
    seq = np.random.randn(2, 20, 32)  # batch, residues, dim
    out = esm.forward(seq)
    print(f"ESM block: {seq.shape} -> {out.shape}")

    print("\n=== Structure Module (AlphaFold-style) ===")
    struct = StructureModule(n_residues=10)
    features = np.random.randn(10, 32)
    coords, dists = struct.forward(features)
    print(f"Predicted coords: {coords.shape}")
    print(f"Distance matrix:  {dists.shape}")
    print(f"Mean pairwise distance: {dists.mean():.4f}")

    plt.figure(figsize=(10, 4))
    plt.subplot(131)
    plt.imshow(dists, cmap='viridis')
    plt.colorbar(label='Distance')
    plt.title('Predicted distance map')
    plt.subplot(132)
    from mpl_toolkits.mplot3d import Axes3D
    ax = plt.subplot(132, projection='3d')
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c=np.arange(len(coords)), cmap='plasma', s=100)
    ax.set_title('Predicted 3D structure')
    plt.subplot(133)
    plt.plot(seq[0, :, 0], label='Residue feature 0')
    plt.plot(seq[0, :, 1], label='Residue feature 1')
    plt.legend()
    plt.title('Protein sequence features')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/ml_for_science.png')
    plt.close()
    print("Saved ml_for_science.png")
