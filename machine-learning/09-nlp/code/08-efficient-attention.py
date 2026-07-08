"""
09.08 Efficient Attention — Tiled Attention with Online Softmax
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


def standard_attention(Q, K, V):
    """Standard O(n²) attention for reference."""
    d = Q.shape[-1]
    scores = Q @ K.transpose(0, 2, 1) / np.sqrt(d)
    attn = np.exp(scores - scores.max(axis=-1, keepdims=True))
    attn = attn / attn.sum(axis=-1, keepdims=True)
    return attn @ V


def flash_attention_tiled(Q, K, V, block_size=4):
    """
    Simplified flash attention with tiling and online softmax.
    Only forward pass (no backward).
    """
    B, T, d = Q.shape
    O = np.zeros_like(Q)
    L = np.zeros((B, T, 1))
    M = np.full((B, T, 1), -np.inf)

    for i in range(0, T, block_size):
        Ki = K[:, i:i + block_size, :]
        Vi = V[:, i:i + block_size, :]
        for j in range(0, T, block_size):
            Qj = Q[:, j:j + block_size, :]
            # Compute block attention scores
            Sij = Qj @ Ki.transpose(0, 2, 1) / np.sqrt(d)  # (B, Bj, Bi)
            # Online softmax
            M_new = np.maximum(M[:, j:j + block_size], Sij.max(axis=-1, keepdims=True))
            Pij = np.exp(Sij - M_new)
            L_new = L[:, j:j + block_size] * np.exp(M[:, j:j + block_size] - M_new) + Pij.sum(axis=-1, keepdims=True)
            # Accumulate output
            O[:, j:j + block_size] = (
                O[:, j:j + block_size] * (L[:, j:j + block_size] / L_new) * np.exp(M[:, j:j + block_size] - M_new)
                + (Pij @ Vi) / L_new
            )
            M[:, j:j + block_size] = M_new
            L[:, j:j + block_size] = L_new

    return O


if __name__ == "__main__":
    np.random.seed(42)
    B, T, d = 2, 8, 16
    Q = np.random.randn(B, T, d)
    K = np.random.randn(B, T, d)
    V = np.random.randn(B, T, d)

    out_std = standard_attention(Q, K, V)
    out_tiled = flash_attention_tiled(Q, K, V, block_size=4)

    diff = np.max(np.abs(out_std - out_tiled))
    print(f"Standard attention:  {out_std.shape}")
    print(f"Tiled attention:     {out_tiled.shape}")
    print(f"Max difference:      {diff:.6f}")
    assert diff < 1e-5, "Tiled attention differs from standard!"
    print("Tiled attention matches standard attention.")
