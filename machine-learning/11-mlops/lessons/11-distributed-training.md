# 11.11 Distributed Training

## Objective
Scale model training across GPUs/nodes with **DDP**, **FSDP**, and **DeepSpeed**.

## Data Parallelism (DDP)
- `DistributedDataParallel` — each GPU has full model copy, processes different micro-batches.
- Gradients all-reduced across GPUs after every step.

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel

dist.init_process_group(backend="nccl")
model = MyModel().cuda()
model = DistributedDataParallel(model)

for data in loader:
    loss = model(data)
    loss.backward()
    optimizer.step()
```

## Fully Sharded Data Parallel (FSDP)
- Shards model parameters, gradients, optimizer states across GPUs.
- Enables training large models that don't fit on single GPU.

```python
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP

model = FSDP(MyModel())
```

## DeepSpeed
- ZeRO stages (1, 2, 3): optimizer, gradient, parameter sharding.
- Mixed precision, offloading, gradient checkpointing.

```python
import deepspeed

model_engine, optimizer, _, _ = deepspeed.initialize(
    model=model,
    model_parameters=params,
    config_params={
        "train_batch_size": 32,
        "zero_optimization": {"stage": 2},
        "fp16": {"enabled": True},
    },
)
```

## Scaling Considerations
| Strategy | Model Size | Speed-up | Complexity |
|----------|-----------|----------|------------|
| DDP | < 1 GB | Near-linear | Low |
| FSDP | 1–10 GB | Good | Medium |
| DeepSpeed | 10+ GB | Excellent | High |

## Best Practices
1. Profile communication overhead — NCCL all-reduce can become bottleneck.
2. Gradient accumulation to increase effective batch size without OOM.
3. Enable `torch.compile` for graph-level optimizations.
4. Use NVLink / InfiniBand for inter-GPU communication.
