# 06.04 Full Autograd Framework

Combine DAG construction, reverse-mode accumulation, and forward-mode into a unified `Tensor` class.

## Tensor Class

```python
class Tensor:
    def __init__(self, data, children=(), op=None, requires_grad=True):
        self.data = np.array(data, dtype=np.float64)
        self.grad = np.zeros_like(self.data)
        self._children = children
        self._op = op
        self.requires_grad = requires_grad
        self._backward = lambda: None
```

## Operation Overloading

Overload `__add__`, `__mul__`, `__matmul__`, `__neg__`, etc. to:

1. Compute the forward result as a new Tensor
2. Record operation and parent references in the graph
3. Define a `_backward` closure that propagates gradients

## Building the Tape

With eager-mode autograd, the graph is built implicitly:

```python
a = Tensor([1.0])
b = Tensor([2.0])
c = a * b        # creates new Tensor node
d = c + a        # creates another node
```

## Backward()

Calling `backward()` on a scalar:

1. Topological sort the graph
2. Seed gradient = 1.0
3. Process nodes in reverse order, calling each `_backward`
4. Gradients accumulate in `.grad`

## Gradient Accumulation

Multiple paths to the same node cause gradient addition:

```python
x = Tensor([3.0])
y = x * x + x * x    # x used twice
y.backward()          # grad = 2x + 2x = 12 (for x=3)
```

## Detach / No-Grad

For inference or when gradients shouldn't flow:

- `detach()`: returns a new Tensor not connected to the graph
- `no_grad` context manager: temporarily disables gradient tracking

## Validation

Test against finite differences for every operation.

## Interfaces

The framework exposes:

- Core tensor ops (add, mul, matmul, neg, sub, div, pow, exp, log, sin, cos, tanh, relu, sum, mean)
- Reduction ops with correct broadcasting support
- In-place ops (careful: must not break the tape)
