# 🎨 Custom Exceptions
<!-- ⏱️ 10 min read | 🟡 Medium | 🧠 Applied -->

**What You'll Learn:** How to define your own exception classes, build exception hierarchies, and add useful attributes.

> 💡 **TL;DR — The whole point:** Custom exceptions make your errors meaningful — `InsufficientFundsError` tells you more than just `ValueError`.

## 🔗 Why This Matters
Raise/assert use built-in exceptions. But in real apps, you need domain-specific errors: `InsufficientFunds`, `RateLimitExceeded`, `PaymentDeclined`. Custom exceptions make error handling precise and readable.

## The Concept
Custom exceptions are regular Python classes that inherit from `Exception`. By creating a hierarchy, you can catch broad categories or specific subtypes:
```
PaymentError (catch this)
├── InsufficientFundsError
├── CardDeclinedError
└── NetworkError
```
Catching `PaymentError` catches all three. Catching `InsufficientFundsError` only catches that one.

## Code Example

```python
"""Domain-specific errors for a payment processing system."""

import logging

logger = logging.getLogger(__name__)


class PaymentError(Exception):
    """Base for all payment errors."""


class InsufficientFundsError(PaymentError):
    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        super().__init__(f"need ${amount:.2f}, have ${balance:.2f}")


class CardDeclinedError(PaymentError):
    def __init__(self, card_last4: str, reason: str):
        self.card_last4 = card_last4
        self.reason = reason
        super().__init__(f"card ****{card_last4} declined: {reason}")


class RateLimitExceededError(PaymentError):
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"rate limit exceeded, retry in {retry_after}s")


def process_payment(amount: float, balance: float, card_last4: str, attempt: int) -> str:
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    if attempt > 3:
        raise CardDeclinedError(card_last4, "too many attempts")
    if attempt > 5:
        raise RateLimitExceededError(30)
    return f"Payment of ${amount:.2f} approved"


for bal, amt, card, attempt in [(500, 100, "1234", 1), (50, 100, "5678", 1), (500, 50, "9999", 4), (500, 50, "9999", 6)]:
    try:
        result = process_payment(amt, bal, card, attempt)
        print(f"OK: {result}")
    except InsufficientFundsError as e:
        print(f"Insufficient: {e}")
    except CardDeclinedError as e:
        print(f"Card declined: {e} (card={e.card_last4}, reason={e.reason})")
    except PaymentError as e:
        print(f"Payment error: {e}")
```

## 🔍 How It Works
- Inherit from `Exception` (not `BaseException`)
- Name ends with `Error` (Python convention)
- Call `super().__init__(message)` to set the error message
- Add useful attributes in `__init__` for programmatic handling
- Keep hierarchy shallow — no more than 2-3 levels

## ⚠️ Common Pitfall
Creating a flat list of unrelated custom exceptions. Use a base class so callers can catch all your domain errors: `except MyAppError:`.

## 🧠 Memory Aid
**"DomainError → SpecificError"**: Think of your exception hierarchy like a file cabinet — one drawer (DomainError) with folders (SpecificErrors) inside.

## 🏃 Try It
Create a `TemperatureError` hierarchy: `TemperatureError` → `TooHotError(temp, limit)` and `TooColdError(temp, limit)`. Write a function `check_temperature(temp)` that raises the appropriate error.

## 🔗 Related
- [Raise & Assert →](./03-raise-assert.md)
- [Context Managers →](./05-context-managers.md)

## ➡️ Next
[Context Managers](./05-context-managers.md)
