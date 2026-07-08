# Lesson 12.07: Distributed Training with FSDP

## Project Architecture

Implement a simplified Fully Sharded Data Parallel (FSDP) training system to scale a transformer model across multiple GPUs (simulated with multiple processes on CPU).

```
FSDP Design
┌─────────────────────────────────────────────────────┐
│                    Training Loop                     │
├─────────────────────────────────────────────────────┤
│ Rank 0       Rank 1       Rank 2       Rank 3       │
│ ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│ │ Shard 0 │  │ Shard 1 │  │ Shard 2 │  │ Shard 3 │ │
│ │ (params)│  │ (params)│  │ (params)│  │ (params)│ │
│ └─────────┘  └─────────┘  └─────────┘  └─────────┘ │
│      │            │            │            │        │
│      └────────────┴────────────┴────────────┘        │
│              AllGather (forward)                      │
│              ReduceScatter (backward)                 │
└─────────────────────────────────────────────────────┘

Key Operations
├── Sharding: split parameters evenly across ranks
├── Forward: AllGather full params, compute, discard non-owned shards
├── Backward: ReduceScatter gradients, update owned shard
└── Optimizer step: each rank updates only its shard
```

## Design Decisions

### Simulation approach
- Use `torch.distributed` with `gloo` backend on CPU
- Multiple processes via `torch.multiprocessing`
- Simulate FSDP without real GPUs

### Sharding strategy
- `FULL_SHARD`: parameters, gradients, optimizer states all sharded
- `NO_SHARD`: equivalent to DDP (baseline)
- `HYBRID_SHARD`: shard within node, replicate across nodes

### Communication primitives
- `all_gather`: collect full parameters from all ranks
- `reduce_scatter`: sum gradients, scatter result to ranks

### Memory tracking
- Track peak memory per rank
- Compare FSDP vs. DDP memory usage

### Scaling metrics
- Weak scaling: double data, double workers, same time
- Strong scaling: same data, double workers, half time

## Implementation Guide

1. **Set up distributed process group** (init, rank, world_size)
2. **Implement parameter sharding** (split along first dimension)
3. **Implement AllGather** for forward pass
4. **Implement ReduceScatter** for backward pass
5. **Build FSDP wrapper module**
6. **Implement no-shard baseline (DDP)**
7. **Build training script with both strategies**
8. **Implement memory tracking**
9. **Run scaling experiments** (weak + strong)
10. **Plot: memory vs. world_size, time vs. world_size**

## Key Insights

- FSDP trades communication for memory: 4x memory savings for 1.2x communication overhead (roughly)
- The AllGather in forward and ReduceScatter in backward can overlap with computation
- FSDP enables training models that don't fit on a single GPU
- The sharding granularity (how often we all-gather) affects the memory/communication tradeoff
- Mixed precision + FSDP further reduces memory via fp16 gradients
