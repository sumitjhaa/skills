"""
09.16 Long Context — StreamingLLM Rolling Cache & Ring Attention Block
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


class StreamingLLMCache:
    """
    StreamingLLM: Rolling window cache + attention sink initial tokens.
    """

    def __init__(self, sink_size=4, window_size=8):
        self.sink_size = sink_size
        self.window_size = window_size
        self.keys = None
        self.values = None

    def update(self, key, value):
        # key, value: (B, H, T_new, d)
        if self.keys is None:
            self.keys = key
            self.values = value
        else:
            self.keys = np.concatenate([self.keys, key], axis=2)
            self.values = np.concatenate([self.values, value], axis=2)
            # Evict middle tokens while preserving sink + recent window
            total_len = self.keys.shape[2]
            if total_len > self.sink_size + self.window_size:
                # Keep sink tokens (first sink_size) + recent window_size tokens
                recent_start = total_len - self.window_size
                indices = list(range(self.sink_size)) + list(range(recent_start, total_len))
                self.keys = self.keys[:, :, indices, :]
                self.values = self.values[:, :, indices, :]

    def get(self):
        return self.keys, self.values


def ring_attention_block(Q, K, V, block_size=4):
    """
    Simplified Ring Attention: compute attention by processing blocks.
    Assumes sequence is distributed across block_size blocks.
    """
    B, T, d = Q.shape
    n_blocks = T // block_size
    out = np.zeros_like(Q)

    for i in range(n_blocks):
        Q_block = Q[:, i * block_size:(i + 1) * block_size, :]
        accum_attn = np.zeros((B, block_size, d))
        norm = np.zeros((B, block_size, 1))

        for j in range(n_blocks):
            K_block = K[:, j * block_size:(j + 1) * block_size, :]
            V_block = V[:, j * block_size:(j + 1) * block_size, :]
            scores = Q_block @ K_block.transpose(0, 2, 1) / np.sqrt(d)
            max_scores = scores.max(axis=-1, keepdims=True)
            exp_scores = np.exp(scores - max_scores)
            sum_exp = exp_scores.sum(axis=-1, keepdims=True)

            old_norm = norm
            norm = norm + sum_exp
            # Update output with safe normalization
            accum_attn = accum_attn * (old_norm / norm) + (exp_scores @ V_block) / norm

        out[:, i * block_size:(i + 1) * block_size, :] = accum_attn

    return out


if __name__ == "__main__":
    # StreamingLLM demo
    cache = StreamingLLMCache(sink_size=2, window_size=4)
    B, H, d = 2, 4, 8
    for step in range(10):
        k = np.random.randn(B, H, 1, d)
        v = np.random.randn(B, H, 1, d)
        cache.update(k, v)
        k_all, v_all = cache.get()
        print(f"Step {step:2d}: cache size = {k_all.shape[2]:2d} (sink=2, window=4)")

    print()

    # Ring Attention demo
    np.random.seed(42)
    B, T, d = 2, 8, 16
    Q = np.random.randn(B, T, d)
    K = np.random.randn(B, T, d)
    V = np.random.randn(B, T, d)

    out = ring_attention_block(Q, K, V, block_size=2)
    print(f"Ring Attention output: {out.shape}")
    print("Processed in blocks without materializing full T×T attention.")
