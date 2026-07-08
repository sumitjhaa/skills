# 06.28 Gradient Accumulation / Checkpointing

Memory-efficient training techniques for fitting large models into limited memory.

## Gradient Accumulation

Simulates larger batch size by accumulating gradients over multiple forward/backward passes:

```python
optimizer.zero_grad()
for micro_step in range(accumulation_steps):
    loss = model(data[micro_step * micro_batch : (micro_step+1) * micro_batch])
    loss = loss / accumulation_steps
    loss.backward()  # accumulates gradients
optimizer.step()     # update with effective_batch = micro_batch × accumulation_steps
```

Key points:
- Divide loss by accumulation_steps to keep loss magnitude consistent
- Only step the optimizer after the full accumulation
- BatchNorm statistics may be affected (use running averages or sync BN)
- Equivalent to training with larger batch (same gradient direction)

## Gradient Checkpointing (Activation Checkpointing)

Trade compute for memory: don't store intermediate activations, recompute them during backward.

Without checkpointing: memory = O(n) for n layers (all activations stored).
With checkpointing: memory = O(√n) or O(log n) depending on strategy.

```python
# Forward with checkpointing
def forward(x):
    x1 = checkpoint(block1, x)
    x2 = checkpoint(block2, x1)
    return checkpoint(block3, x2)
```

During backward: recompute activations from stored inputs.

## Memory vs. Compute Tradeoff

| Strategy | Memory | Compute Overhead |
|----------|--------|-----------------|
| No checkpointing | O(n) | 1x |
| Every layer | O(1) | ~2x extra forward |
| Check every k layers | O(k) | ~n/k extra forward |
| Optimal (Chen et al.) | O(√n) | ~2x |

## Segment-Based Checkpointing

Divide network into segments. Store only segment boundaries. Recompute within each segment during backward.

Best tradeoff: √n segments, each of length √n.

## CPU Offloading

Move optimizer states and parameters to CPU when not in use. Only keep current layer's data on GPU.

## Combined Approach

Use all techniques together for very large models (e.g., training GPT-3):

- Gradient accumulation: large effective batch
- Activation checkpointing: reduce activation memory
- Mixed precision: reduce parameter/gradient memory
- CPU offloading: optimizer states on CPU
