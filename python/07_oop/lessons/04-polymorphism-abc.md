# 🎯 Polymorphism & ABCs
<!-- ⏱️ 14 min read | 🟡 Core | 🧠 Core -->

**What You'll Learn:** Use duck typing and abstract base classes (ABCs) to write flexible, interface-driven code with finance examples.

> 💡 **TL;DR — The whole point:** Polymorphism means different objects can be used interchangeably if they support the same interface — "if it quacks like a duck..."

## 🔗 Why This Matters
In finance, you might have `Stock`, `Bond`, and `Crypto` — all are "assets" but priced differently. Polymorphism lets you treat them uniformly without messy `if-elif` chains.

## The Concept
**Duck typing** means "if it walks like a duck and quacks like a duck, it's a duck." **ABCs** enforce that subclasses implement required methods — they set the contract.

## Code Example
```python
"""Finance: Asset interface with ABC and polymorphic behavior."""

from abc import ABC, abstractmethod


class Asset(ABC):
    @abstractmethod
    def current_value(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass


class Stock(Asset):
    def __init__(self, ticker: str, shares: int, price_per_share: float):
        self.ticker = ticker
        self.shares = shares
        self.price_per_share = price_per_share

    def current_value(self) -> float:
        return self.shares * self.price_per_share

    def description(self) -> str:
        return f"{self.ticker}: {self.shares} shares @ ${self.price_per_share:.2f}"


class Bond(Asset):
    def __init__(self, name: str, face_value: float, rate: float, years: int):
        self.name = name
        self.face_value = face_value
        self.rate = rate
        self.years = years

    def current_value(self) -> float:
        return self.face_value * (1 + self.rate * self.years)

    def description(self) -> str:
        return f"{self.name}: {self.years}y bond at {self.rate*100}%"


# Polymorphic portfolio — works with any Asset
def portfolio_total(assets: list[Asset]) -> float:
    return sum(a.current_value() for a in assets)


portfolio: list[Asset] = [
    Stock("AAPL", 50, 175.0),
    Stock("GOOGL", 30, 140.0),
    Bond("T-Bond 2030", 10000, 0.05, 10),
]

for asset in portfolio:
    print(f"  {asset.description()} — ${asset.current_value():.2f}")

print(f"\nPortfolio total: ${portfolio_total(portfolio):.2f}")
```

## 🔍 How It Works
- `class Asset(ABC):` marks this as abstract — can't be instantiated directly
- `@abstractmethod` forces subclasses to implement the method
- The polymorphic loop `for a in portfolio: a.current_value()` works regardless of the actual type
- Duck typing doesn't require inheritance — any object with `.current_value()` works
- ABCs catch missing implementations at instantiation time

## ⚠️ Common Pitfall
Trying to instantiate an ABC directly: `Asset()` raises `TypeError`. ABCs are contracts, not concrete classes.

## 🧠 Memory Aid
"ABC = contract. Sign the contract (subclass), fulfill the terms (implement methods)."

## 🏃 Try It
Add a `Crypto` class that implements `Asset`. Include `symbol`, `coins`, and `price_per_coin`. Add it to the portfolio and see polymorphic behavior in action.

## 🔗 Related
- [Inheritance](03-inheritance.md) — base and derived classes
- [Dunder Methods](05-dunder-methods.md) — operator overloading polymorphism

## ➡️ Next
[Dunder Methods](05-dunder-methods.md)
