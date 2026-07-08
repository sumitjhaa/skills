# 01. Limits, Continuity & Differentiation

## Introduction

Calculus is the mathematical study of continuous change. The derivative is the fundamental tool for optimization in machine learning — every gradient-based learning algorithm relies on it.

## Limits

The limit of a function `f(x)` as `x` approaches `a` is the value that `f(x)` gets arbitrarily close to:

```
lim_{x→a} f(x) = L
```

Formally (ε-δ definition): For every ε > 0, there exists δ > 0 such that if `0 < |x - a| < δ`, then `|f(x) - L| < ε`.

## Continuity

A function `f` is continuous at `a` if:

1. `f(a)` is defined
2. `lim_{x→a} f(x)` exists
3. `lim_{x→a} f(x) = f(a)`

## Derivative

The derivative of `f` at `x` is defined as the limit of the difference quotient:

```
f'(x) = lim_{h→0} (f(x + h) - f(x)) / h
```

```python
import numpy as np

def derivative(f, x, h=1e-7):
    return (f(x + h) - f(x - h)) / (2 * h)

f = lambda x: x**2
print(f"f'(3) ≈ {derivative(f, 3):.6f} (exact: 6)")
```

The derivative represents the instantaneous rate of change — the slope of the tangent line at a point. In ML, derivatives tell us how to adjust parameters to reduce loss.

## Numerical Differentiation

The central difference formula above has error O(h²), making it more accurate than forward difference. We can compute derivatives numerically for any function:

```python
def forward_difference(f, x, h=1e-7):
    return (f(x + h) - f(x)) / h

def central_difference(f, x, h=1e-7):
    return (f(x + h) - f(x - h)) / (2 * h)

x = np.linspace(-2, 2, 100)
f_vals = f(x)
df_vals = np.array([central_difference(f, xi) for xi in x])

print(f"At x=1: forward={forward_difference(f, 1):.10f}, central={central_difference(f, 1):.10f}, exact=2")
```
