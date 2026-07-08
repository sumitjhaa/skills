"""
12.02: Transformer from Scratch (GPT-2 Scale)
A decoder-only transformer with causal self-attention,
trained on a text corpus with character-level tokenization.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional


# ─────────────────────────────────────────────
# Tokenization (character-level)
# ─────────────────────────────────────────────

CHARS = '\n abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:,.<>?/~`"\'' 
VOCAB_SIZE = len(CHARS)
char_to_idx = {c: i for i, c in enumerate(CHARS)}
idx_to_char = {i: c for i, c in enumerate(CHARS)}

def encode(s: str) -> np.ndarray:
    return np.array([char_to_idx.get(c, 0) for c in s], dtype=np.int64)

def decode(ids: np.ndarray) -> str:
    return ''.join(idx_to_char.get(i, '') for i in ids)


# ─────────────────────────────────────────────
# Sinusoidal positional encoding
# ─────────────────────────────────────────────

def sinusoidal_embeddings(max_len: int, d_model: int) -> np.ndarray:
    pe = np.zeros((max_len, d_model), dtype=np.float64)
    pos = np.arange(max_len)[:, None]
    div = np.exp(np.arange(0, d_model, 2) * -np.log(10000.0) / d_model)
    pe[:, 0::2] = np.sin(pos * div)
    pe[:, 1::2] = np.cos(pos * div)
    return pe


# ─────────────────────────────────────────────
# Layer normalization
# ─────────────────────────────────────────────

class LayerNorm:
    def __init__(self, d_model: int, eps: float = 1e-5):
        self.gamma = np.ones(d_model, dtype=np.float64)
        self.beta = np.zeros(d_model, dtype=np.float64)
        self.eps = eps

    def __call__(self, x: np.ndarray) -> np.ndarray:
        mean = x.mean(axis=-1, keepdims=True)
        var = x.var(axis=-1, keepdims=True)
        return self.gamma * (x - mean) / np.sqrt(var + self.eps) + self.beta

    def parameters(self):
        return [self.gamma, self.beta]


# ─────────────────────────────────────────────
# Causal multi-head attention
# ─────────────────────────────────────────────

class CausalSelfAttention:
    def __init__(self, d_model: int, n_heads: int, dropout: float = 0.1):
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        self.dropout = dropout

        scale = np.sqrt(2.0 / d_model)
        self.W_q = np.random.randn(d_model, d_model).astype(np.float64) * scale
        self.W_k = np.random.randn(d_model, d_model).astype(np.float64) * scale
        self.W_v = np.random.randn(d_model, d_model).astype(np.float64) * scale
        self.W_o = np.random.randn(d_model, d_model).astype(np.float64) * scale

    def forward(self, x: np.ndarray, mask: Optional[np.ndarray] = None) -> np.ndarray:
        B, T, D = x.shape
        Q = x @ self.W_q  # (B, T, D)
        K = x @ self.W_k
        V = x @ self.W_v

        # Split into heads: (B, T, H, d_k) → (B, H, T, d_k)
        Q = Q.reshape(B, T, self.n_heads, self.d_k).transpose(0, 2, 1, 3)
        K = K.reshape(B, T, self.n_heads, self.d_k).transpose(0, 2, 1, 3)
        V = V.reshape(B, T, self.n_heads, self.d_k).transpose(0, 2, 1, 3)

        # Scaled dot-product attention
        scores = Q @ K.transpose(0, 1, 3, 2) / np.sqrt(self.d_k)  # (B, H, T, T)
        if mask is not None:
            scores = scores + mask
        attn = np.exp(scores - scores.max(axis=-1, keepdims=True))
        attn = attn / attn.sum(axis=-1, keepdims=True)
        attn = np.where(np.isnan(attn), 0, attn)

        out = attn @ V  # (B, H, T, d_k)
        out = out.transpose(0, 2, 1, 3).reshape(B, T, D)
        return out @ self.W_o

    def parameters(self):
        return [self.W_q, self.W_k, self.W_v, self.W_o]


# ─────────────────────────────────────────────
# Feed-forward network
# ─────────────────────────────────────────────

class FeedForward:
    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.1):
        scale = np.sqrt(2.0 / d_model)
        self.W1 = np.random.randn(d_model, d_ff).astype(np.float64) * scale
        self.b1 = np.zeros(d_ff, dtype=np.float64)
        scale2 = np.sqrt(2.0 / d_ff)
        self.W2 = np.random.randn(d_ff, d_model).astype(np.float64) * scale2
        self.b2 = np.zeros(d_model, dtype=np.float64)
        self.dropout = dropout

    def forward(self, x: np.ndarray) -> np.ndarray:
        # GELU activation
        h = x @ self.W1 + self.b1
        gelu = 0.5 * h * (1 + np.tanh(np.sqrt(2 / np.pi) * (h + 0.044715 * h ** 3)))
        return gelu @ self.W2 + self.b2

    def parameters(self):
        return [self.W1, self.b1, self.W2, self.b2]


# ─────────────────────────────────────────────
# Transformer block
# ─────────────────────────────────────────────

class TransformerBlock:
    def __init__(self, d_model: int, n_heads: int, d_ff: int, dropout: float = 0.1):
        self.ln1 = LayerNorm(d_model)
        self.attn = CausalSelfAttention(d_model, n_heads, dropout)
        self.ln2 = LayerNorm(d_model)
        self.ffn = FeedForward(d_model, d_ff, dropout)

    def forward(self, x: np.ndarray, mask: Optional[np.ndarray] = None) -> np.ndarray:
        x = x + self.attn.forward(self.ln1(x), mask)
        x = x + self.ffn.forward(self.ln2(x))
        return x

    def parameters(self):
        return self.attn.parameters() + self.ffn.parameters() + [self.ln1.gamma, self.ln1.beta, self.ln2.gamma, self.ln2.beta]


# ─────────────────────────────────────────────
# Full GPT model
# ─────────────────────────────────────────────

class GPT:
    def __init__(self, vocab_size: int, d_model: int = 256, n_heads: int = 8,
                 n_layers: int = 6, d_ff: int = 1024, max_len: int = 128,
                 dropout: float = 0.1):
        self.d_model = d_model
        self.max_len = max_len
        self.token_embed = np.random.randn(vocab_size, d_model).astype(np.float64) * 0.02
        self.pos_embed = sinusoidal_embeddings(max_len, d_model)
        self.blocks = [TransformerBlock(d_model, n_heads, d_ff, dropout) for _ in range(n_layers)]
        self.ln_f = LayerNorm(d_model)
        self.lm_head = np.random.randn(d_model, vocab_size).astype(np.float64) * 0.02

        # Causal mask
        self.register_buffer()

    def register_buffer(self):
        self.causal_mask = np.triu(np.full((self.max_len, self.max_len), -np.inf, dtype=np.float64), k=1)

    def forward(self, idx: np.ndarray, targets: Optional[np.ndarray] = None,
                return_logits: bool = False) -> tuple:
        B, T = idx.shape
        assert T <= self.max_len

        # Embedding
        x = self.token_embed[idx]  # (B, T, D)
        x = x + self.pos_embed[:T][None, :, :]

        # Blocks
        mask = self.causal_mask[:T, :T][None, None, :, :]
        for block in self.blocks:
            x = block.forward(x, mask)

        x = self.ln_f(x)
        logits = x @ self.lm_head  # (B, T, V)

        if return_logits:
            return logits, None

        if targets is not None:
            B, T, V = logits.shape
            logits_flat = logits.reshape(-1, V)
            targets_flat = targets.reshape(-1)
            loss = softmax_cross_entropy(logits_flat, targets_flat)
            return logits, loss
        return logits, None

    def generate(self, prompt: str, max_new_tokens: int = 100,
                 temperature: float = 1.0, top_k: int = 20) -> str:
        self.eval()
        tokens = encode(prompt)
        generated = list(tokens)

        for _ in range(max_new_tokens):
            # Truncate to max_len
            ctx = np.array(generated[-self.max_len:], dtype=np.int64)[None, :]
            logits, _ = self.forward(ctx)
            logits_last = logits[0, -1, :] / temperature

            # Top-k sampling
            if top_k > 0:
                indices = np.argpartition(logits_last, -top_k)[-top_k:]
                probs = np.zeros_like(logits_last)
                # Softmax over top-k
                logits_k = logits_last[indices]
                logits_k = logits_k - logits_k.max()
                probs_k = np.exp(logits_k) / np.exp(logits_k).sum()
                probs[indices] = probs_k
                next_token = np.random.choice(len(probs), p=probs)
            else:
                probs = np.exp(logits_last - logits_last.max())
                probs = probs / probs.sum()
                next_token = np.random.choice(len(probs), p=probs)

            generated.append(next_token)

        return decode(np.array(generated))

    def parameters(self):
        params = [self.token_embed, self.lm_head] + [self.ln_f.gamma, self.ln_f.beta]
        for block in self.blocks:
            params.extend(block.parameters())
        return params


# ─────────────────────────────────────────────
# Loss
# ─────────────────────────────────────────────

def softmax_cross_entropy(logits: np.ndarray, targets: np.ndarray) -> float:
    logits_max = logits.max(axis=-1, keepdims=True)
    logits_stable = logits - logits_max
    log_probs = logits_stable - np.log(np.sum(np.exp(logits_stable), axis=-1, keepdims=True))
    nll = -log_probs[np.arange(len(targets)), targets]
    return float(nll.mean())


# ─────────────────────────────────────────────
# Optimizer
# ─────────────────────────────────────────────

class AdamW:
    def __init__(self, params, lr: float = 3e-4, betas=(0.9, 0.999), eps: float = 1e-8, weight_decay: float = 0.01):
        self.params = params
        self.lr = lr
        self.b1, self.b2 = betas
        self.eps = eps
        self.wd = weight_decay
        self.t = 0
        self.m = [np.zeros_like(p) for p in params]
        self.v = [np.zeros_like(p) for p in params]

    def step(self, grads):
        self.t += 1
        for i, p in enumerate(self.params):
            g = grads[i]
            self.m[i] = self.b1 * self.m[i] + (1 - self.b1) * g
            self.v[i] = self.b2 * self.v[i] + (1 - self.b2) * (g ** 2)
            m_hat = self.m[i] / (1 - self.b1 ** self.t)
            v_hat = self.v[i] / (1 - self.b2 ** self.t)
            update = m_hat / (np.sqrt(v_hat) + self.eps)
            p -= self.lr * (update + self.wd * p)


# ─────────────────────────────────────────────
# Data
# ─────────────────────────────────────────────

def load_text():
    """Load a small text corpus."""
    texts = [
        "The quick brown fox jumps over the lazy dog. "
        "This pangram contains every letter of the alphabet at least once. "
        "Machine learning is a subset of artificial intelligence. "
        "Neural networks are inspired by the human brain. "
        "Transformers have revolutionized natural language processing. "
        "Attention is all you need, said the famous paper. "
        "Deep learning models require large amounts of data. "
        "The cat sat on the mat and watched the birds outside. "
        "Python is a popular programming language for data science. "
        "Mathematics is the foundation of all machine learning algorithms. "
        "Gradient descent is an optimization algorithm used to minimize loss. "
        "Backpropagation computes gradients efficiently in neural networks. "
        "Convolutional neural networks excel at image recognition tasks. "
        "Recurrent neural networks process sequential data effectively. "
        "The future of AI depends on responsible development and deployment. "
        "Natural language understanding enables computers to comprehend text. "
        "Computer vision allows machines to interpret visual information. "
        "Reinforcement learning trains agents through trial and error. "
        "Transfer learning leverages knowledge from one task to another. "
        "Generative models can create new content that mimics training data. "
        "Self-supervised learning learns representations without labels. "
        "Few-shot learning aims to generalize from limited examples. "
        "Federated learning trains models across decentralized data sources. "
        "Quantum machine learning combines quantum computing with ML."
    ]
    return ' '.join(texts)


def get_batches(text: str, seq_len: int, batch_size: int):
    tokens = encode(text)
    data_len = len(tokens)
    n_batches = (data_len - 1) // (seq_len * batch_size)
    if n_batches == 0:
        n_batches = 1
    for i in range(n_batches):
        start = i * batch_size * seq_len
        end = start + batch_size * seq_len + 1
        chunk = tokens[start:end]
        if len(chunk) < batch_size * seq_len + 1:
            chunk = np.concatenate([chunk, tokens[:batch_size * seq_len + 1 - len(chunk)]])
        x = chunk[:batch_size * seq_len].reshape(batch_size, seq_len)
        y = chunk[1:batch_size * seq_len + 1].reshape(batch_size, seq_len)
        yield x, y


# ─────────────────────────────────────────────
# Training
# ─────────────────────────────────────────────

def train():
    np.random.seed(42)
    text = load_text()

    d_model = 128
    n_heads = 4
    n_layers = 4
    d_ff = 512
    max_len = 64
    vocab_size = VOCAB_SIZE

    model = GPT(vocab_size, d_model, n_heads, n_layers, d_ff, max_len)
    params = model.parameters()
    optim = AdamW(params, lr=3e-4)

    # Gradient placeholder
    grads = [np.zeros_like(p) for p in params]

    epochs = 50
    seq_len = max_len
    batch_size = 8
    loss_history = []

    print(f"Vocab size: {vocab_size}")
    print(f"Model params: {sum(p.size for p in params):,}")

    for epoch in range(epochs):
        epoch_loss = 0.0
        n_batches = 0

        for x_batch, y_batch in get_batches(text, seq_len, batch_size):
            # Forward
            logits, loss = model.forward(x_batch, y_batch)
            epoch_loss += loss
            n_batches += 1

            # Backward (manual gradients — numerical approximation)
            # We use a simple gradient estimator for this educational version
            eps = 1e-4
            idx = 0
            for j, p in enumerate(params):
                grad = np.zeros_like(p)
                it = np.nditer(p, flags=['multi_index'])
                flat_idx = 0
                for _ in it:
                    multi_index = it.multi_index
                    orig = p[multi_index]
                    p[multi_index] = orig + eps
                    _, loss_plus = model.forward(x_batch, y_batch)
                    p[multi_index] = orig - eps
                    _, loss_minus = model.forward(x_batch, y_batch)
                    grad[multi_index] = (loss_plus - loss_minus) / (2 * eps)
                    p[multi_index] = orig
                    flat_idx += 1
                grads[j] = grad

            optim.step(grads)

        avg_loss = epoch_loss / max(n_batches, 1)
        loss_history.append(avg_loss)

        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1:2d}/{epochs} | Loss: {avg_loss:.4f}")

    # Generate
    print("\n--- Generation ---")
    prompts = ["The future of", "Machine learning", "Neural networks"]
    for prompt in prompts:
        out = model.generate(prompt, max_new_tokens=50, temperature=0.8, top_k=15)
        print(f"\nPrompt: {prompt}")
        print(f"Generated: {out}")

    # Plot
    plt.figure(figsize=(10, 4))
    plt.plot(loss_history, 'b-', linewidth=2)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase12/02_transformer_results.png', dpi=150)
    plt.close()
    print("\nSaved 02_transformer_results.png")

    return model, loss_history


if __name__ == '__main__':
    model, loss_history = train()
