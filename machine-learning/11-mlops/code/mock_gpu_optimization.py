"""
Mock GPU Optimization — demonstrates CUDA graphs, mixed precision,
gradient checkpointing, and profiling concepts using NumPy simulations.
"""

import time
import numpy as np


def simulate_step(use_amp: bool = False, use_checkpointing: bool = False) -> float:
    """Simulate a training step with various optimization flags."""
    batch_size = 32
    n_layers = 10
    hidden_dim = 1024

    data = np.random.randn(batch_size, hidden_dim).astype(np.float32 if not use_amp else np.float16)
    weights = [np.random.randn(hidden_dim, hidden_dim).astype(np.float32) for _ in range(n_layers)]

    t0 = time.perf_counter()

    # Forward
    x = data
    for w in weights:
        if use_checkpointing:
            # Simulate checkpointing: forward with recompute on backward
            x = x @ w
            time.sleep(0.0001)  # recompute cost
        x = x @ w
        x = np.maximum(x, 0)

    loss = float(np.sum(x ** 2))

    # Backward (simplified)
    for w in weights:
        dummy_grad = np.random.randn(*w.shape).astype(np.float32)
        w -= 0.01 * dummy_grad

    elapsed = time.perf_counter() - t0
    return elapsed


def simulate_cuda_graph(iterations: int = 100) -> tuple[float, float]:
    """Simulate the benefit of CUDA graph capture + replay."""
    static_input = np.random.randn(32, 1024).astype(np.float32)

    # Without CUDA graphs
    t0 = time.perf_counter()
    for _ in range(iterations):
        result = static_input @ np.random.randn(1024, 512).astype(np.float32)
        result = np.maximum(result, 0)
    eager_time = time.perf_counter() - t0

    # With CUDA graphs (capture once + replay)
    t0 = time.perf_counter()
    weights = np.random.randn(1024, 512).astype(np.float32)
    result = static_input @ weights  # capture
    for _ in range(iterations - 1):
        result = static_input @ weights  # replay
    graph_time = time.perf_counter() - t0

    return eager_time, graph_time


def profile_gpu_utilization() -> dict:
    """Return mock GPU utilization metrics."""
    return {
        "gpu_util_pct": np.random.uniform(70, 98),
        "memory_used_gb": np.random.uniform(12, 22),
        "memory_total_gb": 24,
        "mem_pct": np.random.uniform(50, 92),
        "power_watts": np.random.uniform(150, 300),
        "temperature_c": np.random.uniform(55, 78),
    }


if __name__ == "__main__":
    print("=== GPU Optimization Comparison ===")

    fp32_time = simulate_step(use_amp=False)
    fp16_time = simulate_step(use_amp=True)
    print(f"  FP32 step:     {fp32_time*1000:.2f} ms")
    print(f"  FP16 (AMP)     {fp16_time*1000:.2f} ms")
    print(f"  Speedup:       {fp32_time/fp16_time:.2f}x")

    checkpoint_time = simulate_step(use_checkpointing=True)
    print(f"  Checkpointing: {checkpoint_time*1000:.2f} ms")

    print("\n=== CUDA Graph Simulation ===")
    eager, graph = simulate_cuda_graph(iterations=200)
    print(f"  Eager:       {eager*1000:.2f} ms")
    print(f"  CUDA Graph:  {graph*1000:.2f} ms")
    print(f"  Speedup:     {eager/graph:.2f}x")

    print("\n=== GPU Utilization (mock) ===")
    metrics = profile_gpu_utilization()
    for k, v in metrics.items():
        print(f"  {k}: {v}")
