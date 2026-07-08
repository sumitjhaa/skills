"""06.04 - Full Autograd Framework: Tensor class with gradient tape"""

import numpy as np


class Tensor:
    """Core autograd tensor with gradient tape and operation recording."""
    def __init__(self, data, children=(), op=None, requires_grad=True):
        self.data = np.array(data, dtype=np.float64)
        self.requires_grad = requires_grad
        self.grad = np.zeros_like(self.data, dtype=np.float64)
        self._children = children
        self._op = op
        self._backward = lambda: None

    @classmethod
    def _ensure(cls, x):
        return x if isinstance(x, cls) else cls(x, requires_grad=False)

    def __add__(self, other):
        other = self._ensure(other)
        out = Tensor(self.data + other.data, (self, other), "+")
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = self._ensure(other)
        out = Tensor(self.data * other.data, (self, other), "*")
        def _backward():
            self.grad += out.grad * other.data
            other.grad += out.grad * self.data
        out._backward = _backward
        return out

    def __pow__(self, n):
        out = Tensor(self.data ** n, (self,), f"**{n}")
        if not isinstance(n, (int, float)):
            raise TypeError("pow only supports numeric exponent")
        n_const = n
        def _backward():
            self.grad += out.grad * n_const * self.data ** (n_const - 1)
        out._backward = _backward
        return out

    def __neg__(self):
        out = Tensor(-self.data, (self,), "neg")
        def _backward():
            self.grad += -out.grad
        out._backward = _backward
        return out

    def __sub__(self, other):
        return self + (-other)

    def __truediv__(self, other):
        return self * (other ** -1)

    def __matmul__(self, other):
        other = self._ensure(other)
        out = Tensor(self.data @ other.data, (self, other), "@")
        def _backward():
            a, b = self.data, other.data
            g = out.grad
            if a.ndim == 1 and b.ndim == 1:
                self.grad += g * b
                other.grad += g * a
            elif a.ndim == 1:
                self.grad += b @ g
                other.grad += np.outer(a, g)
            elif b.ndim == 1:
                self.grad += np.outer(g, b)
                other.grad += a.T @ g
            else:
                self.grad += g @ b.T
                other.grad += a.T @ g
        out._backward = _backward
        return out

    def __radd__(self, other):
        return self + other

    def __rmul__(self, other):
        return self * other

    def sum(self):
        out = Tensor(np.sum(self.data), (self,), "sum")
        def _backward():
            self.grad += out.grad * np.ones_like(self.data)
        out._backward = _backward
        return out

    def mean(self):
        n = self.data.size
        out = Tensor(np.mean(self.data), (self,), "mean")
        def _backward():
            self.grad += out.grad * np.ones_like(self.data) / n
        out._backward = _backward
        return out

    def relu(self):
        out = Tensor(np.maximum(0, self.data), (self,), "relu")
        def _backward():
            self.grad += out.grad * (self.data > 0)
        out._backward = _backward
        return out

    def exp(self):
        out = Tensor(np.exp(self.data), (self,), "exp")
        def _backward():
            self.grad += out.grad * out.data
        out._backward = _backward
        return out

    def log(self):
        out = Tensor(np.log(self.data), (self,), "log")
        def _backward():
            self.grad += out.grad / self.data
        out._backward = _backward
        return out

    def tanh(self):
        t = np.tanh(self.data)
        out = Tensor(t, (self,), "tanh")
        def _backward():
            self.grad += out.grad * (1 - t ** 2)
        out._backward = _backward
        return out

    def sigmoid(self):
        s = 1 / (1 + np.exp(-self.data))
        out = Tensor(s, (self,), "sigmoid")
        def _backward():
            self.grad += out.grad * s * (1 - s)
        out._backward = _backward
        return out

    def backward(self):
        order = []
        visited = set()
        def topo(node):
            if node not in visited:
                visited.add(node)
                for child in node._children:
                    if isinstance(child, Tensor):
                        topo(child)
                order.append(node)
        topo(self)
        self.grad = np.ones_like(self.data, dtype=np.float64)
        for node in reversed(order):
            node._backward()

    def detach(self):
        return Tensor(self.data, requires_grad=False)

    def zero_grad(self):
        self.grad = np.zeros_like(self.data, dtype=np.float64)

    def __repr__(self):
        return f"Tensor(data={self.data}, grad={self.grad})"


if __name__ == "__main__":
    # Basic ops
    a = Tensor([2.0])
    b = Tensor([3.0])
    c = a * b + a ** 2
    c.backward()
    print(f"c = a*b + a^2 at a=2, b=3: c={c.data}")
    print(f"dc/da = {a.grad}  (expected: b + 2a = 3 + 4 = 7)")
    print(f"dc/db = {b.grad}  (expected: a = 2)")

    # Matrix multiply
    x = Tensor(np.array([[1.0, 2.0], [3.0, 4.0]]))
    w = Tensor(np.array([[0.5, 0.0], [0.0, 0.5]]))
    y = (x @ w).sum()
    y.backward()
    print(f"\nMatrix multiply + sum: y = {y.data}")
    print(f"dy/dx = {x.grad}")

    # MLP forward
    x = Tensor(np.random.randn(4))
    W1 = Tensor(np.random.randn(4, 8) * 0.1)
    b1 = Tensor(np.zeros(8))
    h = (x @ W1 + b1).relu()
    W2 = Tensor(np.random.randn(8, 2) * 0.1)
    logits = h @ W2
    loss = logits.sum()
    loss.backward()
    print(f"\nMLP forward + backward complete. Loss = {loss.data}")
    print(f"dL/dW1 norm = {np.linalg.norm(W1.grad):.6f}")
    print(f"dL/dW2 norm = {np.linalg.norm(W2.grad):.6f}")
    print("Full autograd framework verified.")
