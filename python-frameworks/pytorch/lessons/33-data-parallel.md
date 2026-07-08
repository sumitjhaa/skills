# 🏗️ Data Parallel & Distributed Training
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Train on multiple GPUs.

## DataParallel (simple, single-node)

```python
model = nn.DataParallel(model)
# Automatically splits batches across GPUs
```

## DistributedDataParallel (recommended)

```python
# Per-process launch:
# torchrun --nproc_per_node=4 train.py

import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

dist.init_process_group(backend='nccl')
model = DDP(model)
```

## Why DDP > DataParallel

| Aspect | DataParallel | DDP |
|--------|-------------|-----|
| Speed | Slower (GIL, single process) | Faster (multi-process) |
| Scalability | Single node | Multi-node |
| Recommended | No | Yes |

<!-- 🤔 DataParallel is fine for 2-4 GPUs. DDP is standard for distributed training. -->

## Run the Code

```bash
python code/33-data-parallel.py
```
