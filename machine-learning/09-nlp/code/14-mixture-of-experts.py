"""
09.14 Mixture of Experts — Top-2 Sparse MoE Layer
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


def softmax(x, axis=-1):
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / np.sum(e, axis=axis, keepdims=True)


class ExpertFFN:
    """Single expert: a 2-layer feed-forward network."""

    def __init__(self, d_model, d_ff):
        self.W1 = np.random.randn(d_model, d_ff) * 0.02
        self.W2 = np.random.randn(d_ff, d_model) * 0.02

    def __call__(self, x):
        # x: (..., d_model)
        hidden = np.maximum(0, x @ self.W1)
        return hidden @ self.W2


class SparseMoE:
    """
    Mixture of Experts with top-k routing.
    """

    def __init__(self, d_model, d_ff, num_experts=8, top_k=2):
        self.num_experts = num_experts
        self.top_k = top_k
        self.experts = [ExpertFFN(d_model, d_ff) for _ in range(num_experts)]
        self.router = np.random.randn(d_model, num_experts) * 0.02

    def __call__(self, x):
        original_shape = x.shape
        if x.ndim == 3:
            B, T, D = x.shape
            x_flat = x.reshape(-1, D)
        else:
            x_flat = x

        # Router logits
        router_logits = x_flat @ self.router  # (N, E)
        router_probs = softmax(router_logits, axis=-1)

        # Top-k selection
        top_k_indices = np.argsort(-router_probs, axis=-1)[:, :self.top_k]
        top_k_probs = np.take_along_axis(router_probs, top_k_indices, axis=-1)
        top_k_probs = top_k_probs / (top_k_probs.sum(axis=-1, keepdims=True) + 1e-10)

        # Compute expert outputs
        outputs = np.zeros_like(x_flat)
        for e_idx in range(self.num_experts):
            mask = np.any(top_k_indices == e_idx, axis=-1)
            if mask.any():
                expert_out = self.experts[e_idx](x_flat[mask])
                # Weight by router probability (for this expert)
                pos_in_k = np.argmax((top_k_indices[mask] == e_idx).astype(int), axis=-1)
                weights = np.take_along_axis(router_probs[mask], top_k_indices[mask], axis=-1)
                w = weights[np.arange(len(mask[mask])), pos_in_k]
                outputs[mask] += expert_out * w[:, None]

        return outputs.reshape(original_shape)


if __name__ == "__main__":
    d_model, d_ff, num_experts, top_k = 32, 64, 8, 2
    moe = SparseMoE(d_model, d_ff, num_experts, top_k)

    B, T = 4, 8
    x = np.random.randn(B, T, d_model)
    out = moe(x)

    print(f"MoE input:  {x.shape}")
    print(f"MoE output: {out.shape}")
    print(f"Experts: {num_experts}, Top-k: {top_k}, Params per expert: {d_model * d_ff * 2}")
    print(f"Active params per token: {top_k * d_model * d_ff * 2}")
