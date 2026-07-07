"""07-04-polymorphism-abc.py — Finance: Asset interface with ABC and polymorphism."""

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


def portfolio_total(assets: list[Asset]) -> float:
    return sum(a.current_value() for a in assets)


portfolio = [
    Stock("AAPL", 50, 175.0),
    Stock("GOOGL", 30, 140.0),
    Bond("T-Bond 2030", 10000, 0.05, 10),
]

for asset in portfolio:
    print(f"  {asset.description()} — ${asset.current_value():.2f}")

print(f"\nPortfolio total: ${portfolio_total(portfolio):.2f}")
