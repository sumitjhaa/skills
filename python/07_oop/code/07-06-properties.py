"""07-06-properties.py — Banking: BankAccount with property validation."""

class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0):
        self._owner = owner
        self._balance = initial_balance
        self._overdraft_limit = 0

    @property
    def balance(self) -> float:
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
