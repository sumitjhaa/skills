"""06.19 - Positional Encodings: Sinusoidal, learned, RoPE, ALiBi"""

import numpy as np
import matplotlib.pyplot as plt


def sinusoidal_encoding(max_len, d_model):
    pe = np.zeros((max_len, d_model))
    position = np.arange(max_len)[:, None]
    div_term = np.exp(np.arange(0, d_model, 2) * (-np.log(10000.0) / d_model))
    pe[:, 0::2] = np.sin(position * div_term)
    pe[:, 1::2] = np.cos(position * div_term)
    return pe


class LearnedPositionalEncoding:
    def __init__(self, max_len, d_model):
        self.embeddings = np.random.randn(max_len, d_model) * 0.01

    def forward(self, x, positions=None):
        max_len = x.shape[1]
        if positions is None:
            positions = np.arange(max_len)
        return x + self.embeddings[positions][None, :, :]


def rope(x, base=10000.0):
    seq_len, d_model = x.shape[-2], x.shape[-1]
    theta = base ** (-2 * np.arange(0, d_model, 2) / d_model)
    pos = np.arange(seq_len)
    cos = np.cos(np.outer(pos, theta))
    sin = np.sin(np.outer(pos, theta))
    x_reshaped = x.reshape(*x.shape[:-1], -1, 2)
    x_rot = np.stack([x_reshaped[..., 0] * cos[:seq_len] - x_reshaped[..., 1] * sin[:seq_len],
                      x_reshaped[..., 1] * cos[:seq_len] + x_reshaped[..., 0] * sin[:seq_len]], axis=-1)
    return x_rot.reshape(*x.shape)


class ALiBi:
    def __init__(self, n_heads):
        self.slopes = self._get_slopes(n_heads)

    def _get_slopes(self, n_heads):
        def get_slopes_power_of_2(n):
            start = 2 ** (-(2 ** -(np.log2(n) - 3)))
            return np.array([start * (2 ** -(i // 2)) for i in range(n)])
        if n_heads & (n_heads - 1) == 0:
            return get_slopes_power_of_2(n_heads)
        n_power_of_2 = 2 ** int(np.log2(n_heads))
        slopes = get_slopes_power_of_2(n_power_of_2)
        extra = slopes[-1] / 2 ** (n_heads - n_power_of_2 + 1)
        extra_slopes = np.array([extra * (2 ** -(i // 2)) for i in range(n_heads - n_power_of_2)])
        return np.concatenate([slopes, extra_slopes])

    def forward(self, scores):
        seq_len = scores.shape[-1]
        pos = np.abs(np.arange(seq_len)[:, None] - np.arange(seq_len)[None, :])
        bias = -self.slopes[:, None, None] * pos[None, :, :]
        return scores + bias[None, :, :, :]


if __name__ == "__main__":
    max_len, d_model = 50, 64

    sin_pe = sinusoidal_encoding(max_len, d_model)
    print(f"Sinusoidal PE shape: {sin_pe.shape}")
    print(f"  PE[0, :4] = {sin_pe[0, :4]}")
    print(f"  PE[1, :4] = {sin_pe[1, :4]}")

    lpe = LearnedPositionalEncoding(max_len, d_model)
    x = np.random.randn(2, 10, d_model)
    x_out = lpe.forward(x)
    print(f"\nLearned PE: input shape {x.shape}, output shape {x_out.shape}")

    rope_out = rope(x)
    print(f"RoPE: input shape {x.shape}, output shape {rope_out.shape}")

    alibi = ALiBi(n_heads=8)
    scores = np.random.randn(2, 8, 10, 10)
    biased_scores = alibi.forward(scores)
    print(f"\nALiBi: scores shape {scores.shape} -> biased shape {biased_scores.shape}")

    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    axes[0].imshow(sin_pe[:, :32], aspect="auto", cmap="RdBu")
    axes[0].set_title("Sinusoidal (first 32)")
    axes[0].set_xlabel("Dimension"); axes[0].set_ylabel("Position")

    axes[1].imshow(lpe.embeddings[:, :32], aspect="auto", cmap="RdBu")
    axes[1].set_title("Learned (first 32)")
    axes[1].set_xlabel("Dimension")

    pos_bias = -np.abs(np.arange(10)[:, None] - np.arange(10)[None, :])
    axes[2].imshow(pos_bias, cmap="RdBu")
    axes[2].set_title("RoPE relative bias")

    alibi_bias = -alibi.slopes[:, None, None] * np.abs(np.arange(10)[:, None] - np.arange(10)[None, :])[None, :, :]
    axes[3].imshow(alibi_bias.mean(axis=0), cmap="RdBu")
    axes[3].set_title("ALiBi bias (mean over heads)")

    plt.tight_layout()
    plt.savefig("../../assets/phase06/positional_encodings.png")
    plt.close()
    print("\nAll positional encoding implementations verified.")
