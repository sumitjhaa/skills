"""
09.15 Inference Optimization — KV Cache & Speculative Decoding Simulation
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


class KVCache:
    """Simple KV cache for auto-regressive generation."""

    def __init__(self):
        self.cache = {}

    def append(self, layer_idx, key, value):
        # key, value: (B, H, T, d_head)
        if layer_idx not in self.cache:
            self.cache[layer_idx] = (key, value)
        else:
            k_prev, v_prev = self.cache[layer_idx]
            self.cache[layer_idx] = (
                np.concatenate([k_prev, key], axis=2),
                np.concatenate([v_prev, value], axis=2),
            )

    def get(self, layer_idx):
        return self.cache.get(layer_idx, (None, None))

    def clear(self):
        self.cache = {}


def draft_generate(draft_model, prefix, num_tokens=5):
    """Draft model generates k tokens quickly."""
    tokens = list(prefix)
    for _ in range(num_tokens):
        logits = draft_model(tokens)
        next_token = np.argmax(logits[-1])
        tokens.append(next_token)
    return tokens[len(prefix):]


def verify_with_target(target_model, prefix, draft_tokens):
    """Target model verifies draft tokens in one forward pass."""
    full_sequence = prefix + draft_tokens
    logits = target_model(full_sequence)
    accepted = []
    for i, draft_token in enumerate(draft_tokens):
        prob = np.exp(logits[len(prefix) + i - 1][draft_token])
        prob = prob / logits[len(prefix) + i - 1].sum()
        if np.random.random() < min(1.0, prob / 0.1):  # Rejection sampling
            accepted.append(draft_token)
        else:
            # Resample from target distribution with adjusted probs
            adjusted = np.maximum(0, logits[len(prefix) + i - 1] - 0.1)
            resample = np.random.choice(len(adjusted), p=adjusted / adjusted.sum())
            accepted.append(resample)
            break
    return accepted


if __name__ == "__main__":
    vocab_size, d_model = 100, 16

    class DummyLM:
        def __init__(self, bias=0.0):
            self.W = np.random.randn(vocab_size, d_model) * 0.1
            self.bias = bias

        def __call__(self, tokens):
            """Return logits per position."""
            T = len(tokens)
            x = np.random.randn(T, d_model)
            logits = x @ self.W.T
            # Add bias toward certain tokens
            logits[:, :10] += self.bias
            return logits

    draft = DummyLM(bias=0.5)   # Fast, less accurate
    target = DummyLM(bias=1.0)  # Slow, accurate

    prefix = [0, 1, 2]
    draft_tokens = draft_generate(draft, prefix, num_tokens=5)
    accepted = verify_with_target(target, prefix, draft_tokens)

    print(f"Prefix:            {prefix}")
    print(f"Draft tokens:      {draft_tokens}")
    print(f"Accepted tokens:   {accepted}")
    print(f"Acceptance rate:   {len(accepted)}/{len(draft_tokens)}")

    # KV Cache demo
    cache = KVCache()
    B, H, d_head = 2, 4, 8
    for step in range(3):
        k = np.random.randn(B, H, 1, d_head)
        v = np.random.randn(B, H, 1, d_head)
        cache.append(0, k, v)
        k_full, v_full = cache.get(0)
        print(f"Step {step}: KV cache size = {k_full.shape[2]}")
