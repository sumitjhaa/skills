# 03. Taylor Series

## Introduction

The Taylor series represents a function as an infinite sum of terms calculated from its derivatives at a single point. It is the foundation for many optimization methods, including Newton's method and second-order optimization.

## Taylor Expansion

A function `f` that is infinitely differentiable at `a` can be expanded as:

```
f(x) = Σ_{n=0}^{∞} f⁽ⁿ⁾(a) · (x - a)ⁿ / n!
```

For expansions around 0 (Maclaurin series):

```
f(x) = f(0) + f'(0)x + f''(0)x²/2! + f'''(0)x³/3! + ...
```

## Common Expansions

```
eˣ = 1 + x + x²/2! + x³/3! + ...
sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...
cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + ...
ln(1 + x) = x - x²/2 + x³/3 - x⁴/4 + ...
```

## First-Order (Linear) Approximation

```
f(x) ≈ f(a) + f'(a)(x - a)
```

This is the basis of gradient descent — move in the direction of steepest descent.

## Second-Order Approximation

```
f(x) ≈ f(a) + f'(a)(x - a) + ½f''(a)(x - a)²
```

This is the basis of Newton's method, which uses curvature information for faster convergence.

```python
import numpy as np

def taylor_exp(x, n_terms):
    """Taylor series of e^x around 0."""
    s = 0.0
    term = 1.0
    for n in range(n_terms):
        s += term
        term *= x / (n + 1)
    return s

x_vals = np.linspace(-2, 2, 100)
exact = np.exp(x_vals)

for n in [1, 2, 3, 5]:
    approx = np.array([taylor_exp(x, n) for x in x_vals])
    error = np.max(np.abs(approx - exact))
    print(f"n={n}: max error = {error:.6f}")
```

The error after `n` terms is bounded by `|f⁽ⁿ⁾(ξ)|·|x - a|ⁿ / n!` for some ξ between `a` and `x`.
