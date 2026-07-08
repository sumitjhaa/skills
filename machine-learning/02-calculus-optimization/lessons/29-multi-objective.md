# 29. Multi-Objective Optimization

## Introduction

Many real-world problems require optimizing multiple conflicting objectives simultaneously (e.g., accuracy vs. latency, performance vs. energy). Multi-objective optimization finds Pareto-optimal trade-offs.

## Pareto Optimality

A solution `x*` is Pareto optimal if no objective can be improved without degrading another.

The Pareto front is the set of all Pareto-optimal solutions.

```python
import numpy as np

def is_pareto_efficient(costs):
    """Find Pareto-efficient points."""
    n = len(costs)
    is_efficient = np.ones(n, dtype=bool)
    for i in range(n):
        for j in range(n):
            if i != j and np.all(costs[j] <= costs[i]) and np.any(costs[j] < costs[i]):
                is_efficient[i] = False
                break
    return is_efficient
```

## Scalarization Methods

### Weighted Sum

```
minimize Σᵢ wᵢ fᵢ(x)  where wᵢ ≥ 0, Σ wᵢ = 1
```

```python
def weighted_sum(f_list, weights, x0):
    """Minimize weighted sum of objectives."""
    from scipy.optimize import minimize
    objective = lambda x: sum(w * f(x) for w, f in zip(weights, f_list))
    return minimize(objective, x0)
```

### ε-Constraint Method

Optimize one objective while constraining others:

```
minimize f₁(x)
subject to f₂(x) ≤ ε₂, ..., fₘ(x) ≤ εₘ
```

## NSGA-II (Non-dominated Sorting Genetic Algorithm)

NSGA-II is a population-based multi-objective optimizer:

1. **Non-dominated sorting**: Rank solutions by Pareto dominance
2. **Crowding distance**: Maintain diversity in each front
3. **Selection**: Tournament selection based on rank and crowding

```python
def nsga2_crowding_distance(front):
    """Compute crowding distance for a Pareto front."""
    n = len(front)
    m = front.shape[1]
    distance = np.zeros(n)

    for obj in range(m):
        idx = np.argsort(front[:, obj])
        distance[idx[0]] = np.inf
        distance[idx[-1]] = np.inf
        for i in range(1, n - 1):
            distance[idx[i]] += (front[idx[i+1], obj] - front[idx[i-1], obj])

    return distance
```

## Hypervolume Indicator

The hypervolume measures the quality of a Pareto front by computing the volume dominated by the front relative to a reference point:

```python
def hypervolume_indicator(front, ref_point):
    """Compute hypervolume (simplified 2D version)."""
    front = front[np.argsort(front[:, 0])]
    hv = 0.0
    prev_x = ref_point[0]
    for i in range(len(front) - 1, -1, -1):
        hv += (prev_x - front[i, 0]) * (ref_point[1] - front[i, 1])
        prev_x = front[i, 0]
    return hv
```

## Applications in ML

- **Neural architecture search**: Accuracy vs. FLOPs
- **Model compression**: Size vs. accuracy
- **Fairness**: Accuracy vs. fairness metrics
- **Reinforcement learning**: Reward vs. risk

Multi-objective optimization provides principled methods for navigating trade-offs central to practical ML systems.
