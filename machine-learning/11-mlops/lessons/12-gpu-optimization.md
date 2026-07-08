# 11.12 GPU Optimization

## Objective
Maximize GPU utilization, minimize memory footprint, and profile performance.

## Memory Optimization
1. **Gradient Checkpointing** — recompute activations during backward (saves memory, uses compute).
   ```python
   model = torch.utils.checkpoint.checkpoint_sequential(layers, segments=4, input)
   ```
2. **Mixed Precision (AMP)** — FP16/BF16 for forward/backward, FP32 for master weights.
   ```python
   with torch.cuda.amp.autocast():
       output = model(input)
   ```
3. **`torch.compile`** — fuses kernel operations, reduces launch overhead.
   ```python
   model = torch.compile(model, mode="reduce-overhead")
   ```

## CUDA Graphs
- Capture a static graph of CUDA kernels and replay it.
- Eliminates kernel launch overhead for fixed-shape models.

```python
graph = torch.cuda.CUDAGraph()
with torch.cuda.graph(graph):
    output = model(fixed_input)
# Replay:
graph.replay()
```

## Profiling
```python
with torch.profiler.profile(
    activities=[torch.profiler.ProfilerActivity.CUDA],
    schedule=torch.profiler.schedule(wait=1, warmup=1, active=3),
) as prof:
    for step in range(5):
        train_step()
        prof.step()
prof.export_chrome_trace("trace.json")
```

## Key Metrics
| Metric | Target |
|--------|--------|
| GPU Utilization | > 80 % |
| Memory Used | < 90 % capacity |
| Kernel Launch Overhead | < 5 % of step time |
| PCIe / NVLink Bandwidth | < 70 % saturated |

## Best Practices
1. Use `NVIDIA SMI` / `nvidia-topo -m` to check GPU topology.
2. Set `OMP_NUM_THREADS` = number of CPU cores per GPU.
3. Pin memory for DataLoader workers (`pin_memory=True`).
4. Profile at least once per major model architecture change.
