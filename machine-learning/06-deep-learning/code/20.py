"""06.20 - Transformer Variants: GPT, BERT, ViT, Performer, Linformer"""

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
        self.d_model, self.n_heads = d_model, n_heads
        self.d_k = d_model // n_heads
        self.W_Q = np.random.randn(d_model, d_model) * 0.01
        self.W_K = np.random.randn(d_model, d_model) * 0.01
        self.W_V = np.random.randn(d_model, d_model) * 0.01
        self.W_O = np.random.randn(d_model, d_model) * 0.01

    def forward(self, Q, K, V, mask=None):
        N, L, _ = Q.shape
        def split_heads(x, seq_len):
            return (x @ self.W_Q).reshape(N, seq_len, self.n_heads, self.d_k).transpose(0, 2, 1, 3)
        Q_h = split_heads(Q, Q.shape[1])
        K_h = split_heads(K, K.shape[1])
        V_h = split_heads(V, V.shape[1])
        scores = Q_h @ K_h.transpose(0, 1, 3, 2) / np.sqrt(self.d_k)
        if mask is not None:
            scores = np.where(mask, scores, -1e9)
        attn = softmax(scores)
        out = attn @ V_h
        out = out.transpose(0, 2, 1, 3).reshape(N, L, self.d_model)
        return out @ self.W_O


class FeedForward:
    def __init__(self, d_model, d_ff):
        self.W1 = np.random.randn(d_model, d_ff) * 0.01
        self.W2 = np.random.randn(d_ff, d_model) * 0.01

    def forward(self, x):
        return gelu(x @ self.W1) @ self.W2


class DecoderBlock:
    def __init__(self, d_model, n_heads, d_ff):
        self.masked_attn = MultiHeadAttention(d_model, n_heads)
        self.cross_attn = MultiHeadAttention(d_model, n_heads)
        self.ffn = FeedForward(d_model, d_ff)
        self.norm1, self.norm2, self.norm3 = LayerNorm(d_model), LayerNorm(d_model), LayerNorm(d_model)

    def forward(self, x, enc_out, mask=None):
        x = x + self.masked_attn.forward(self.norm1.forward(x), self.norm1.forward(x), self.norm1.forward(x), mask)
        if enc_out is not None:
            x = x + self.cross_attn.forward(self.norm2.forward(x), self.norm2.forward(enc_out), self.norm2.forward(enc_out))
        x = x + self.ffn.forward(self.norm3.forward(x))
        return x


class GPT:
    def __init__(self, vocab_size, d_model, n_heads, n_layers, d_ff, max_len=128):
        self.token_embed = np.random.randn(vocab_size, d_model) * 0.01
        self.pos_embed = np.random.randn(max_len, d_model) * 0.01
        self.blocks = [DecoderBlock(d_model, n_heads, d_ff) for _ in range(n_layers)]
        self.ln = LayerNorm(d_model)
        self.head = np.random.randn(d_model, vocab_size) * 0.01

    def forward(self, tokens, mask=None):
        N, L = tokens.shape
        x = self.token_embed[tokens] + self.pos_embed[:L][None, :, :]
        for block in self.blocks:
            x = block.forward(x, None, mask)
        return softmax(x @ self.head, axis=-1)


class BERT:
    def __init__(self, vocab_size, d_model, n_heads, n_layers, d_ff, max_len=128):
        self.token_embed = np.random.randn(vocab_size, d_model) * 0.01
        self.seg_embed = np.random.randn(2, d_model) * 0.01
        self.pos_embed = np.random.randn(max_len, d_model) * 0.01
        self.enc_blocks = [DecoderBlock(d_model, n_heads, d_ff) for _ in range(n_layers)]
        self.ln = LayerNorm(d_model)
        self.mlm_head = np.random.randn(d_model, vocab_size) * 0.01

    def forward(self, tokens, seg_ids, mask=None):
        N, L = tokens.shape
        x = self.token_embed[tokens] + self.seg_embed[seg_ids] + self.pos_embed[:L][None, :, :]
        for block in self.enc_blocks:
            x = block.forward(x, None, mask)
        return softmax(x @ self.mlm_head, axis=-1)


class ViT:
    def __init__(self, img_size=32, patch_size=4, in_channels=3, d_model=64, n_heads=8, n_layers=6, d_ff=256, num_classes=10):
        n_patches = (img_size // patch_size) ** 2
        self.patch_size = patch_size
        self.proj = np.random.randn(in_channels * patch_size * patch_size, d_model) * 0.01
        self.cls_token = np.random.randn(1, 1, d_model) * 0.01
        self.pos_embed = np.random.randn(1, n_patches + 1, d_model) * 0.01
        self.blocks = [DecoderBlock(d_model, n_heads, d_ff) for _ in range(n_layers)]
        self.ln = LayerNorm(d_model)
        self.head = np.random.randn(d_model, num_classes) * 0.01

    def forward(self, x):
        N, C, H, W = x.shape
        P = self.patch_size
        patches = x.reshape(N, C, H // P, P, W // P, P).transpose(0, 2, 4, 1, 3, 5).reshape(N, -1, C * P * P)
        tokens = patches @ self.proj
        cls_tokens = np.tile(self.cls_token, (N, 1, 1))
        x = np.concatenate([cls_tokens, tokens], axis=1) + self.pos_embed
        for block in self.blocks:
            x = block.forward(x, None)
        x = self.ln.forward(x)
        return softmax(x[:, 0] @ self.head, axis=-1)


class Performer:
    def __init__(self, d_model, n_heads, d_ff=256, num_features=64):
        self.d_model = d_model
        self.num_features = num_features
        self.W_rand = np.random.randn(d_model, num_features) * 0.01
        self.ffn = FeedForward(d_model, d_ff)
        self.ln = LayerNorm(d_model)

    def _favor_plus(self, Q, K):
        Q_proj = Q @ self.W_rand
        K_proj = K @ self.W_rand
        Q_prime = np.exp(Q_proj - Q_proj.max(axis=-1, keepdims=True))
        K_prime = np.exp(K_proj - K_proj.max(axis=-1, keepdims=True))
        return Q_prime, K_prime

    def forward(self, Q, K, V):
        Q_p, K_p = self._favor_plus(Q, K)
        kv = K_p.transpose(0, 2, 1) @ V
        attn_out = Q_p @ kv
        normalizer = (Q_p * K_p.sum(axis=1, keepdims=True)).sum(axis=-1, keepdims=True)
        attn_out = attn_out / (normalizer + 1e-6)
        return self.ln.forward(Q + attn_out)

    def forward_ffn(self, x):
        return x + self.ffn.forward(self.ln.forward(x))


class Linformer:
    def __init__(self, d_model, n_heads, seq_len=64, k=16):
        self.k = k
        self.proj_K = np.random.randn(seq_len, k) * 0.01
        self.proj_V = np.random.randn(seq_len, k) * 0.01
        self.attn = MultiHeadAttention(d_model, n_heads)

    def forward(self, Q, K, V):
        K_proj = self.proj_K[:K.shape[1]].T @ K
        V_proj = self.proj_V[:V.shape[1]].T @ V
        return self.attn.forward(Q, K_proj, V_proj)


if __name__ == "__main__":
    np.random.seed(42)
    d_model, n_heads, d_ff = 64, 8, 256
    causal_mask = np.tril(np.ones((10, 10)))[None, None, :, :]

    gpt = GPT(100, d_model, n_heads, 2, d_ff)
    out = gpt.forward(np.random.randint(0, 100, (2, 10)), causal_mask)
    print(f"GPT:                input (2,10) -> output {out.shape}")

    bert = BERT(100, d_model, n_heads, 2, d_ff)
    out = bert.forward(np.random.randint(0, 100, (2, 10)), np.zeros((2, 10), dtype=int))
    print(f"BERT:               input (2,10) -> output {out.shape}")

    vit = ViT()
    out = vit.forward(np.random.randn(2, 3, 32, 32))
    print(f"ViT:                input (2,3,32,32) -> output {out.shape}")

    performer = Performer(d_model, n_heads)
    x = np.random.randn(2, 10, d_model)
    out = performer.forward(x, x, x)
    print(f"Performer:          input (2,10,64) -> output {out.shape}")

    linformer = Linformer(d_model, n_heads)
    out = linformer.forward(x, x, x)
    print(f"Linformer:          input (2,10,64) -> output {out.shape}")

    print("\nAll transformer variants implemented and tested.")
