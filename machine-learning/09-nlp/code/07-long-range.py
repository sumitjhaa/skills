"""
09.07 Long-Range — Sliding Window & Dilated Attention
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


def sliding_window_attention(Q, K, V, window_size, mask=None):
    """
    Compute attention with a fixed window.
    Q, K, V: (B, T, d)
    Returns: (B, T, d)
    """
    B, T, d = Q.shape
    out = np.zeros_like(Q)
    for t in range(T):
        start = max(0, t - window_size)
        end = min(T, t + window_size + 1)
        q = Q[:, t:t+1, :]  # (B, 1, d)
        k = K[:, start:end, :]  # (B, W, d)
        v = V[:, start:end, :]  # (B, W, d)
        scores = q @ k.transpose(0, 2, 1) / np.sqrt(d)  # (B, 1, W)
        if mask is not None:
            scores += mask[:, :, t, start:end]
        attn = np.exp(scores - scores.max(axis=-1, keepdims=True))
        attn = attn / attn.sum(axis=-1, keepdims=True)
        out[:, t:t+1, :] = attn @ v
    return out


def dilated_attention(Q, K, V, window_size, dilation=1):
    """
    Dilated sliding window — attends every d-th token within window.
    """
    B, T, d = Q.shape
    out = np.zeros_like(Q)
    for t in range(T):
        indices = []
        for offset in range(-window_size, window_size + 1):
            if offset == 0:
                continue
            idx = t + offset
            if 0 <= idx < T and (abs(offset) % dilation == 0):
                indices.append(idx)
        indices.append(t)  # always attend self
        indices = sorted(set(indices))
        q = Q[:, t:t+1, :]
        k = K[:, indices, :]
        v = V[:, indices, :]
        scores = q @ k.transpose(0, 2, 1) / np.sqrt(d)
        attn = np.exp(scores - scores.max(axis=-1, keepdims=True))
        attn = attn / attn.sum(axis=-1, keepdims=True)
        out[:, t:t+1, :] = attn @ v
    return out


if __name__ == "__main__":
    B, T, d = 2, 16, 32
    np.random.seed(42)
    Q = np.random.randn(B, T, d)
    K = np.random.randn(B, T, d)
    V = np.random.randn(B, T, d)

    out_sw = sliding_window_attention(Q, K, V, window_size=3)
    out_dil = dilated_attention(Q, K, V, window_size=3, dilation=2)

    print(f"Input shape:         {Q.shape}")
    print(f"Sliding window out:  {out_sw.shape}")
    print(f"Dilated window out:  {out_dil.shape}")
    print(f"Max diff: {np.max(np.abs(out_sw - out_dil)):.4f}")
