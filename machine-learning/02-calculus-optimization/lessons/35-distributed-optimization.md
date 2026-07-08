# 35. Distributed Optimization

## Introduction

Distributed optimization enables training on data that cannot be centralized and scales optimization to models too large for a single machine. It is fundamental to modern deep learning at scale.

## Data Parallelism

Each worker has a copy of the model and processes a different data shard:

```
w_{t+1} = w_t - η · (1/N) Σᵢ ∇f_i(w_t)
```

```python
import numpy as np

def all_reduce(gradients):
    """Simulate all-reduce: average gradients across workers."""
    # In practice: ring all-reduce, tree all-reduce, or NCCL
    return np.mean(gradients, axis=0)

def distributed_sgd(grad_f, x0, n_workers=4, lr=0.01, n_iter=100):
    """Simulated distributed SGD."""
    x = x0.copy()

    for t in range(n_iter):
        # Each worker computes local gradient
        local_grads = []
        for w in range(n_workers):
            local_grads.append(grad_f(x, w))  # worker w on its shard

        # All-reduce to average gradients
        avg_grad = all_reduce(np.array(local_grads))

        # Global update
        x = x - lr * avg_grad

    return x
```

## Communication Topologies

### All-Reduce (Synchronous)

All workers compute gradients, then average them via ring all-reduce. Communication cost: O(n) per worker, independent of the number of workers.

### Parameter Server (Asynchronous)

A central server stores parameters. Workers pull parameters, compute gradients, and push updates asynchronously. Stale gradients can slow convergence.

### Decentralized (Gossip)

Workers communicate only with neighbors in a graph:

```
x_{i,t+1} = Σ_{j ∈ N(i)} W_{ij} (x_{j,t} - η ∇f_j(x_{j,t}))
```

```python
def gossip_sgd(grad_f, x0, adjacency, lr=0.01, n_iter=100):
    """Decentralized gossip SGD."""
    n_workers = len(adjacency)
    x = np.array([x0.copy() for _ in range(n_workers)])

    # Mixing matrix (symmetric doubly stochastic)
    W = np.zeros((n_workers, n_workers))
    for i in range(n_workers):
        deg = len(adjacency[i])
        for j in adjacency[i]:
            W[i, j] = 1 / (max(deg, len(adjacency[j])) + 1)
        W[i, i] = 1 - W[i].sum()

    for t in range(n_iter):
        for i in range(n_workers):
            g = grad_f(x[i], i)
            consensus = W[i] @ x
            x[i] = consensus - lr * g

    return x.mean(axis=0)  # all workers converge to same value
```

## Communication-Efficient Methods

### Gradient Compression

- **Quantization**: Compress gradients to low precision (e.g., 8-bit)
- **Sparsification**: Send only top-k% largest gradients
- **SignSGD**: Only transmit the sign of gradients

```python
def top_k_sparsification(grad, k=0.01):
    """Keep only top k% of gradient entries by magnitude."""
    flat = grad.flatten()
    n = len(flat)
    k_keep = max(1, int(n * k))
    idx = np.argsort(np.abs(flat))[-k_keep:]
    sparse = np.zeros_like(flat)
    sparse[idx] = flat[idx]
    return sparse.reshape(grad.shape)
```

### Local SGD (FedAvg)

Workers perform multiple local steps before communication:

```python
def local_sgd(grad_f, x0, n_workers=4, local_steps=5, lr=0.01, n_rounds=20):
    """Federated averaging / Local SGD."""
    x = np.array([x0.copy() for _ in range(n_workers)])
    x_global = x0.copy()

    for r in range(n_rounds):
        for i in range(n_workers):
            x[i] = x_global.copy()
            for _ in range(local_steps):
                x[i] = x[i] - lr * grad_f(x[i], i)

        x_global = x.mean(axis=0)

    return x_global
```

## Applications

- **Large-batch training**: Train ResNet-50 on ImageNet in minutes
- **Federated learning**: Train across user devices without centralizing data
- **Distributed RL**: Parallelized environment simulation and policy optimization

Distributed optimization enables training at scales impossible on single devices, at the cost of communication overhead and convergence analysis challenges.
