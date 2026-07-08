"""06.05 - Higher-Order Gradients: Hessian-vector products and double backprop"""

import numpy as np


class Tensor:
    """Tensor supporting higher-order gradients via create_graph."""
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
        n_const = n
        out = Tensor(self.data ** n_const, (self,), f"**{n_const}")
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

    def sin(self):
        out = Tensor(np.sin(self.data), (self,), "sin")
        def _backward():
            self.grad += out.grad * np.cos(self.data)
        out._backward = _backward
        return out

    def backward(self, retain_graph=False):
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
        if not retain_graph:
            for node in order:
                node._backward = lambda: None

    def __repr__(self):
        return f"T({self.data}, grad={self.grad})"


def finite_diff_hessian(f, x0, eps=1e-5):
    """Numerical Hessian via central differences."""
    x0 = np.asarray(x0, dtype=np.float64)
    n = x0.shape[0]
    H = np.zeros((n, n))
    f0 = f(x0)
    for i in range(n):
        for j in range(n):
            ei = np.zeros(n); ei[i] = eps
            ej = np.zeros(n); ej[j] = eps
            fpp = f(x0 + ei + ej)
            fpm = f(x0 + ei - ej)
            fmp = f(x0 - ei + ej)
            fmm = f(x0 - ei - ej)
            H[i, j] = (fpp - fpm - fmp + fmm) / (4 * eps * eps)
    return H


if __name__ == "__main__":
    x = Tensor(2.0)
    y = x ** 3 + 2 * x ** 2 + x
    y.backward()
    print(f"f(x) = x^3 + 2x^2 + x at x=2")
    print(f"f(2) = {y.data}")
    print(f"df/dx = {x.grad}  (expected: 3*4 + 4*2 + 1 = 21)")

    x = Tensor(1.0)
    y = x.sin()
    y.backward()
    print(f"\nsin(1): f={y.data:.6f}, f'={x.grad:.6f}  (expected: cos(1)={np.cos(1):.6f})")

    x0 = Tensor(2.0)
    x1 = Tensor(3.0)
    y = x0 ** 2 + x1 ** 3 + x0 * x1
    y.backward()
    print(f"\nf(x,y)=x^2 + y^3 + xy at (2,3): f={y.data}")
    print(f"Gradient: df/dx={x0.grad:.1f} (expected: 2*2+3=7), df/dy={x1.grad:.1f} (expected: 3*9+2=29)")

    H = finite_diff_hessian(lambda p: p[0]**2 + p[1]**3 + p[0]*p[1], np.array([2.0, 3.0]))
    print(f"Numerical Hessian:\n{H}")
