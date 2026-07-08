# 06.03 Forward-Mode Autograd

Forward-mode autograd computes directional derivatives alongside the forward pass using dual numbers.

## Dual Numbers

A dual number is a + bε where ε² = 0. Arithmetic follows:

```
(a + bε) + (c + dε) = (a + c) + (b + d)ε
(a + bε) * (c + dε) = (ac) + (bc + ad)ε
```

The ε coefficient carries the derivative.

## Propagation

Every variable is annotated with a tangent (derivative with respect to a chosen seed). Operations propagate tangents via the chain rule:

```
y = f(x)
ẏ = f'(x) * ẋ
```

## Example: f(x, y) = x² + y, seeded for ∂/∂x

```
x = 3 + 1ε   (tangent = 1)
y = 5 + 0ε   (tangent = 0)
t = x² = 9 + 6ε   (3²=9, 2*3*1=6)
f = t + y = 14 + 6ε
∂f/∂x = 6
```

## Advantages

- Natural for ∂f/∂x where f is scalar and x is one variable
- No need to store the graph — derivatives flow forward
- No "reverse tape" memory cost
- Handles branches and loops naturally

## Disadvantages

- O(n) passes for n inputs — terrible for neural nets (millions of params)
- Each pass requires re-running the entire computation

## When to Use

- Few inputs, many outputs (e.g., Jacobian of a small function)
- Hessian-vector products (repeated forward mode)
- Combined with reverse mode in mixed-mode AD

## Dual Number Implementation

Represent as `(primal, tangent)` tuple. Overload arithmetic operators to propagate tangents.
