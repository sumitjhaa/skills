# 06.27 Mixed Precision

Mixed precision training uses FP16 for most operations while keeping FP32 master copies of weights.

## Why Mixed Precision

- FP16 uses half the memory of FP32
- FP16 matrix multiplications are 2-8x faster on modern GPUs
- Training larger models or larger batches

## The Problem

FP16 has limited range: ~5.5e-5 to 65,504. Gradients often underflow to 0.

FP16 precision: ~3 decimal digits (10 bits mantissa vs FP32's 23 bits).

## Loss Scaling

Multiply loss by a scale factor before backward pass. Gradients scaled up → values stay in FP16 range. Unscale before optimizer step.

```
loss = criterion(output, target)
loss = loss * scale_factor
loss.backward()
# gradients are scaled
for p in params:
    p.grad /= scale_factor
    optimizer.step(p)
```

Dynamic loss scaling: double scale if no overflow for N steps, halve on overflow.

## FP32 Master Copy

Keep a FP32 copy of weights. Accumulate gradients in FP32. Update FP32 weights. Cast to FP16 for forward pass.

```
fp32_weights → fp16 → forward → loss → scale → backward → fp16_grads
    ↑                                                  ↓
    └──────────── optimizer step ←─ unscale ←─ fp32_grads
```

## Gradient Overflow Detection

Check for NaNs/Infs in gradients. Skip update step if detected.

## Simulating in NumPy

Since we're not on GPU, we can simulate mixed precision by deliberately casting to float16 and back:

```python
x_16 = x.astype(np.float16)
x_32 = x_16.astype(np.float32)  # lossy round-trip
```

## Implementation Considerations

- `matmul` in FP16: accumulator in FP32
- Softmax, LayerNorm: keep in FP32 for numerical stability
- Loss scaling factor: start with 2^16 (65536)
