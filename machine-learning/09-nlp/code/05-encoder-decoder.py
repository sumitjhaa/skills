"""
09.05 Encoder-Decoder — Simplified T5-style Transformer Block
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


def softmax(x, axis=-1):
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / np.sum(e, axis=axis, keepdims=True)


def layer_norm(x, eps=1e-6):
    mean = np.mean(x, axis=-1, keepdims=True)
    var = np.var(x, axis=-1, keepdims=True)
    return (x - mean) / np.sqrt(var + eps)


class SelfAttention:
    def __init__(self, d_model, n_heads):
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_head = d_model // n_heads
        scale = np.sqrt(2.0 / d_model)
        self.W_q = np.random.randn(d_model, d_model) * scale
        self.W_k = np.random.randn(d_model, d_model) * scale
        self.W_v = np.random.randn(d_model, d_model) * scale
        self.W_o = np.random.randn(d_model, d_model) * scale

    def __call__(self, x, mask=None):
        B, T, D = x.shape
        Q = x @ self.W_q
        K = x @ self.W_k
        V = x @ self.W_v

        Q = Q.reshape(B, T, self.n_heads, self.d_head).transpose(0, 2, 1, 3)
        K = K.reshape(B, T, self.n_heads, self.d_head).transpose(0, 2, 1, 3)
        V = V.reshape(B, T, self.n_heads, self.d_head).transpose(0, 2, 1, 3)

        scores = Q @ K.transpose(0, 1, 3, 2) / np.sqrt(self.d_head)
        if mask is not None:
            scores = scores + mask
        attn = softmax(scores, axis=-1)
        out = attn @ V
        out = out.transpose(0, 2, 1, 3).reshape(B, T, D)
        return out @ self.W_o


class CrossAttention:
    def __init__(self, d_model, n_heads):
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_head = d_model // n_heads
        scale = np.sqrt(2.0 / d_model)
        self.W_q = np.random.randn(d_model, d_model) * scale
        self.W_k = np.random.randn(d_model, d_model) * scale
        self.W_v = np.random.randn(d_model, d_model) * scale
        self.W_o = np.random.randn(d_model, d_model) * scale

    def __call__(self, x, enc_out, mask=None):
        B, T, D = x.shape
        _, S, _ = enc_out.shape
        Q = x @ self.W_q
        K = enc_out @ self.W_k
        V = enc_out @ self.W_v

        Q = Q.reshape(B, T, self.n_heads, self.d_head).transpose(0, 2, 1, 3)
        K = K.reshape(B, S, self.n_heads, self.d_head).transpose(0, 2, 1, 3)
        V = V.reshape(B, S, self.n_heads, self.d_head).transpose(0, 2, 1, 3)

        scores = Q @ K.transpose(0, 1, 3, 2) / np.sqrt(self.d_head)
        if mask is not None:
            scores = scores + mask
        attn = softmax(scores, axis=-1)
        out = attn @ V
        out = out.transpose(0, 2, 1, 3).reshape(B, T, D)
        return out @ self.W_o


class FFN:
    def __init__(self, d_model, d_ff):
        scale = np.sqrt(2.0 / d_model)
        self.W1 = np.random.randn(d_model, d_ff) * scale
        self.W2 = np.random.randn(d_ff, d_model) * scale

    def __call__(self, x):
        hidden = np.maximum(0, x @ self.W1)  # ReLU (simplified, T5 uses GeGLU)
        return hidden @ self.W2


class TransformerEncoderBlock:
    def __init__(self, d_model, n_heads, d_ff):
        self.self_attn = SelfAttention(d_model, n_heads)
        self.ffn = FFN(d_model, d_ff)

    def __call__(self, x, mask=None):
        x = x + self.self_attn(layer_norm(x), mask)
        x = x + self.ffn(layer_norm(x))
        return x


class TransformerDecoderBlock:
    def __init__(self, d_model, n_heads, d_ff):
        self.self_attn = SelfAttention(d_model, n_heads)
        self.cross_attn = CrossAttention(d_model, n_heads)
        self.ffn = FFN(d_model, d_ff)

    def __call__(self, x, enc_out, self_mask=None, cross_mask=None):
        x = x + self.self_attn(layer_norm(x), self_mask)
        x = x + self.cross_attn(layer_norm(x), enc_out, cross_mask)
        x = x + self.ffn(layer_norm(x))
        return x


if __name__ == "__main__":
    d_model, n_heads, d_ff = 64, 4, 128
    enc = TransformerEncoderBlock(d_model, n_heads, d_ff)
    dec = TransformerDecoderBlock(d_model, n_heads, d_ff)

    B, T_enc, T_dec = 2, 6, 4
    enc_in = np.random.randn(B, T_enc, d_model)
    dec_in = np.random.randn(B, T_dec, d_model)

    causal_mask = np.triu(np.full((T_dec, T_dec), -1e9), k=1)
    causal_mask = causal_mask[np.newaxis, np.newaxis, :, :]

    enc_out = enc(enc_in)
    dec_out = dec(dec_in, enc_out, self_mask=causal_mask)

    print(f"Encoder input:  {enc_in.shape}")
    print(f"Encoder output: {enc_out.shape}")
    print(f"Decoder output: {dec_out.shape}")
    print("T5-style encoder-decoder block forward pass successful.")
