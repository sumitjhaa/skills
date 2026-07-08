"""
12.05: RLHF / DPO from Scratch
Implement Direct Preference Optimization (DPO) and PPO-based RLHF
for aligning a small language model.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, List, Tuple


# ─────────────────────────────────────────────
# Shared Utilities
# ─────────────────────────────────────────────

CHARS = '\n abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:,.<>?/~`"\'' 
VOCAB_SIZE = len(CHARS)
char_to_idx = {c: i for i, c in enumerate(CHARS)}
idx_to_char = {i: c for i, c in enumerate(CHARS)}

def encode(s: str) -> np.ndarray:
    return np.array([char_to_idx.get(c, 0) for c in s], dtype=np.int64)

def decode(ids: np.ndarray) -> str:
    return ''.join(idx_to_char.get(i, '') for i in ids)

def layer_norm(x, gamma, beta, eps=1e-5):
    mean = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    return gamma * (x - mean) / np.sqrt(var + eps) + beta

def gelu(x):
    return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3)))

def softmax_cross_entropy(logits, targets):
    logits_max = logits.max(axis=-1, keepdims=True)
    logits_stable = logits - logits_max
    log_probs = logits_stable - np.log(np.sum(np.exp(logits_stable), axis=-1, keepdims=True))
    nll = -log_probs[np.arange(len(targets)), targets]
    return float(nll.mean())


# ─────────────────────────────────────────────
# Small Transformer LM
# ─────────────────────────────────────────────

class TransformerBlock:
    def __init__(self, d_model, n_heads, d_ff):
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        scale = np.sqrt(2.0 / d_model)
        self.W_q = np.random.randn(d_model, d_model).astype(np.float64) * scale
        self.W_k = np.random.randn(d_model, d_model).astype(np.float64) * scale
        self.W_v = np.random.randn(d_model, d_model).astype(np.float64) * scale
        self.W_o = np.random.randn(d_model, d_model).astype(np.float64) * scale
        self.ln1_g = np.ones(d_model, dtype=np.float64)
        self.ln1_b = np.zeros(d_model, dtype=np.float64)
        scale2 = np.sqrt(2.0 / d_model)
        self.W1 = np.random.randn(d_model, d_ff).astype(np.float64) * scale2
        self.b1 = np.zeros(d_ff, dtype=np.float64)
        self.W2 = np.random.randn(d_ff, d_model).astype(np.float64) * scale2
        self.b2 = np.zeros(d_model, dtype=np.float64)
        self.ln2_g = np.ones(d_model, dtype=np.float64)
        self.ln2_b = np.zeros(d_model, dtype=np.float64)

    def forward(self, x, mask=None):
        B, T, D = x.shape
        x_n = layer_norm(x, self.ln1_g, self.ln1_b)
        Q = x_n @ self.W_q
        K = x_n @ self.W_k
        V = x_n @ self.W_v
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
        x_n2 = layer_norm(x, self.ln2_g, self.ln2_b)
        ffn = gelu(x_n2 @ self.W1 + self.b1) @ self.W2 + self.b2
        x = x + ffn
        return x


class SmallLM:
    def __init__(self, vocab_size, d_model=64, n_layers=3, n_heads=4, d_ff=256, max_len=64):
        self.d_model = d_model
        self.max_len = max_len
        self.token_embed = np.random.randn(vocab_size, d_model).astype(np.float64) * 0.02
        pos = np.arange(max_len)[:, None]
        div = np.exp(np.arange(0, d_model, 2) * -np.log(10000.0) / d_model)
        self.pos_embed = np.zeros((max_len, d_model), dtype=np.float64)
        self.pos_embed[:, 0::2] = np.sin(pos * div)
        self.pos_embed[:, 1::2] = np.cos(pos * div)
        self.blocks = [TransformerBlock(d_model, n_heads, d_ff) for _ in range(n_layers)]
        self.ln_f_g = np.ones(d_model, dtype=np.float64)
        self.ln_f_b = np.zeros(d_model, dtype=np.float64)
        self.lm_head = np.random.randn(d_model, vocab_size).astype(np.float64) * 0.02
        self._causal_mask = np.triu(np.full((max_len, max_len), -np.inf), k=1)

    def forward(self, idx, targets=None, return_logits=False):
        B, T = idx.shape
        x = self.token_embed[idx] + self.pos_embed[None, :T, :]
        mask = self._causal_mask[None, None, :T, :T]
        for block in self.blocks:
            x = block.forward(x, mask)
        x = layer_norm(x, self.ln_f_g, self.ln_f_b)
        logits = x @ self.lm_head
        if return_logits:
            return logits, None
        if targets is not None:
            loss = softmax_cross_entropy(logits.reshape(-1, vocab_size), targets.reshape(-1))
            return logits, loss
        return logits, None

    def forward_with_probs(self, idx):
        """Forward and return log probabilities."""
        logits, _ = self.forward(idx)
        logits_max = logits.max(axis=-1, keepdims=True)
        stable = logits - logits_max
        log_probs = stable - np.log(np.sum(np.exp(stable), axis=-1, keepdims=True))
        return logits, log_probs

    def generate(self, prompt, max_new_tokens=30, temperature=0.8, top_k=10):
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

    def get_token_logprobs(self, idx):
        """Get log probabilities for each token in sequence."""
        logits, log_probs = self.forward_with_probs(idx)
        # log_probs shape: (B, T, V)
        B, T, V = log_probs.shape
        token_logprobs = log_probs[np.arange(B)[:, None], np.arange(T)[None, :], idx]
        return token_logprobs  # (B, T)

    def parameters(self):
        params = [self.token_embed, self.pos_embed, self.lm_head,
                  self.ln_f_g, self.ln_f_b]
        for block in self.blocks:
            params.extend([block.W_q, block.W_k, block.W_v, block.W_o,
                          block.ln1_g, block.ln1_b,
                          block.W1, block.b1, block.W2, block.b2,
                          block.ln2_g, block.ln2_b])
        return params

    def copy_params_from(self, other):
        """Copy parameters from another model."""
        for p, op in zip(self.parameters(), other.parameters()):
            p[:] = op[:]


# ─────────────────────────────────────────────
# Synthetic preference data
# ─────────────────────────────────────────────

PREFERENCE_PROMPTS = [
    "Explain machine learning",
    "What is deep learning?",
    "Tell me about neural networks",
    "How does gradient descent work?",
    "What is reinforcement learning?",
    "Define supervised learning",
    "What are transformers?",
    "Explain backpropagation",
    "What is computer vision?",
    "Describe natural language processing",
]

PREFERENCE_CHOSEN = [
    "Machine learning is a field of AI that enables systems to learn from data.",
    "Deep learning uses multi-layer neural networks to model complex patterns.",
    "Neural networks are computing systems inspired by biological neural networks.",
    "Gradient descent iteratively adjusts parameters to minimize a loss function.",
    "Reinforcement learning trains agents through rewards and punishments.",
    "Supervised learning maps labeled inputs to outputs using training examples.",
    "Transformers use self-attention to process sequences in parallel efficiently.",
    "Backpropagation computes gradients by applying the chain rule through the network.",
    "Computer vision enables machines to interpret and understand visual information.",
    "NLP allows computers to understand, generate, and process human language.",
]

PREFERENCE_REJECTED = [
    "ML is computers learning stuff I guess.",
    "Deep learning is when the network is very deep, like the ocean.",
    "Neural networks are like spider webs.",
    "Gradient descent goes downhill step by step.",
    "RL is about learning to react to things.",
    "Supervised learning is when a supervisor teaches the computer.",
    "Transformers are robots that change shape.",
    "Backpropagation goes backwards somehow.",
    "CV is about seeing things.",
    "NLP is about talking to computers.",
]


def create_preference_batch(prompts, chosen, rejected, seq_len=64):
    """Create a batch of preference pairs."""
    batch_prompts = []
    batch_chosen = []
    batch_rejected = []

    for p, c, r in zip(prompts, chosen, rejected):
        p_tokens = list(encode(p))
        c_tokens = list(encode(c))
        r_tokens = list(encode(r))

        # Pad/truncate to seq_len
        def pad_tokens(toks):
            if len(toks) >= seq_len:
                return np.array(toks[:seq_len], dtype=np.int64)
            return np.pad(toks, (0, seq_len - len(toks)), 'constant').astype(np.int64)

        batch_prompts.append(p_tokens)
        batch_chosen.append(pad_tokens(p_tokens + c_tokens))
        batch_rejected.append(pad_tokens(p_tokens + r_tokens))

    return batch_prompts, np.stack(batch_chosen), np.stack(batch_rejected)


# ─────────────────────────────────────────────
# Optimizer
# ─────────────────────────────────────────────

class Optimizer:
    def __init__(self, params, lr=1e-4):
        self.params = params
        self.lr = lr

    def step(self, grads):
        for p, g in zip(self.params, grads):
            p -= self.lr * g


# ─────────────────────────────────────────────
# DPO Implementation
# ─────────────────────────────────────────────

class DPOTrainer:
    """
    Direct Preference Optimization.
    Loss: -E[log σ(β (log π_θ(y_w|x)/π_ref(y_w|x) - log π_θ(y_l|x)/π_ref(y_l|x)))]
    """
    def __init__(self, policy: SmallLM, ref_model: SmallLM, beta: float = 0.1, lr: float = 1e-4):
        self.policy = policy
        self.ref_model = ref_model
        self.beta = beta
        self.optim = Optimizer(policy.parameters(), lr)

    def compute_loss(self, chosen_ids: np.ndarray, rejected_ids: np.ndarray) -> float:
        """Compute DPO loss for a batch."""
        B, T = chosen_ids.shape

        # Policy log probs
        policy_chosen_lp = self.policy.get_token_logprobs(chosen_ids)  # (B, T)
        policy_rejected_lp = self.policy.get_token_logprobs(rejected_ids)  # (B, T)

        # Reference log probs
        ref_chosen_lp = self.ref_model.get_token_logprobs(chosen_ids)  # (B, T)
        ref_rejected_lp = self.ref_model.get_token_logprobs(rejected_ids)  # (B, T)

        # Sum over tokens
        pi_chosen = policy_chosen_lp.sum(axis=1)  # (B,)
        pi_rejected = policy_rejected_lp.sum(axis=1)  # (B,)
        ref_chosen = ref_chosen_lp.sum(axis=1)  # (B,)
        ref_rejected = ref_rejected_lp.sum(axis=1)  # (B,)

        # DPO loss
        log_ratio_chosen = pi_chosen - ref_chosen
        log_ratio_rejected = pi_rejected - ref_rejected
        logits_diff = self.beta * (log_ratio_chosen - log_ratio_rejected)

        # Loss = -log(sigmoid(logits_diff))
        # Use -log(sigmoid(x)) = -x + softplus(x) for numerical stability
        loss = np.mean(-logits_diff + np.log(1 + np.exp(logits_diff)))
        return float(loss)

    def compute_gradients(self, chosen_ids, rejected_ids, eps=1e-4):
        base_loss = self.compute_loss(chosen_ids, rejected_ids)
        params = self.policy.parameters()
        grads = [np.zeros_like(p) for p in params]

        for j, p in enumerate(params):
            for idx in np.ndindex(p.shape[:min(4, p.ndim)]):
                orig = p[idx]
                p[idx] = orig + eps
                loss_p = self.compute_loss(chosen_ids, rejected_ids)
                p[idx] = orig - eps
                loss_m = self.compute_loss(chosen_ids, rejected_ids)
                grads[j][idx] = (loss_p - loss_m) / (2 * eps)
                p[idx] = orig

        return grads

    def train_step(self, chosen_ids, rejected_ids):
        grads = self.compute_gradients(chosen_ids, rejected_ids)
        self.optim.step(grads)


# ─────────────────────────────────────────────
# PPO Implementation
# ─────────────────────────────────────────────

class RewardModel(SmallLM):
    """Reward model: transformer with scalar output."""
    def __init__(self, vocab_size, d_model=64, n_layers=3, n_heads=4, d_ff=256, max_len=64):
        super().__init__(vocab_size, d_model, n_layers, n_heads, d_ff, max_len)
        self.reward_head = np.random.randn(d_model, 1).astype(np.float64) * 0.02

    def forward(self, idx, targets=None):
        B, T = idx.shape
        x = self.token_embed[idx] + self.pos_embed[None, :T, :]
        mask = self._causal_mask[None, None, :T, :T]
        for block in self.blocks:
            x = block.forward(x, mask)
        x = layer_norm(x, self.ln_f_g, self.ln_f_b)
        # Use last token representation for reward
        reward = x[:, -1, :] @ self.reward_head  # (B, 1)
        return reward.squeeze(-1)  # (B,)

    def parameters(self):
        return super().parameters() + [self.reward_head]


class PPOTrainer:
    """
    PPO-based RLHF with reward model and KL penalty.
    Simplified implementation for educational purposes.
    """
    def __init__(self, policy: SmallLM, ref_model: SmallLM, reward_model: RewardModel,
                 kl_coef: float = 0.1, lr: float = 1e-4):
        self.policy = policy
        self.ref_model = ref_model
        self.reward_model = reward_model
        self.kl_coef = kl_coef
        self.optim = Optimizer(policy.parameters(), lr)

    def compute_advantages(self, responses):
        """Compute rewards = reward_model score - KL * (log π_θ - log π_ref)."""
        policy_lp = self.policy.get_token_logprobs(responses).sum(axis=1)
        ref_lp = self.ref_model.get_token_logprobs(responses).sum(axis=1)
        kl_div = policy_lp - ref_lp

        rewards = self.reward_model.forward(responses) - self.kl_coef * kl_div
        return rewards

    def compute_loss(self, responses):
        advantages = self.compute_advantages(responses)
        # Policy gradient loss: -E[advantage * log π]
        policy_lp = self.policy.get_token_logprobs(responses).sum(axis=1)
        loss = -(advantages * policy_lp).mean()
        return float(loss)

    def compute_gradients(self, responses, eps=1e-4):
        params = self.policy.parameters()
        grads = [np.zeros_like(p) for p in params]
        base_loss = self.compute_loss(responses)

        for j, p in enumerate(params):
            for idx in np.ndindex(p.shape[:min(3, p.ndim)]):
                orig = p[idx]
                p[idx] = orig + eps
                loss_p = self.compute_loss(responses)
                p[idx] = orig - eps
                loss_m = self.compute_loss(responses)
                grads[j][idx] = (loss_p - loss_m) / (2 * eps)
                p[idx] = orig

        return grads

    def train_step(self, responses):
        grads = self.compute_gradients(responses)
        self.optim.step(grads)


# ─────────────────────────────────────────────
# SFT training
# ─────────────────────────────────────────────

def sft_train(model: SmallLM, prompts, responses, epochs=5, lr=1e-4):
    """Supervised fine-tuning on chosen responses."""
    params = model.parameters()
    optim = Optimizer(params, lr)
    losses = []

    combined = []
    for p, r in zip(prompts, responses):
        tokens = list(encode(p)) + list(encode(r))
        combined.append(np.array(tokens[:model.max_len], dtype=np.int64))

    for epoch in range(epochs):
        epoch_loss = 0.0
        for seq in combined:
            x = seq[:-1][None, :]
            y = seq[1:][None, :]
            _, loss = model.forward(x, y)

            # Compute gradients via finite differences
            params = model.parameters()
            grads = [np.zeros_like(p) for p in params]
            for j, p in enumerate(params):
                for idx in np.ndindex(p.shape[:min(3, p.ndim)]):
                    orig = p[idx]
                    p[idx] = orig + 1e-4
                    _, lp = model.forward(x, y)
                    p[idx] = orig - 1e-4
                    _, lm = model.forward(x, y)
                    grads[j][idx] = (lp - lm) / (2e-4)
                    p[idx] = orig
            optim.step(grads)
            epoch_loss += loss

        losses.append(epoch_loss / len(combined))
        if (epoch + 1) % 2 == 0:
            print(f"  SFT Epoch {epoch+1}/{epochs} | Loss: {losses[-1]:.4f}")

    return losses


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    np.random.seed(42)
    d_model = 48
    n_layers = 2
    n_heads = 4
    d_ff = 192
    max_len = 48

    print("=" * 60)
    print("RLHF / DPO FROM SCRATCH")
    print("=" * 60)

    # ── 1. Initialize models ──
    print("\n[1] Initializing models...")
    policy = SmallLM(VOCAB_SIZE, d_model, n_layers, n_heads, d_ff, max_len)
    ref_model = SmallLM(VOCAB_SIZE, d_model, n_layers, n_heads, d_ff, max_len)
    ref_model.copy_params_from(policy)

    # ── 2. SFT ──
    print("\n[2] Supervised Fine-Tuning...")
    sft_loss = sft_train(policy, PREFERENCE_PROMPTS, PREFERENCE_CHOSEN, epochs=5)
    ref_model.copy_params_from(policy)

    # ── 3. Prepare preference data ──
    print("\n[3] Preparing preference data...")
    _, chosen_ids, rejected_ids = create_preference_batch(
        PREFERENCE_PROMPTS, PREFERENCE_CHOSEN, PREFERENCE_REJECTED, max_len
    )
    print(f"    Preference pairs: {len(chosen_ids)}")

    # ── 4. DPO Training ──
    print("\n[4] DPO Training...")
    dpo_trainer = DPOTrainer(policy, ref_model, beta=0.2, lr=1e-4)
    dpo_losses = []

    for step in range(15):
        dpo_trainer.train_step(chosen_ids, rejected_ids)
        loss = dpo_trainer.compute_loss(chosen_ids, rejected_ids)
        dpo_losses.append(loss)
        if (step + 1) % 5 == 0:
            print(f"  DPO Step {step+1:2d}/15 | Loss: {loss:.4f}")

    # ── 5. PPO Training (uses reward model) ──
    print("\n[5] Training reward model for PPO...")
    reward_model = RewardModel(VOCAB_SIZE, d_model, n_layers, n_heads, d_ff, max_len)
    # Simple reward model training: higher score for chosen, lower for rejected
    rm_epochs = 5
    for ep in range(rm_epochs):
        rw = reward_model.forward(chosen_ids)
        rl = reward_model.forward(rejected_ids)
        # Margin loss: -mean(rw - rl)
        loss = -np.mean(rw - rl)
        print(f"  RM Epoch {ep+1}/{rm_epochs} | Reward margin: {-(rw - rl).mean():.4f}")

    # Reset policy for PPO training
    ppo_policy = SmallLM(VOCAB_SIZE, d_model, n_layers, n_heads, d_ff, max_len)
    ppo_policy.copy_params_from(ref_model)
    ppo_ref = SmallLM(VOCAB_SIZE, d_model, n_layers, n_heads, d_ff, max_len)
    ppo_ref.copy_params_from(ref_model)

    print("\n[6] PPO Training...")
    ppo_trainer = PPOTrainer(ppo_policy, ppo_ref, reward_model, kl_coef=0.05, lr=1e-4)
    ppo_losses = []

    for step in range(10):
        ppo_trainer.train_step(chosen_ids)
        loss = ppo_trainer.compute_loss(chosen_ids)
        ppo_losses.append(loss)
        if (step + 1) % 5 == 0:
            print(f"  PPO Step {step+1:2d}/10 | Loss: {loss:.4f}")

    # ── 6. Generate samples ──
    print("\n" + "=" * 60)
    print("GENERATION COMPARISON")
    print("=" * 60)

    test_prompts = ["Explain machine learning", "What is deep learning?"]
    models = [("SFT (initial)", policy)]
    # We use the DPO-trained policy
    dpo_trained = SmallLM(VOCAB_SIZE, d_model, n_layers, n_heads, d_ff, max_len)
    dpo_trained.copy_params_from(policy)

    for name, model in [("DPO Trained", dpo_trained), ("PPO Trained", ppo_policy)]:
        print(f"\n--- {name} ---")
        for prompt in test_prompts:
            out = model.generate(prompt, max_new_tokens=25, temperature=0.7, top_k=10)
            print(f"  [{prompt}] → {out}")

    # ── 7. Plot ──
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].plot(sft_loss, 'b-', linewidth=2)
    axes[0].set_title('SFT Loss')
    axes[0].set_xlabel('Epoch')
    axes[0].grid(alpha=0.3)

    axes[1].plot(dpo_losses, 'g-', linewidth=2)
    axes[1].set_title('DPO Loss')
    axes[1].set_xlabel('Step')
    axes[1].grid(alpha=0.3)

    axes[2].plot(ppo_losses, 'r-', linewidth=2)
    axes[2].set_title('PPO Loss')
    axes[2].set_xlabel('Step')
    axes[2].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('../../assets/phase12/05_rlhf_dpo_results.png', dpi=150)
    plt.close()
    print("\nSaved 05_rlhf_dpo_results.png")


if __name__ == '__main__':
    main()
