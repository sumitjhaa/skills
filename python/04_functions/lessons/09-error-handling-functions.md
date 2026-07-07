# ⚠️ Error Handling in Functions
<!-- ⏱️ 10 min read | 🟡 Medium | 🧠 Applied -->

**What You'll Learn:** How to raise exceptions inside functions, handle them in the caller, and propagate errors through a call chain.

> 💡 **TL;DR — The whole point:** Exceptions travel up the call stack — a function raises, its caller handles, or it bubbles further up.

## 🔗 Why This Matters
Functools showed you caching and dispatch. But what happens when a cached function fails? In real systems — API calls, database queries, payment processing — errors must propagate correctly through layers of function calls.

## The Concept
When an exception occurs inside a function:
1. Python unwinds the stack looking for a matching `except` block
2. If none is found in the current function, it propagates to the caller
3. If the caller doesn't handle it, it propagates further up
4. If nothing handles it, the program crashes

This is like a chain of command: a junior dev (inner function) reports an issue to their manager (caller), who either handles it or escalates up.

## Code Example

```python
"""Error propagation through a chain of API calls — payment processing."""


def validate_payment(card_number: str, amount: float) -> None:
    """Validate payment details."""
    if not card_number or len(card_number) < 13:
        raise ValueError(f"Invalid card number: {card_number}")
    if amount <= 0:
        raise ValueError(f"Invalid amount: {amount}")


def charge_card(card_number: str, amount: float) -> dict:
    """Attempt to charge a card. Caller handles errors."""
    validate_payment(card_number, amount)
    if amount > 10000:
        raise RuntimeError("Amount exceeds authorization limit")
    return {"status": "charged", "amount": amount, "card_last4": card_number[-4:]}


def process_order(order: dict) -> dict:
    """Process an order — handle payment errors gracefully."""
    try:
        payment = charge_card(order["card"], order["total"])
        return {**order, "payment": payment, "status": "completed"}
    except ValueError as e:
        return {**order, "status": "failed", "error": str(e)}
    except RuntimeError as e:
        # Escalate: re-raise with more context
        raise RuntimeError(f"Order {order['id']} failed: {e}") from e


orders = [
    {"id": "ORD-1", "card": "4111111111111111", "total": 50.00},
    {"id": "ORD-2", "card": "1234", "total": 25.00},
    {"id": "ORD-3", "card": "4111111111111111", "total": 50000},
]

for order in orders:
    result = process_order(order)
    print(f"{result['id']}: {result['status']}")

# Unhandled errors propagate to top level
try:
    process_order({"id": "ORD-4", "card": "", "total": -5})
except RuntimeError as e:
    print(f"Escalated: {e}")
```

## 🔍 How It Works
- `raise` inside a function immediately exits the function
- Python walks up the call stack looking for `except`
- If no handler is found → program crashes with traceback
- `raise ... from e` chains exceptions for debugging
- Catch specific exception types, not bare `except:`

## ⚠️ Common Pitfall
Catching too broadly (`except:` or `except Exception`). Catch specific types so unexpected bugs aren't silently swallowed.

## 🧠 Memory Aid
**"Raise it, catch it, or pass it"**: You have three choices — raise (create), catch (handle), or propagate (let it bubble up). Never silently ignore.

## 🏃 Try It
Write `get_user(id)` that raises `ValueError` if `id < 0`, and `fetch_profile(user_id)` that calls it, catches `ValueError`, and returns `{"error": str(e)}`. Test both valid and invalid IDs.

## 🔗 Related
- [Functools Module →](./08-functools.md)
- [Function Composition →](./10-function-composition.md)

## ➡️ Next
[Function Composition](./10-function-composition.md)
