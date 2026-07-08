# 36. Full Optimizer Zoo

## Introduction

This lesson provides a comprehensive comparison of optimizers across benchmark problems, helping practitioners understand which optimizer to choose for different scenarios.

## Optimizer Taxonomy

### First-Order Methods
- **SGD**: Basic, no momentum
- **Momentum**: Velocity accumulation, β ≈ 0.9
- **NAG**: Nesterov's lookahead gradient
- **AdaGrad**: Per-parameter adaptive LR for sparse data
- **RMSprop**: Moving average of squared gradients
- **Adam**: Momentum + RMSprop with bias correction
- **AdaMax**: Adam with L∞ norm
- **Nadam**: Adam with Nesterov momentum
- **AMSGrad**: Adam with max squared gradient

### Second-Order Methods
- **Newton**: Full Hessian (impractical for large n)
- **BFGS**: Dense inverse Hessian approximation
- **L-BFGS**: Limited-memory BFGS
- **AdaHessian**: Diagonal Hessian via Hutchinson

### Stochastic Methods
- **SVRG**: Variance-reduced with snapshot
- **SAGA**: Variance-reduced with per-sample storage
- **SARAH**: Recursive gradient estimation

## Benchmark Functions

### Rosenbrock (Banana) Function
```
f(x, y) = (1 - x)² + 100(y - x²)²
```

A classic test with a narrow curved valley.

### Beale Function
```
f(x, y) = (1.5 - x + xy)² + (2.25 - x + xy²)² + (2.625 - x + xy³)²
```

Multiple local minima.

### Rastrigin Function
```
f(x) = 10n + Σ [xᵢ² - 10cos(2πxᵢ)]
```

Highly multimodal with many local minima.

```python
import numpy as np

rosenbrock = lambda x: (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2
beale = lambda x: (1.5 - x[0] + x[0]*x[1])**2 + (2.25 - x[0] + x[0]*x[1]**2)**2 + (2.625 - x[0] + x[0]*x[1]**3)**2
rastrigin = lambda x: 10*len(x) + np.sum(x**2 - 10*np.cos(2*np.pi*x))
```

## Comparison Methodology

```python
def benchmark_optimizers(problem, x0, optimizers, n_iter=100):
    """Compare multiple optimizers on a problem."""
    results = {}
    for name, opt_fn in optimizers.items():
        x = x0.copy()
        trajectory = [x.copy()]
        for t in range(n_iter):
            g = problem['grad'](x) if 'grad' in problem else None
            x = opt_fn(x, g, t)
            trajectory.append(x.copy())
        results[name] = np.array(trajectory)
    return results
```

## Convergence Speed vs. Final Accuracy

| Optimizer | Rosenbrock | Beale | Rastrigin | MNIST | CIFAR-10 |
|-----------|-----------|-------|-----------|-------|----------|
| SGD | Slow | Slow | Poor | Good | Good |
| Momentum | Medium | Medium | Medium | Good | Good |
| NAG | Medium | Medium | Medium | Good | Good |
| AdaGrad | Poor | Poor | Poor | OK | Poor |
| RMSprop | Fast | Fast | Good | Good | Good |
| Adam | Fast | Fast | Good | Excellent | Excellent |
| L-BFGS | Excellent | Excellent | Poor | N/A | N/A |

## Practical Guidelines

1. **Adam** is the default choice for deep learning
2. **SGD + Momentum** with proper tuning matches Adam on many tasks
3. **RMSprop** is good for RNNs and noisy problems
4. **L-BFGS** is excellent for deterministic, small-to-medium problems
5. **AdaGrad** works well for sparse features (embedding layers)
6. **AMSGrad** helps when Adam fails to converge

No optimizer dominates universally — the choice depends on the problem structure, dataset size, and computational budget.
