# 🎯 Properties
<!-- ⏱️ 13 min read | 🟡 Core | 🧠 Core -->

**What You'll Learn:** Use `@property` for computed attributes, validation via setters, and read-only attributes with banking domain examples.

> 💡 **TL;DR — The whole point:** Properties let you define methods that look like attributes — giving you control without sacrificing clean syntax.

## 🔗 Why This Matters
A `BankAccount` should prevent negative balances. Without properties, you'd write `account.get_balance()` and `account.set_balance()`. With properties, it's just `account.balance` — with validation built-in.

## The Concept
`@property` turns a method into a read-only attribute. `@setter` adds validation on assignment. `@deleter` handles cleanup. Properties are Python's answer to Java-style getters/setters — but cleaner.

## Code Example
```python
"""Banking: BankAccount with property validation for balance and overdraft."""

class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0):
        self._owner = owner
        self._balance = initial_balance
        self._overdraft_limit = 0

    @property
    def balance(self) -> float:
        """Read-only balance — no direct assignment."""
        return self._balance

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def overdraft_limit(self) -> float:
        return self._overdraft_limit

    @overdraft_limit.setter
    def overdraft_limit(self, limit: float) -> None:
        if limit < 0:
            raise ValueError("Overdraft limit cannot be negative")
        self._overdraft_limit = limit

    @property
    def available_funds(self) -> float:
        """Computed property — balance + overdraft."""
        return self._balance + self._overdraft_limit

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self.available_funds:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        return self._balance


acc = BankAccount("Alice", 1000)
acc.overdraft_limit = 500

print(f"Owner: {acc.owner}")
print(f"Balance: ${acc.balance:.2f}")
print(f"Available: ${acc.available_funds:.2f}")

acc.withdraw(1200)
print(f"After withdrawal: ${acc.balance:.2f}")
print(f"Available: ${acc.available_funds:.2f}")

try:
    acc.balance = 5000  # AttributeError — no setter
except AttributeError as e:
    print(f"Can't set balance directly: {e}")
```

## 🔍 How It Works
- `@property` makes `balance()` into `obj.balance` (read-only)
- `@overdraft_limit.setter` runs validation when assigning to `overdraft_limit`
- `available_funds` is a **computed property** — derived from `_balance + _overdraft_limit`
- Properties use `_name` convention for the backing attribute
- Without a setter, the property is read-only

## ⚠️ Common Pitfall
Naming the property and backing attribute the same (e.g., `self.balance` and `@property def balance`) causes infinite recursion. Use `self._balance`.

## 🧠 Memory Aid
"Property = method dressed as attribute. The `_` prefix is the real data, the `@property` is the public face."

## 🏃 Try It
Add a `@property` for `account_age` that computes days since account opening. Add a `monthly_fee` property with a setter that validates (0–50 range).

## 🔗 Related
- [Encapsulation](07-encapsulation.md) — hiding internal state
- [Dunder Methods](05-dunder-methods.md) — `__getattr__`, `__setattr__`

## ➡️ Next
[Encapsulation](07-encapsulation.md)
