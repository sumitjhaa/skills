# 38. Mini-Batch Selection Strategies

## Introduction

Standard SGD uses uniform random minibatches. However, not all examples are equally informative. Adaptive selection strategies can significantly accelerate convergence.

## Importance Sampling

Assign higher sampling probability to examples with larger gradients:

```
p_i ∝ ‖∇f_i(x)‖  or  p_i ∝ ‖∇f_i(x)‖²
```

```python
import numpy as np

def importance_sampled_batch(gradients, batch_size, temperature=1.0):
    """Sample minibatch proportional to gradient norms."""
    norms = np.array([np.linalg.norm(g) for g in gradients])
    weights = norms ** temperature
    weights = weights / weights.sum()

    idx = np.random.choice(len(gradients), size=batch_size, p=weights)
    return idx
```

This minimizes the variance of the gradient estimate:

```
Var[importance_sampled_gradient] ≤ Var[uniform_gradient]
```

## Self-Paced Learning

Start with easy examples, gradually incorporate harder ones:

```python
def self_paced_batch(losses, batch_size, epoch, total_epochs):
    """Self-paced curriculum learning."""
    threshold = epoch / total_epochs
    # Select examples below threshold percentile (easier examples first)
    threshold_loss = np.percentile(losses, threshold * 100)
    eligible = np.where(losses <= threshold_loss)[0]

    if len(eligible) < batch_size:
        eligible = np.arange(len(losses))

    return np.random.choice(eligible, size=batch_size)
```

## Coresets

Select a weighted subset that approximates the full dataset:

```python
def uniform_coreset(X, k):
    """Select k representative points via k-center clustering."""
    from scipy.spatial.distance import cdist

    n = len(X)
    idx = [np.random.randint(n)]

    for _ in range(k - 1):
        dists = cdist(X, X[idx]).min(axis=1)
        idx.append(np.argmax(dists))

    return np.array(idx)
```

## Adaptive Batch Size

Gradually increase batch size during training:

```python
def adaptive_batch_size(t, initial_batch=32, growth_factor=1.1):
    """Exponentially growing batch size."""
    return min(8192, int(initial_batch * growth_factor ** t))
```

Larger batches in later iterations reduce gradient noise without sacrificing convergence speed (Smith et al., 2018).

## Gradient Diversity

Measure of how much individual gradients differ from the mean:

```python
def gradient_diversity(gradients):
    """Gradient diversity metric."""
    n = len(gradients)
    grad_mean = np.mean(gradients, axis=0)
    grad_var = np.mean([np.linalg.norm(g - grad_mean)**2 for g in gradients])
    return grad_var / (np.linalg.norm(grad_mean)**2 + 1e-10)
```

High gradient diversity suggests a smaller batch suffices.

## Applications

- **Imbalanced datasets**: Focus on misclassified examples
- **Active learning**: Select most uncertain examples for labeling
- **Noisy labels**: Downweight examples with inconsistent gradients
- **Accelerated training**: Reduce iterations while maintaining quality

Adaptive minibatch selection bridges optimization theory (variance reduction) with practical data characteristics, offering significant speedups in training time.
