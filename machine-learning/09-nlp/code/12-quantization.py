"""
09.12 Quantization — Symmetric, Asymmetric, and GPTQ-style
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


def symmetric_quantize(weights, bits=8):
    """Symmetric quantization to [-2^(b-1), 2^(b-1) - 1]."""
    max_val = 2 ** (bits - 1) - 1
    scale = np.max(np.abs(weights))
    q = np.round(weights / scale * max_val)
    q = np.clip(q, -max_val - 1, max_val).astype(np.int8)
    return q, scale


def asymmetric_quantize(weights, bits=8):
    """Asymmetric quantization to [0, 2^b - 1]."""
    min_val = np.min(weights)
    max_val = np.max(weights)
    scale = (max_val - min_val) / (2**bits - 1)
    zero_point = round(-min_val / scale)
    q = np.round(weights / scale + zero_point)
    q = np.clip(q, 0, 2**bits - 1).astype(np.uint8)
    return q, scale, zero_point


def gptq_quantize_row(row, bits=4):
    """GPTQ-style quant for a single weight row using Hessian info."""
    # Simplified: quantize with optimal rounding
    n = len(row)
    H = np.eye(n) * 0.01 + row[:, None] @ row[None, :] / n  # Dummy Hessian
    H_inv = np.linalg.inv(H + np.eye(n) * 1e-5)
    q_row = row.copy()
    errors = np.zeros(n, dtype=np.float32)

    for i in range(n):
        # Quantize to nearest int
        q_val = np.round(q_row[i] * (2**(bits-1)) / max(abs(q_row[i]), 1e-8))
        q_val = np.clip(q_val, -2**(bits-1), 2**(bits-1) - 1)
        err = q_val - q_row[i] * (2**(bits-1)) / max(abs(q_row[i]), 1e-8)
        errors[i] = err
        # Update remaining weights
        if i < n - 1:
            update = err * H_inv[i, i+1:] / H_inv[i, i]
            q_row[i+1:] -= update
    return q_row, errors


if __name__ == "__main__":
    np.random.seed(42)
    weights = np.random.randn(32, 64) * 0.5

    # Symmetric INT8
    q_sym, scale_sym = symmetric_quantize(weights.flatten())
    deq_sym = q_sym * scale_sym / 127.0
    err_sym = np.mean((weights.flatten() - deq_sym) ** 2)

    # Asymmetric INT8
    q_asym, scale_as, zp = asymmetric_quantize(weights.flatten())
    deq_asym = (q_asym.astype(np.float32) - zp) * scale_as
    err_asym = np.mean((weights.flatten() - deq_asym) ** 2)

    print(f"Symmetric INT8 MSE:  {err_sym:.6f}")
    print(f"Asymmetric INT8 MSE: {err_asym:.6f}")

    # GPTQ row quantization (INT4)
    row = weights[0, :]
    q_row, errors = gptq_quantize_row(row, bits=4)
    print(f"\nGPTQ quantized row MSE: {np.mean(errors**2):.6f}")
    print(f"Original range: [{row.min():.3f}, {row.max():.3f}] -> "
          f"Quantized range: [{q_row.min():.3f}, {q_row.max():.3f}]")
