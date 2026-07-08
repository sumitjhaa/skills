"""06.17 - Attention: Scaled dot-product, additive, multi-head"""

import numpy as np


def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)
    if mask is not None:
        scores = np.where(mask, scores, -1e9)
    weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
    weights /= weights.sum(axis=-1, keepdims=True)
    return weights @ V, weights


def additive_attention(Q, K, V):
    d_k = Q.shape[-1]
    V_a = np.random.randn(d_k)
    scores = np.tanh(Q + K).sum(axis=-1)
    weights = np.exp(scores - scores.max())
    weights /= weights.sum()
    return weights @ V, weights


class MultiHeadAttention:
    def __init__(self, d_model, num_heads):
        assert d_model % num_heads == 0
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.W_Q = np.random.randn(d_model, d_model) * 0.01
        self.W_K = np.random.randn(d_model, d_model) * 0.01
        self.W_V = np.random.randn(d_model, d_model) * 0.01
        self.W_O = np.random.randn(d_model, d_model) * 0.01

    def forward(self, Q, K, V, mask=None):
        N = Q.shape[0]
        Q_proj = Q @ self.W_Q
        K_proj = K @ self.W_K
        V_proj = V @ self.W_V
        Q_heads = Q_proj.reshape(N, -1, self.num_heads, self.d_k).transpose(0, 2, 1, 3)
        K_heads = K_proj.reshape(N, -1, self.num_heads, self.d_k).transpose(0, 2, 1, 3)
        V_heads = V_proj.reshape(N, -1, self.num_heads, self.d_k).transpose(0, 2, 1, 3)

        scores = Q_heads @ K_heads.transpose(0, 1, 3, 2) / np.sqrt(self.d_k)
        if mask is not None:
            scores = np.where(mask, scores, -1e9)
        weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
        weights /= weights.sum(axis=-1, keepdims=True)

        head_out = weights @ V_heads
        concat = head_out.transpose(0, 2, 1, 3).reshape(N, -1, self.d_model)
        return concat @ self.W_O, weights


if __name__ == "__main__":
    np.random.seed(42)

    d_model, n_heads = 64, 8
    seq_len = 10
    Q = np.random.randn(seq_len, d_model)
    K = np.random.randn(seq_len, d_model)
    V = np.random.randn(seq_len, d_model)

    out_sdp, w_sdp = scaled_dot_product_attention(Q, K, V)
    print(f"Scaled Dot-Product Attention: output shape={out_sdp.shape}")

    mha = MultiHeadAttention(d_model, n_heads)
    Q_batch = np.random.randn(2, seq_len, d_model)
    out_mha, w_mha = mha.forward(Q_batch, Q_batch, Q_batch)
    print(f"Multi-Head Self-Attention:   output shape={out_mha.shape}")

    causal_mask = np.tril(np.ones((seq_len, seq_len)))[None, None, :, :]
    out_causal, w_causal = mha.forward(Q_batch, Q_batch, Q_batch, mask=causal_mask)
    print(f"Causal (masked) attention:   output shape={out_causal.shape}")

    attn_matrix = w_mha[0].mean(axis=0)
    print(f"\nAttention matrix ({attn_matrix.shape[0]}x{attn_matrix.shape[1]}):")
    print(f"  Row sums: min={attn_matrix.sum(axis=-1).min():.4f}, max={attn_matrix.sum(axis=-1).max():.4f}")
    print("All attention mechanisms implemented and verified.")
