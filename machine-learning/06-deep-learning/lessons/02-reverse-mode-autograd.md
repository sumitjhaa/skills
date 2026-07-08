# 06.02 Reverse-Mode Autograd

Reverse-mode automatic differentiation computes gradients of a scalar output with respect to many inputs in two passes.

## Forward Pass

Traverse the DAG in topological order, computing and storing intermediate values (activations). Each node's `data` field holds its forward result.

## Backward Pass (Reverse Pass)

Traverse the DAG in reverse topological order. Apply the chain rule at each node:

```
∂L/∂x = Σ (∂L/∂y_i) * (∂y_i/∂x)
```

For a node y = f(x₁, x₂, ...), the local gradient ∂y/∂xᵢ is known. The incoming gradient ∂L/∂y is accumulated. Then:

```
∂L/∂xᵢ += ∂L/∂y * ∂y/∂xᵢ
```

## Accumulation

Gradients **accumulate** because a variable may influence the loss through multiple paths. This is why we use `+=` instead of `=`.

## Example: z = (a + b) * c

| Node | Forward | Backward |
|------|---------|----------|
| a    | a_val   | ∂z/∂a = ∂z/∂t * 1 (t = a+b) = c * 1 |
| b    | b_val   | ∂z/∂b = c * 1 |
| +    | t = a+b | ∂z/∂t = c |
| c    | c_val   | ∂z/∂c = t |
| *    | z = t*c | ∂L/∂z (seed) |

## Advantages

- O(n) cost for n operations (same as forward)
- Best for many-parameters-few-outputs (standard ML scenario)
- Exact gradients (no truncation error)

## Limitations

- Requires storing intermediate values (memory O(n))
- Cannot handle branches cleanly in traced graphs

## Implementation Strategy

Each operation defines a `backward` closure that captures its children and calls their `accumulate_grad` method.
