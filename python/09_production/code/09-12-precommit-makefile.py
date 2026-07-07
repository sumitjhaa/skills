"""Pre-commit & Makefile — Code that pre-commit hooks check.
Run: python 09-12-precommit-makefile.py
"""

from typing import Final

TAX_RATE: Final[float] = 0.08


def calculate_total(items: list[float], discount: float = 0.0) -> float:
    subtotal = sum(items)
    discounted = subtotal * (1 - discount)
    return round(discounted * (1 + TAX_RATE), 2)


def format_price(amount: float) -> str:
    return f"${amount:,.2f}"


if __name__ == "__main__":
    cart = [29.99, 49.99, 9.99]
    total = calculate_total(cart, discount=0.1)
    print(f"Cart items: {cart}")
    print(f"Total after 10% discount + tax: {format_price(total)}")
