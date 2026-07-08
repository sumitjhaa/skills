"""06.03 - Forward-Mode Autograd: Dual numbers and directional derivatives"""

import numpy as np


class Dual:
    """Dual number a + b*eps where eps^2 = 0."""
    def __init__(self, primal, tangent=0.0):
        self.primal = primal
        self.tangent = tangent

    def __add__(self, other):
        if not isinstance(other, Dual):
            other = Dual(other)
        return Dual(self.primal + other.primal, self.tangent + other.tangent)

    def __mul__(self, other):
        if not isinstance(other, Dual):
            other = Dual(other)
        return Dual(self.primal * other.primal,
                    self.primal * other.tangent + self.tangent * other.primal)

    def __pow__(self, n):
        return Dual(self.primal ** n, n * self.primal ** (n - 1) * self.tangent)

    def __neg__(self):
        return Dual(-self.primal, -self.tangent)

    def __sub__(self, other):
        return self + (-other)

    def __truediv__(self, other):
        if not isinstance(other, Dual):
            other = Dual(other)
        return Dual(self.primal / other.primal,
                    (self.tangent * other.primal - self.primal * other.tangent) / other.primal ** 2)

    def sin(self):
        return Dual(np.sin(self.primal), np.cos(self.primal) * self.tangent)

    def cos(self):
        return Dual(np.cos(self.primal), -np.sin(self.primal) * self.tangent)

    def exp(self):
        return Dual(np.exp(self.primal), np.exp(self.primal) * self.tangent)

    def log(self):
        return Dual(np.log(self.primal), self.tangent / self.primal)

    def __repr__(self):
        return f"Dual({self.primal}, {self.tangent})"


def f(x, y):
    return x * x + y * y + x * y


if __name__ == "__main__":
    x = Dual(3.0, 1.0)
    y = Dual(4.0, 0.0)
    result = f(x, y)
    print(f"f(x,y) = x^2 + y^2 + xy at x=3, y=4")
    print(f"f = {result.primal}")
    print(f"df/dx = {result.tangent}  (expected: 2*3 + 4 = 10)")

    x2 = Dual(3.0, 0.0)
    y2 = Dual(4.0, 1.0)
    result2 = f(x2, y2)
    print(f"df/dy = {result2.tangent}  (expected: 2*4 + 3 = 11)")

    z = Dual(1.0, 1.0)
    g = z.sin() * z.exp() + z.log()
    print(f"\ng(z) = sin(z)*exp(z) + log(z) at z=1")
    print(f"g = {g.primal:.6f}")
    print(f"dg/dz = {g.tangent:.6f}")
