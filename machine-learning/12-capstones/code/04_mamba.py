"""
12.04: Mamba from Scratch + Transformer Comparison
Implement the Mamba state-space model block and compare
perplexity/efficiency against a transformer of similar size.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional
import time


# ─────────────────────────────────────────────
# Shared utilities
# ─────────────────────────────────────────────

def silu(x: np.ndarray) -> np.ndarray:
    return x * (1.0 / (1.0 + np.exp(-x)))


def gelu(x: np.ndarray) -> np.ndarray:
    return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3)))


def softmax_cross_entropy(logits: np.ndarray, targets: np.ndarray) -> float:
    logits_max = logits.max(axis=-1, keepdims=True)
    logits_stable = logits - logits_max
    log_probs = logits_stable - np.log(np.sum(np.exp(logits_stable), axis=-1, keepdims=True))
    nll = -log_probs[np.arange(len(targets)), targets]
    return float(nll.mean())


def layer_norm(x: np.ndarray, gamma: np.ndarray, beta: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    mean = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    return gamma * (x - mean) / np.sqrt(var + eps) + beta


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
# Mamba SSM Core
# ─────────────────────────────────────────────

class MambaBlock:
    """Selective State-Space Model block from Gu & Dao (2023)."""
    def __init__(self, d_model: int, d_state: int = 16, d_conv: int = 4, expand: int = 2):
        self.d_model = d_model
        self.d_inner = d_model * expand
        self.d_state = d_state
        self.d_conv = d_conv

        scale = np.sqrt(2.0 / d_model)
        # Input projection -> 2 * d_inner (split into x and gate)
        self.in_proj = np.random.randn(d_model, 2 * self.d_inner).astype(np.float64) * scale

        # 1D convolution (causal)
        self.conv_w = np.random.randn(self.d_inner, 1, d_conv).astype(np.float64) * 0.1
        self.conv_b = np.zeros(self.d_inner, dtype=np.float64)

        # SSM parameters (input-dependent)
        self.x_proj = np.random.randn(self.d_inner, d_state + 3).astype(np.float64) * scale
        # dt, B, C projections

        # Learnable A matrix (log-space for stability)
        self.A_log = np.log(np.random.rand(d_state, self.d_inner).astype(np.float64) * 0.1)

        # D (skip connection)
        self.D = np.ones(self.d_inner, dtype=np.float64)

        # Output projection
        self.out_proj = np.random.randn(self.d_inner, d_model).astype(np.float64) * scale

        # Cache for inference
        self._conv_state = None
        self._ssm_state = None

    def _selective_scan(self, x: np.ndarray, dt: np.ndarray, A: np.ndarray,
                        B: np.ndarray, C: np.ndarray) -> np.ndarray:
        """
        Parallel selective scan using the associative scan algorithm.
        x: (B, L, D)
        dt: (B, L, D, 1)
        A: (D, N)
        B: (B, L, N)
        C: (B, L, N)
        """
        B_sz, L, D = x.shape
        N = A.shape[0]

        # Discretize A: A_bar = exp(dt * A)
        # dt has shape (B, L, D, 1), A has shape (N, D)
        # We want A_bar of shape (B, L, D, N)
        dt_expanded = dt  # (B, L, D, 1)
        A_expanded = A.T[None, None, :, :]  # (1, 1, D, N)
        A_bar = np.exp(dt_expanded * A_expanded)  # (B, L, D, N)

        # Discretize B: B_bar = dt * B  (Euler approx)
        B_bar = dt_expanded * B[:, :, None, :]  # (B, L, D, N)

        # Parallel scan
        # Initialize state h = 0
        h = np.zeros((B_sz, D, N), dtype=np.float64)
        ys = []

        for l in range(L):
            h = A_bar[:, l] * h + B_bar[:, l] * x[:, l, :, None]  # (B, D, N)
            y_l = (h * C[:, l, None, :]).sum(axis=-1)  # (B, D)
            ys.append(y_l)

        y = np.stack(ys, axis=1)  # (B, L, D)
        return y

    def forward(self, x: np.ndarray) -> np.ndarray:
        B, L, D = x.shape

        # Input projection
        x_proj = x @ self.in_proj
        x_inner, gate = np.split(x_proj, 2, axis=-1)  # both (B, L, D_inner)

        # 1D causal convolution
        conv_out = np.zeros_like(x_inner)
        # Simple causal conv implementation
        x_pad = np.pad(x_inner, ((0, 0), (self.d_conv - 1, 0), (0, 0)), mode='constant')
        for i in range(L):
            conv_out[:, i] = (x_pad[:, i:i + self.d_conv] * self.conv_w[:, 0, ::-1][None, :, :]).sum(axis=(-1, -2))
        x_conv = silu(conv_out + self.conv_b)

        # SSM parameters
        ssm_params = x_conv @ self.x_proj  # (B, L, D + 3)
        dt, B_proj, C_proj = np.split(ssm_params, [1, 1 + self.d_state], axis=-1)
        # dt: (B, L, 1), B: (B, L, D_state), C: (B, L, D_state)

        # dt activation: softplus
        dt = np.log(1 + np.exp(dt))  # (B, L, 1)
        dt = dt[:, :, :, None]  # (B, L, 1, 1)
        # Expand dt to D_inner dimension
        dt = dt.repeat(self.d_inner, axis=2)  # (B, L, D_inner, 1)

        A = -np.exp(self.A_log)  # (D_state, D_inner)

        y = self._selective_scan(x_conv, dt, A, B_proj, C_proj)  # (B, L, D_inner)

        # Skip connection (D)
        y = y + self.D * x_conv

        # Gate
        y = y * silu(gate)

        # Output projection
        out = y @ self.out_proj
        return out

    def parameters(self):
        return [self.in_proj, self.conv_w, self.conv_b, self.x_proj,
                self.A_log, self.D, self.out_proj]


class MambaStack:
    """Stack of Mamba blocks with residual connections and LayerNorm."""
    def __init__(self, vocab_size: int, d_model: int = 128, n_layers: int = 4,
                 d_state: int = 16, max_len: int = 128):
        self.d_model = d_model
        self.max_len = max_len

        self.token_embed = np.random.randn(vocab_size, d_model).astype(np.float64) * 0.02

        self.blocks = [MambaBlock(d_model, d_state) for _ in range(n_layers)]

        self.ln_gamma = np.ones(d_model, dtype=np.float64)
        self.ln_beta = np.zeros(d_model, dtype=np.float64)
        self.lm_head = np.random.randn(d_model, vocab_size).astype(np.float64) * 0.02

    def forward(self, idx: np.ndarray, targets: Optional[np.ndarray] = None) -> tuple:
        B, T = idx.shape
        x = self.token_embed[idx]  # (B, T, D)

        for block in self.blocks:
            x = x + block.forward(x)

        x = layer_norm(x, self.ln_gamma, self.ln_beta)
        logits = x @ self.lm_head

        if targets is not None:
            B, T, V = logits.shape
            loss = softmax_cross_entropy(logits.reshape(-1, V), targets.reshape(-1))
            return logits, loss
        return logits, None

    def generate(self, prompt: str, max_new_tokens: int = 50, temperature: float = 0.8,
                 top_k: int = 15) -> str:
        tokens = encode(prompt)
        generated = list(tokens)

        for _ in range(max_new_tokens):
            ctx = np.array(generated[-self.max_len:], dtype=np.int64)[None, :]
            logits, _ = self.forward(ctx)
            logits_last = logits[0, -1, :] / temperature

            if top_k > 0:
                indices = np.argpartition(logits_last, -top_k)[-top_k:]
                probs = np.zeros_like(logits_last)
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
        params = [self.token_embed, self.lm_head, self.ln_gamma, self.ln_beta]
        for block in self.blocks:
            params.extend(block.parameters())
        return params


# ─────────────────────────────────────────────
# Transformer baseline (simplified from 02)
# ─────────────────────────────────────────────

class TransformerBlock:
    def __init__(self, d_model: int, n_heads: int, d_ff: int):
        self.n_heads = n_heads
        self.d_k = d_model // n_heads

        scale = np.sqrt(2.0 / d_model)
        self.W_q = np.random.randn(d_model, d_model).astype(np.float64) * scale
        self.W_k = np.random.randn(d_model, d_model).astype(np.float64) * scale
        self.W_v = np.random.randn(d_model, d_model).astype(np.float64) * scale
        self.W_o = np.random.randn(d_model, d_model).astype(np.float64) * scale

        self.ln1_gamma = np.ones(d_model, dtype=np.float64)
        self.ln1_beta = np.zeros(d_model, dtype=np.float64)

        scale2 = np.sqrt(2.0 / d_model)
        self.W1 = np.random.randn(d_model, d_ff).astype(np.float64) * scale2
        self.b1 = np.zeros(d_ff, dtype=np.float64)
        self.W2 = np.random.randn(d_ff, d_model).astype(np.float64) * scale2
        self.b2 = np.zeros(d_model, dtype=np.float64)

        self.ln2_gamma = np.ones(d_model, dtype=np.float64)
        self.ln2_beta = np.zeros(d_model, dtype=np.float64)

        self._causal_mask = None

    def forward(self, x: np.ndarray, mask: Optional[np.ndarray] = None) -> np.ndarray:
        B, T, D = x.shape
        # Attention
        x_norm = layer_norm(x, self.ln1_gamma, self.ln1_beta)
        Q = x_norm @ self.W_q
        K = x_norm @ self.W_k
        V = x_norm @ self.W_v

        Q = Q.reshape(B, T, self.n_heads, self.d_k).transpose(0, 2, 1, 3)
        K = K.reshape(B, T, self.n_heads, self.d_k).transpose(0, 2, 1, 3)
        V = V.reshape(B, T, self.n_heads, self.d_k).transpose(0, 2, 1, 3)

        scores = Q @ K.transpose(0, 1, 3, 2) / np.sqrt(self.d_k)
        if mask is not None:
            scores = scores + mask

        attn = np.exp(scores - scores.max(axis=-1, keepdims=True))
        attn = attn / attn.sum(axis=-1, keepdims=True)
        out = attn @ V
        out = out.transpose(0, 2, 1, 3).reshape(B, T, D)
        x = x + out @ self.W_o

        # FFN
        x_norm2 = layer_norm(x, self.ln2_gamma, self.ln2_beta)
        ffn = gelu(x_norm2 @ self.W1 + self.b1) @ self.W2 + self.b2
        x = x + ffn
        return x

    def parameters(self):
        return [self.W_q, self.W_k, self.W_v, self.W_o,
                self.ln1_gamma, self.ln1_beta,
                self.W1, self.b1, self.W2, self.b2,
                self.ln2_gamma, self.ln2_beta]


class TransformerLM:
    def __init__(self, vocab_size: int, d_model: int = 128, n_layers: int = 4,
                 n_heads: int = 4, d_ff: int = 512, max_len: int = 128):
        self.d_model = d_model
        self.max_len = max_len
        self.n_heads = n_heads

        self.token_embed = np.random.randn(vocab_size, d_model).astype(np.float64) * 0.02
        # Positional encoding (sinusoidal)
        pos = np.arange(max_len)[:, None]
        div = np.exp(np.arange(0, d_model, 2) * -np.log(10000.0) / d_model)
        self.pos_embed = np.zeros((max_len, d_model), dtype=np.float64)
        self.pos_embed[:, 0::2] = np.sin(pos * div)
        self.pos_embed[:, 1::2] = np.cos(pos * div)

        self.blocks = [TransformerBlock(d_model, n_heads, d_ff) for _ in range(n_layers)]
        self.ln_f_gamma = np.ones(d_model, dtype=np.float64)
        self.ln_f_beta = np.zeros(d_model, dtype=np.float64)
        self.lm_head = np.random.randn(d_model, vocab_size).astype(np.float64) * 0.02

        self._causal_mask = np.triu(np.full((max_len, max_len), -np.inf), k=1)

    def forward(self, idx: np.ndarray, targets: Optional[np.ndarray] = None) -> tuple:
        B, T = idx.shape
        x = self.token_embed[idx] + self.pos_embed[None, :T, :]
        mask = self._causal_mask[None, None, :T, :T]

        for block in self.blocks:
            x = block.forward(x, mask)

        x = layer_norm(x, self.ln_f_gamma, self.ln_f_beta)
        logits = x @ self.lm_head

        if targets is not None:
            loss = softmax_cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1))
            return logits, loss
        return logits, None

    def generate(self, prompt: str, max_new_tokens: int = 50, temperature: float = 0.8,
                 top_k: int = 15) -> str:
        tokens = encode(prompt)
        generated = list(tokens)

        for _ in range(max_new_tokens):
            ctx = np.array(generated[-self.max_len:], dtype=np.int64)[None, :]
            logits, _ = self.forward(ctx)
            logits_last = logits[0, -1, :] / temperature

            if top_k > 0:
                indices = np.argpartition(logits_last, -top_k)[-top_k:]
                probs = np.zeros_like(logits_last)
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
        params = [self.token_embed, self.pos_embed, self.lm_head,
                  self.ln_f_gamma, self.ln_f_beta]
        for block in self.blocks:
            params.extend(block.parameters())
        return params


# ─────────────────────────────────────────────
# Optimizer
# ─────────────────────────────────────────────

class SimpleOptimizer:
    def __init__(self, params, lr: float = 3e-4):
        self.params = params
        self.lr = lr

    def step(self, grads):
        for p, g in zip(self.params, grads):
            p -= self.lr * g


# ─────────────────────────────────────────────
# Data
# ─────────────────────────────────────────────

def load_text():
    texts = [
        "The quick brown fox jumps over the lazy dog. ",
        "Machine learning is transforming every industry. ",
        "Neural networks learn patterns from data. ",
        "Transformers use attention mechanisms for processing sequences. ",
        "The cat sat on the mat and watched the birds. ",
        "Deep learning requires large datasets and compute. ",
        "Natural language processing enables computers to understand text. ",
        "Computer vision helps machines see and interpret images. ",
        "Reinforcement learning trains agents through rewards. ",
        "State space models offer an alternative to transformers. ",
        "Mamba uses selective state spaces for efficient sequence modeling. ",
        "The sun set over the mountains in a blaze of orange. ",
        "Python is widely used for machine learning development. ",
        "Mathematics provides the foundation for all ML algorithms. ",
        "Data science combines statistics, programming, and domain knowledge. ",
        "Artificial intelligence aims to create intelligent systems. ",
    ]
    return ' '.join(texts)


def collect_gradients(model, x_batch, y_batch, eps=1e-4):
    """Compute gradients via finite differences."""
    params = model.parameters()
    grads = [np.zeros_like(p) for p in params]
    base_logits, base_loss = model.forward(x_batch, y_batch)
    base_loss_val = base_loss if base_loss is not None else 0.0

    for j, p in enumerate(params):
        grad = np.zeros_like(p)
        for idx in np.ndindex(p.shape[:min(4, p.ndim)]):
            orig = p[idx]
            p[idx] = orig + eps
            _, loss_p = model.forward(x_batch, y_batch)
            p[idx] = orig - eps
            _, loss_m = model.forward(x_batch, y_batch)
            grad[idx] = (loss_p - loss_m) / (2 * eps)
            p[idx] = orig
        grads[j] = grad
    return grads


# ─────────────────────────────────────────────
# Training and comparison
# ─────────────────────────────────────────────

def train_model(model, text, epochs=30, batch_size=8, seq_len=64, lr=1e-4):
    params = model.parameters()
    optim = SimpleOptimizer(params, lr)
    loss_history = []

    tokens = encode(text)
    data_len = len(tokens)

    for epoch in range(epochs):
        perm = np.random.permutation(max(1, data_len - seq_len))
        epoch_loss = 0.0
        n_batches = 0

        for start_idx in perm[:10]:  # limit batches for speed
            if start_idx + seq_len + 1 >= data_len:
                continue
            x = tokens[start_idx:start_idx + seq_len][None, :]
            y = tokens[start_idx + 1:start_idx + seq_len + 1][None, :]

            _, loss = model.forward(x, y)

            # Compute gradients
            grads = collect_gradients(model, x, y)
            optim.step(grads)

            epoch_loss += loss
            n_batches += 1

        avg_loss = epoch_loss / max(n_batches, 1)
        loss_history.append(avg_loss)

        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch+1:2d}/{epochs} | Loss: {avg_loss:.4f}")

    return loss_history


def benchmark_speed(model, seq_len: int, n_tokens: int = 1000):
    """Measure tokens/second for forward pass."""
    B = 4
    x = np.random.randint(0, VOCAB_SIZE, size=(B, seq_len)).astype(np.int64)

    # Warmup
    for _ in range(5):
        model.forward(x)

    n_repeats = max(1, n_tokens // (B * seq_len))
    start = time.time()
    for _ in range(n_repeats):
        model.forward(x)
    elapsed = time.time() - start

    tokens_processed = B * seq_len * n_repeats
    return tokens_processed / elapsed


def count_params(model):
    return sum(p.size for p in model.parameters())


def main():
    np.random.seed(42)
    text = load_text()
    d_model = 96
    n_layers = 4

    print("=" * 60)
    print("MAMBA vs TRANSFORMER COMPARISON")
    print("=" * 60)

    # --- Mamba ---
    print("\n[1] Building Mamba model...")
    mamba = MambaStack(VOCAB_SIZE, d_model, n_layers, d_state=16, max_len=64)
    mamba_params = count_params(mamba)
    print(f"    Parameters: {mamba_params:,}")

    print("\n[2] Training Mamba...")
    mamba_loss = train_model(mamba, text, epochs=20, lr=1e-4)

    # --- Transformer ---
    print("\n[3] Building Transformer model...")
    transformer = TransformerLM(VOCAB_SIZE, d_model, n_layers, n_heads=4,
                                d_ff=d_model * 4, max_len=64)
    tf_params = count_params(transformer)
    print(f"    Parameters: {tf_params:,}")

    print("\n[4] Training Transformer...")
    tf_loss = train_model(transformer, text, epochs=20, lr=1e-4)

    # --- Comparison ---
    print("\n" + "=" * 60)
    print("COMPARISON RESULTS")
    print("=" * 60)
    print(f"\n{'Metric':<20} {'Mamba':<20} {'Transformer':<20}")
    print("-" * 60)
    print(f"{'Parameters':<20} {mamba_params:<20,} {tf_params:<20,}")
    print(f"{'Final Loss (Mamba)':<20} {mamba_loss[-1]:<20.4f} {'':<20}")
    print(f"{'Final Loss (TF)':<20} {'':<20} {tf_loss[-1]:<20.4f}")

    # Speed benchmark at different lengths
    for seq_len in [16, 32, 64]:
        mamba_speed = benchmark_speed(mamba, seq_len)
        tf_speed = benchmark_speed(transformer, seq_len)
        speedup = mamba_speed / tf_speed if tf_speed > 0 else 0
        print(f"\nSpeed at L={seq_len:<3}: {mamba_speed:<10.0f} tok/s vs {tf_speed:<10.0f} tok/s (Mamba {speedup:.2f}x)")

    # Generation
    print("\n--- Mamba Generation ---")
    print(mamba.generate("Machine learning", max_new_tokens=40, temperature=0.8, top_k=10))

    print("\n--- Transformer Generation ---")
    print(transformer.generate("Machine learning", max_new_tokens=40, temperature=0.8, top_k=10))

    # Plot training curves
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    axes[0].plot(mamba_loss, 'b-', linewidth=2, label='Mamba')
    axes[0].plot(tf_loss, 'r-', linewidth=2, label='Transformer')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Training Loss')
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # Speed comparison bar chart
    speeds_mamba = [benchmark_speed(mamba, l) for l in [16, 32, 64]]
    speeds_tf = [benchmark_speed(transformer, l) for l in [16, 32, 64]]
    x = np.arange(3)
    width = 0.35
    axes[1].bar(x - width/2, speeds_mamba, width, label='Mamba', color='blue', alpha=0.7)
    axes[1].bar(x + width/2, speeds_tf, width, label='Transformer', color='red', alpha=0.7)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(['L=16', 'L=32', 'L=64'])
    axes[1].set_ylabel('Tokens/sec')
    axes[1].set_title('Speed Comparison')
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('../../assets/phase12/04_mamba_comparison.png', dpi=150)
    plt.close()
    print("\nSaved 04_mamba_comparison.png")


if __name__ == '__main__':
    main()
