"""06.02 - Reverse-Mode Autograd: Backpropagation via gradient accumulation"""

import numpy as np


class Var:
    """Variable node in a computational graph with reverse-mode autograd."""
    def __init__(self, data, parents=None, grad_fn=None):
        self.data = np.array(data, dtype=np.float64)
        self.grad = np.zeros_like(self.data, dtype=np.float64)
        self.parents = parents or []
        self.grad_fn = grad_fn

    def backward(self, grad=None):
        if grad is None:
            grad = np.ones_like(self.data, dtype=np.float64)
        self.grad = self.grad + grad
        if self.grad_fn is not None:
            incoming = self.grad_fn(grad)
            for parent, pg in zip(self.parents, incoming):
                parent.backward(pg)

    @staticmethod
    def _ensure_var(x):
        return x if isinstance(x, Var) else Var(x)

    def __add__(self, other):
        other = self._ensure_var(other)
        return Var(self.data + other.data, parents=[self, other],
                   grad_fn=lambda g: (g, g))

    def __mul__(self, other):
        other = self._ensure_var(other)
        return Var(self.data * other.data, parents=[self, other],
                   grad_fn=lambda g: (g * other.data, g * self.data))

    def __pow__(self, n):
        return Var(self.data ** n, parents=[self],
                   grad_fn=lambda g: (g * n * self.data ** (n - 1),))

    def __neg__(self):
        return Var(-self.data, parents=[self],
                   grad_fn=lambda g: (-g,))

    def __sub__(self, other):
        return self + (-other)

    def __radd__(self, other):
        return self + other

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self * (other ** -1)

    def __repr__(self):
        return f"Var(data={self.data}, grad={self.grad})"


if __name__ == "__main__":
    a = Var(2.0)
    b = Var(3.0)
    c = a * b
    d = c + a
    print(f"Forward: d = a*b + a = 2*3 + 2 = {d.data}")

    d.backward()
    print(f"Gradient of d w.r.t a: {a.grad}  (expected: b + 1 = 4)")
    print(f"Gradient of d w.r.t b: {b.grad}  (expected: a = 2)")

    x = Var(3.0)
    y = x ** 3 + 2 * x
    y.backward()
    print(f"\ny = x^3 + 2x at x=3: y={y.data}, dy/dx={x.grad}  (expected: 3*9+2=29)")
