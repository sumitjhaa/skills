"""
09.10 Efficient Finetuning — LoRA from scratch
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


class LoRALayer:
    """
    LoRA: W' = W + B @ A
    W: (d_out, d_in) — frozen
    B: (d_out, r) — trainable, init zero
    A: (r, d_in) — trainable, init Gaussian
    """

    def __init__(self, d_in, d_out, rank=4, alpha=1.0):
        self.rank = rank
        self.alpha = alpha
        # Frozen pretrained weights
        self.W = np.random.randn(d_out, d_in) * 0.02
        # LoRA matrices
        self.A = np.random.randn(rank, d_in) * 0.01
        self.B = np.zeros((d_out, rank))
        self.lr = 0.01

    def forward(self, x):
        # x: (..., d_in)
        base = x @ self.W.T  # (..., d_out)
        lora = x @ self.A.T @ self.B.T  # (..., d_out)
        return base + self.alpha * lora

    def backward(self, x, grad_output):
        """Update LoRA weights with SGD."""
        B, T, d_in = x.shape if x.ndim == 3 else (1,) + x.shape
        x_flat = x.reshape(-1, d_in)  # (N, d_in)
        grad_flat = grad_output.reshape(-1, self.W.shape[0])  # (N, d_out)

        # Gradient w.r.t. B: grad_B = grad^T @ (x @ A^T)
        xA = x_flat @ self.A.T  # (N, r)
        grad_B = grad_flat.T @ xA  # (d_out, r)
        # Gradient w.r.t. A: grad_A = (grad @ B)^T @ x
        grad_A = (grad_flat @ self.B).T @ x_flat  # (r, d_in)

        self.B -= self.lr * grad_B / len(x_flat)
        self.A -= self.lr * grad_A / len(x_flat)

        # Gradient through frozen W (for downstream, but we don't update W)
        grad_x = grad_flat @ self.W  # (N, d_in)
        return grad_x.reshape(*x.shape)


if __name__ == "__main__":
    d_in, d_out, rank = 16, 32, 4
    layer = LoRALayer(d_in, d_out, rank=rank, alpha=2.0)

    B, T = 4, 8
    x = np.random.randn(B, T, d_in)

    out = layer.forward(x)
    print(f"Forward: {x.shape} -> {out.shape}")

    # Simulate a backward pass
    grad_out = np.random.randn(B, T, d_out) * 0.1
    grad_x = layer.backward(x, grad_out)

    print(f"LoRA A norm before:  {np.linalg.norm(layer.A):.4f}")
    print(f"LoRA B norm before:  {np.linalg.norm(layer.B):.4f}")
    print(f"Gradient w.r.t. x:   {np.linalg.norm(grad_x):.4f}")
    print(f"LoRA A rank:         {np.linalg.matrix_rank(layer.A)} (of {rank})")
    print(f"LoRA B rank:         {np.linalg.matrix_rank(layer.B)} (of {rank})")
    print("LoRA layer trains only the low-rank adapters, W stays frozen.")
