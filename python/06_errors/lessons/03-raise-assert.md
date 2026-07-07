# 🚨 Raise & Assert
<!-- ⏱️ 10 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** How to raise exceptions intentionally, chain exceptions with `raise from`, and use assertions for debugging.

> 💡 **TL;DR — The whole point:** `raise` creates errors on purpose; `assert` checks assumptions during development.

## 🔗 Why This Matters
Try/except handles errors that happen. `raise` lets you *create* errors — like a guard checking IDs at the door. `assert` checks your program's internal assumptions during development.

## The Concept
- `raise Exception("message")` — intentionally signal an error
- `raise` — re-raise the current exception (preserving the call stack)
- `raise ... from e` — chain exceptions (the new exception caused by the old one)
- `raise ... from None` — suppress the chain
- `assert condition, message` — debugging check; disabled with `-O` flag

Think of `assert` as a sanity-check for developers, and `raise` as a contract for users.

## Code Example

```python
"""Input validation, preconditions, and API contracts."""


def transfer_funds(from_account: str, to_account: str, amount: float) -> dict:
    """Transfer funds between accounts with validation."""
    # Preconditions — input validation
    if not from_account or not to_account:
        raise ValueError("Both accounts must be specified")
    if amount <= 0:
        raise ValueError(f"Amount must be positive, got {amount}")

    # Simulated business logic
    balance = get_balance(from_account)
    if amount > balance:
        raise RuntimeError(f"Insufficient funds: have ${balance:.2f}, need ${amount:.2f}")

    # Internal assertion (development only)
    assert amount > 0, "Amount should be positive at this point"
    assert balance >= amount, "Balance should be sufficient"

    return {"from": from_account, "to": to_account, "amount": amount, "status": "completed"}


def get_balance(account: str) -> float:
    """Simulate DB lookup — can fail."""
    db = {"ACC-001": 5000.0, "ACC-002": 1000.0}
    try:
        return db[account]
    except KeyError as e:
        raise ValueError(f"Account {account} not found") from e


# Test cases
print(transfer_funds("ACC-001", "ACC-002", 500))

try:
    transfer_funds("", "ACC-002", 100)
except ValueError as e:
    print(f"Validation error: {e}")

try:
    transfer_funds("ACC-001", "ACC-002", 10000)
except RuntimeError as e:
    print(f"Business error: {e}")

try:
    transfer_funds("ACC-999", "ACC-002", 100)
except ValueError as e:
    print(f"DB error chained: {e}")
```

## 🔍 How It Works
- `raise` creates an exception object and unwinds the stack
- `assert` compiles to a `CHECK` opcode; with `-O` it generates nothing
- Exception chaining (`raise from`) sets `__cause__` on the exception
- Use `assert` for internal invariants, not for input validation

## ⚠️ Common Pitfall
Using `assert` for input validation. Assertions are disabled with `-O`. Always use `raise ValueError(...)` for user-facing validation.

## 🧠 Memory Aid
**"raise = contract violation, assert = sanity check"**: Raise when the user does something wrong. Assert when the code does something impossible.

## 🏃 Try It
Write `withdraw(balance, amount)` that raises `ValueError` if `amount <= 0` or `amount > balance`, and uses `assert` to verify balance is non-negative after withdrawal.

## 🔗 Related
- [Try/Except/Else/Finally →](./02-try-except.md)
- [Custom Exceptions →](./04-custom-exceptions.md)

## ➡️ Next
[Custom Exceptions](./04-custom-exceptions.md)
