"""
09.09 Positional Encodings — RoPE and ALiBi
Built with only numpy, scipy, matplotlib.
"""
import numpy as np
import matplotlib.pyplot as plt


def apply_rope(x, positions, base=10000.0):
    """
    Apply Rotary Position Embeddings to x.
    x: (..., d) where d is even
    positions: (...,) position indices
    """
    d = x.shape[-1]
    half = d // 2
    # Compute frequencies
    freqs = base ** (-np.arange(0, half, dtype=np.float32) / half)
    # Position angles: (..., half)
    angles = np.outer(positions, freqs).reshape(x.shape[:-1] + (half,))
    cos = np.cos(angles)
    sin = np.sin(angles)

    # Split x into two halves and rotate
    x1 = x[..., :half]
    x2 = x[..., half:2 * half]
    rotated = np.concatenate([x1 * cos - x2 * sin, x1 * sin + x2 * cos], axis=-1)
    # If d is odd, carry over last dim unchanged
    if d > 2 * half:
        rotated = np.concatenate([rotated, x[..., -1:]], axis=-1)
    return rotated


def apply_alibi(attention_scores, position_ids, num_heads, base=8.0):
    """
    Add ALiBi biases to attention scores.
    attention_scores: (B, H, T, T)
    position_ids: (T,) or (B, T)
    """
    B, H, T, _ = attention_scores.shape
    # Compute slopes per head
    m = np.array([1.0 / (base ** (i / H)) for i in range(1, H + 1)], dtype=np.float32)
    # Compute distance matrix
    pos = np.arange(T, dtype=np.float32)
    dist = pos[:, None] - pos[None, :]  # (T, T)
    alibi_bias = -m[:, None, None] * np.abs(dist)[None, :, :]  # (H, T, T)
    return attention_scores + alibi_bias[None, :, :, :]


if __name__ == "__main__":
    # RoPE demo
    d = 8
    T = 6
    x = np.random.randn(T, d)
    positions = np.arange(T)
    x_rot = apply_rope(x, positions)
    print(f"RoPE: {x.shape} -> {x_rot.shape}")

    # Verify: dot product depends on relative position
    q = apply_rope(np.random.randn(1, d), np.array([5]))
    k = apply_rope(np.random.randn(1, d), np.array([2]))
    k2 = apply_rope(np.random.randn(1, d), np.array([5]))
    print(f"Q·K (diff=3): {np.dot(q[0], k[0]):.4f}")
    print(f"Q·K (same):   {np.dot(q[0], k2[0]):.4f}")

    # ALiBi demo
    B, H, T = 2, 4, 8
    scores = np.random.randn(B, H, T, T)
    biased = apply_alibi(scores, np.arange(T), H)
    print(f"\nALiBi: {scores.shape} -> {biased.shape}")
    print(f"Bias at head 0, pos (5,2): {biased[0, 0, 5, 2] - scores[0, 0, 5, 2]:.4f}")
    print(f"Bias at head 3, pos (5,2): {biased[0, 3, 5, 2] - scores[0, 3, 5, 2]:.4f}")

    # Plot ALiBi slopes
    fig, ax = plt.subplots(figsize=(6, 4))
    H_plot = 8
    pos = np.arange(10)
    for h in range(H_plot):
        m = 1.0 / (8.0 ** (h / H_plot))
        ax.plot(pos, -m * pos, label=f"head {h}")
    ax.set_xlabel("Distance")
    ax.set_ylabel("Bias")
    ax.set_title("ALiBi: Attention Bias by Distance")
    ax.legend(fontsize=6)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("../../assets/phase09/09-positional-encodings.png")
