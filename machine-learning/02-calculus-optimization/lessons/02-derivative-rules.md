# 02. Derivative Rules

## Introduction

Derivative rules allow us to differentiate complex functions analytically without resorting to limits each time. These rules are the backbone of backpropagation in neural networks.

## Basic Rules

### Constant Rule
```
d/dx [c] = 0
```

### Power Rule
```
d/dx [xⁿ] = n·xⁿ⁻¹
```

### Constant Multiple Rule
```
d/dx [c·f(x)] = c·f'(x)
```

### Sum Rule
```
d/dx [f(x) ± g(x)] = f'(x) ± g'(x)
```

## Product Rule

```
d/dx [f(x)·g(x)] = f'(x)·g(x) + f(x)·g'(x)
```

```python
import numpy as np

def product_rule(f, g, fp, gp, x):
    return fp(x) * g(x) + f(x) * gp(x)

f = lambda x: x**2
g = lambda x: np.sin(x)
fp = lambda x: 2*x
gp = lambda x: np.cos(x)

x = 1.0
print(f"Product rule: {product_rule(f, g, fp, gp, x):.6f}")
```

## Quotient Rule

```
d/dx [f(x)/g(x)] = (f'(x)g(x) - f(x)g'(x)) / [g(x)]²
```

## Chain Rule

The chain rule is the most important rule for deep learning:

```
d/dx [f(g(x))] = f'(g(x)) · g'(x)
```

```python
def chain_rule(f, g, fp, gp, x):
    return fp(g(x)) * gp(x)

# f(u) = u², g(x) = sin(x)
# d/dx sin²(x) = 2·sin(x)·cos(x)
f = lambda u: u**2
g = lambda x: np.sin(x)
fp = lambda u: 2*u
gp = lambda x: np.cos(x)

x = 1.0
manual = chain_rule(f, g, fp, gp, x)
numerical = (f(g(x + 1e-7)) - f(g(x - 1e-7))) / (2 * 1e-7)
print(f"Chain rule: {manual:.6f}, numerical: {numerical:.6f}")
```

## Automatic Differentiation

Modern ML frameworks implement automatic differentiation by applying the chain rule to elementary operations, building a computation graph and propagating gradients backward (reverse-mode autodiff).
