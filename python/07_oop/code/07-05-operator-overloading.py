"""Operator overloading — Money with +, -, *, /, unary, in-place."""
class Money:
    def __init__(self, amount, currency="USD"):
        self.amount, self.currency = amount, currency
    def __repr__(self):
        return f"Money({self.amount:.2f} {self.currency})"
    def __eq__(self, other):
        if isinstance(other, Money):
            return self.amount == other.amount and self.currency == other.currency
        return NotImplemented
    def __neg__(self):
        return Money(-self.amount, self.currency)
    def __abs__(self):
        return Money(abs(self.amount), self.currency)
    def __add__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            return Money(self.amount + other.amount, self.currency)
        return NotImplemented
    def __radd__(self, other):
        if isinstance(other, (int, float)):
            return Money(self.amount + other, self.currency)
        return NotImplemented
    def __sub__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            return Money(self.amount - other.amount, self.currency)
        return NotImplemented
    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Money(self.amount * scalar, self.currency)
        return NotImplemented
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Money(self.amount / scalar, self.currency)
        return NotImplemented
    def __iadd__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            self.amount += other.amount
            return self
        return NotImplemented
    def __lt__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            return self.amount < other.amount
        return NotImplemented

m1 = Money(100, "USD")
m2 = Money(50, "USD")
print(f"{m1} + {m2} = {m1 + m2}")
print(f"3 * {m1} = {3 * m1}, {m1} * 2 = {m1 * 2}")
print(f"/4: {m1 / 4}, -: {-m1}, abs: {abs(Money(-50,'USD'))}")
print(f"{m2} < {m1}: {m2 < m1}, eq: {m1 == Money(100,'USD')}")
m1 += Money(25, "USD")
print(f"after +=: {m1}")
