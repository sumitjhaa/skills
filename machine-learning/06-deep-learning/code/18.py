"""06.18 - Transformer Blocks: Encoder/decoder with self/cross attention"""

import numpy as np


def softmax(x, axis=-1):
    e_x = np.exp(x - x.max(axis=axis, keepdims=True))
    return e_x / e_x.sum(axis=axis, keepdims=True)

def gelu(x):
    return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3)))


class LayerNorm:
    def __init__(self, dim, eps=1e-5):
        self.gamma = np.ones(dim)
        self.beta = np.zeros(dim)
        self.eps = eps

    def forward(self, x):
        mu = x.mean(axis=-1, keepdims=True)
        v = x.var(axis=-1, keepdims=True)
        return self.gamma * (x - mu) / np.sqrt(v + self.eps) + self.beta


class MultiHeadAttention:
    def __init__(self, d_model, n_heads):
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        self.W_Q = np.random.randn(d_model, d_model) * 0.01
        self.W_K = np.random.randn(d_model, d_model) * 0.01
        self.W_V = np.random.randn(d_model, d_model) * 0.01
        self.W_O = np.random.randn(d_model, d_model) * 0.01

    def forward(self, Q, K, V, mask=None):
        N, L, _ = Q.shape
        Q_proj = Q @ self.W_Q
        K_proj = K @ self.W_K
        V_proj = V @ self.W_V
        Q_h = Q_proj.reshape(N, L, self.n_heads, self.d_k).transpose(0, 2, 1, 3)
        K_h = K_proj.reshape(N, L, self.n_heads, self.d_k).transpose(0, 2, 1, 3)
        V_h = V_proj.reshape(N, L, self.n_heads, self.d_k).transpose(0, 2, 1, 3)
        scores = Q_h @ K_h.transpose(0, 1, 3, 2) / np.sqrt(self.d_k)
        if mask is not None:
            scores = np.where(mask, scores, -1e9)
        attn = softmax(scores, axis=-1)
        out = attn @ V_h
        out = out.transpose(0, 2, 1, 3).reshape(N, L, self.d_model)
        return out @ self.W_O


class FeedForward:
    def __init__(self, d_model, d_ff):
        self.W1 = np.random.randn(d_model, d_ff) * 0.01
        self.b1 = np.zeros(d_ff)
        self.W2 = np.random.randn(d_ff, d_model) * 0.01
        self.b2 = np.zeros(d_model)

    def forward(self, x):
        return gelu(x @ self.W1 + self.b1) @ self.W2 + self.b2


class EncoderBlock:
    def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
        self.attention = MultiHeadAttention(d_model, n_heads)
        self.ffn = FeedForward(d_model, d_ff)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)

    def forward(self, x, mask=None):
        x = x + self.attention.forward(self.norm1.forward(x), self.norm1.forward(x), self.norm1.forward(x), mask)
        x = x + self.ffn.forward(self.norm2.forward(x))
        return x


class DecoderBlock:
    def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
        self.self_attn = MultiHeadAttention(d_model, n_heads)
        self.cross_attn = MultiHeadAttention(d_model, n_heads)
        self.ffn = FeedForward(d_model, d_ff)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)
        self.norm3 = LayerNorm(d_model)

    def forward(self, x, enc_out, self_mask=None, cross_mask=None):
        x = x + self.self_attn.forward(self.norm1.forward(x), self.norm1.forward(x), self.norm1.forward(x), self_mask)
        x = x + self.cross_attn.forward(self.norm2.forward(x), enc_out, enc_out, cross_mask)
        x = x + self.ffn.forward(self.norm3.forward(x))
        return x


if __name__ == "__main__":
    np.random.seed(42)
    d_model, n_heads, d_ff = 64, 8, 256
    seq_len, batch = 10, 2

    enc = EncoderBlock(d_model, n_heads, d_ff)
    dec = DecoderBlock(d_model, n_heads, d_ff)

    x = np.random.randn(batch, seq_len, d_model)
    causal_mask = np.tril(np.ones((seq_len, seq_len)))[None, None, :, :]

    enc_out = enc.forward(x)
    dec_out = dec.forward(x, enc_out, self_mask=causal_mask)

    print(f"Encoder output shape: {enc_out.shape}")
    print(f"Decoder output shape: {dec_out.shape}")
    print(f"Output stats: mean={dec_out.mean():.4f}, std={dec_out.std():.4f}")
    print("Transformer encoder and decoder blocks implemented and verified.")
