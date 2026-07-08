"""
Mock Data Pipeline Optimization — demonstrates data loading bottlenecks,
caching, prefetching, and format efficiency comparisons.
"""

import time
import numpy as np
from dataclasses import dataclass


@dataclass
class PipelineProfile:
    data_load_ms: float = 0.0
    compute_ms: float = 0.0
    total_ms: float = 0.0
    iobound: bool = False


def simulate_dataloader(num_workers: int = 0, prefetch: bool = False, cache: bool = False) -> PipelineProfile:
    """Simulate data loading with different optimization flags."""
    batch_size = 64
    n_batches = 50

    # Simulate dataset on disk
    load_time_per_batch = 0.015 - (num_workers * 0.002)  # parallel workers reduce load time
    if prefetch:
        load_time_per_batch *= 0.7
    if cache:
        load_time_per_batch *= 0.3

    load_time = max(load_time_per_batch, 0.001)

    compute_time = 0.020  # constant compute per batch

    total_load = 0.0
    total_compute = 0.0

    for _ in range(n_batches):
        # Simulate I/O wait
        time.sleep(load_time * 0.01)  # scaled down for speed
        total_load += load_time

        # Simulate compute
        _ = np.random.randn(batch_size, 3, 224, 224).mean()
        total_compute += compute_time

    return PipelineProfile(
        data_load_ms=round(total_load * 1000, 1),
        compute_ms=round(total_compute * 1000, 1),
        total_ms=round((total_load + total_compute) * 1000, 1),
        iobound=(total_load / (total_load + total_compute)) > 0.3,
    )


def format_comparison() -> dict:
    """Compare storage formats for a mock dataset."""
    n_rows = 1_000_000
    n_cols = 50

    sizes = {
        "CSV (float32)": n_rows * n_cols * 4,
        "CSV (float16)": n_rows * n_cols * 2,
        "Parquet + Snappy": n_rows * n_cols * 4 * 0.25,
        "Parquet + Zstd": n_rows * n_cols * 4 * 0.15,
        "NumPy memmap": n_rows * n_cols * 4,
    }

    read_speeds = {
        "CSV (float32)": 150,
        "CSV (float16)": 200,
        "Parquet + Snappy": 450,
        "Parquet + Zstd": 400,
        "NumPy memmap": 800,
    }

    results = {}
    for fmt, size_bytes in sizes.items():
        size_mb = size_bytes / (1024 ** 2)
        read_time_s = size_mb / read_speeds[fmt]
        results[fmt] = {
            "size_mb": round(size_mb, 1),
            "read_speed_mbps": read_speeds[fmt],
            "read_time_s": round(read_time_s, 2),
        }
    return results


if __name__ == "__main__":
    print("=== Data Pipeline Optimization ===")

    configs = [
        ("num_workers=0", PipelineProfile()),
        ("num_workers=4", PipelineProfile()),
        ("num_workers=4, prefetch=True", PipelineProfile()),
        ("num_workers=4, cache=True", PipelineProfile()),
    ]

    profiles = [
        simulate_dataloader(num_workers=0),
        simulate_dataloader(num_workers=4),
        simulate_dataloader(num_workers=4, prefetch=True),
        simulate_dataloader(num_workers=4, cache=True),
    ]

    for name, prof in zip([c[0] for c in configs], profiles):
        bottleneck = "I/O BOUND" if prof.iobound else "compute bound"
        print(f"  {name:40s} load={prof.data_load_ms:6.1f}ms  compute={prof.compute_ms:6.1f}ms  [{bottleneck}]")

    print("\n=== Format Comparison (1M x 50 dataset) ===")
    formats = format_comparison()
    for fmt, info in formats.items():
        print(f"  {fmt:25s} {info['size_mb']:8.1f} MB  read={info['read_time_s']:5.2f}s")

    print("\nTip: Use Parquet + Zstd for storage efficiency.")
    print("Tip: Use memmap to avoid loading entire dataset into RAM.")
