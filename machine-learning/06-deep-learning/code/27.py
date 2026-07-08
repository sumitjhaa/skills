"""06.27 - Mixed Precision: FP16/FP32 training, loss scaling simulation"""

import numpy as np
import matplotlib.pyplot as plt


def simulate_fp16_cast(x):
    """Simulate FP16 cast by rounding to FP16 precision."""
    return x.astype(np.float16).astype(np.float32)


class MixedPrecisionModel:
    def __init__(self, dims):
        self.params = [np.random.randn(dims[i], dims[i+1]).astype(np.float32) * 0.1
                       for i in range(len(dims) - 1)]
        self.biases = [np.zeros(dims[i+1], dtype=np.float32) for i in range(len(dims) - 1)]
        self.fp32_params = [p.copy() for p in self.params]

    def forward_fp16(self, x):
        h = x.astype(np.float16)
        for W, b in zip(self.params, self.biases):
            W_16 = simulate_fp16_cast(W)
            h = simulate_fp16_cast(h @ W_16 + b)
            h = np.maximum(0, h)
        return h

    def forward_fp32(self, x):
        h = x
        for W, b in zip(self.params, self.biases):
            h = h @ W + b
            h = np.maximum(0, h)
        return h


class LossScaler:
    def __init__(self, scale=2.0 ** 15, growth_factor=2.0, backoff_factor=0.5, growth_interval=2000):
        self.scale = scale
        self.growth_factor = growth_factor
        self.backoff_factor = backoff_factor
        self.growth_interval = growth_interval
        self.steps_since_update = 0

    def scale_loss(self, loss):
        return loss * self.scale

    def unscale_gradients(self, grads):
        return [g / self.scale for g in grads]

    def update(self, overflow_detected):
        if overflow_detected:
            self.scale *= self.backoff_factor
            self.steps_since_update = 0
        else:
            self.steps_since_update += 1
            if self.steps_since_update >= self.growth_interval:
                self.scale *= self.growth_factor
                self.steps_since_update = 0


def detect_overflow(grads):
    for g in grads:
        if np.any(np.isnan(g)) or np.any(np.isinf(g)):
            return True
        if np.any(np.abs(g) > 65504):
            return True
    return False


if __name__ == "__main__":
    np.random.seed(42)

    model = MixedPrecisionModel([16, 32, 16, 8])
    x_fp32 = np.random.randn(8, 16).astype(np.float32)
    out_fp32 = model.forward_fp32(x_fp32)
    out_fp16 = model.forward_fp16(x_fp32)

    diff = np.abs(out_fp32 - out_fp16.astype(np.float32))
    print(f"FP32 output:  {out_fp32[0, :4]}")
    print(f"FP16 output:  {out_fp16[0, :4]}")
    print(f"Max difference: {diff.max():.6f}")

    scaler = LossScaler(scale=128.0)
    loss = np.array(1.5, dtype=np.float32)
    scaled_loss = scaler.scale_loss(loss)
    print(f"\nLoss scaling: {loss:.2f} -> {scaled_loss:.2f}")

    grads = [np.random.randn(*p.shape).astype(np.float32) * 0.1 for p in model.params]
    overflow = detect_overflow(grads)
    print(f"Overflow detected: {overflow}")

    unscaled = scaler.unscale_gradients(grads)
    print(f"Gradient before scaling: {grads[0][0, 0]:.6f}")
    print(f"Gradient after unscaling: {unscaled[0][0, 0]:.6f}")

    fp16_precision_loss = []
    for magnitude in np.logspace(-4, 4, 100):
        val = np.float32(magnitude)
        rounded = simulate_fp16_cast(val)
        fp16_precision_loss.append(abs(float(val - rounded) / val) if val != 0 else 0)

    plt.figure(figsize=(10, 5))
    plt.loglog(np.logspace(-4, 4, 100), fp16_precision_loss)
    plt.xlabel("Value magnitude")
    plt.ylabel("Relative precision loss")
    plt.title("FP16 Precision Loss vs Value Magnitude")
    plt.grid(True, alpha=0.3)
    plt.savefig("../../assets/phase06/mixed_precision.png")
    plt.close()

    for mag in [0.001, 0.1, 1.0, 100.0, 10000.0]:
        fp32_val = np.float32(mag)
        fp16_val = simulate_fp16_cast(fp32_val)
        print(f"  Value {mag:8.1f}: FP32={fp32_val}, FP16={fp16_val}, "
              f"loss={abs(fp32_val-fp16_val)/max(abs(fp32_val),1e-10):.6e}")

    print("\nMixed precision simulation complete.")
