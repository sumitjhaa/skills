"""Input validation, preconditions, and API contracts."""


def get_balance(account: str) -> float:
    db = {"ACC-001": 5000.0, "ACC-002": 1000.0}
    try:
        return db[account]
    except KeyError as e:
        raise ValueError(f"Account {account} not found") from e


def transfer_funds(from_account: str, to_account: str, amount: float) -> dict:
    if not from_account or not to_account:
        raise ValueError("Both accounts must be specified")
    if amount <= 0:
        raise ValueError(f"Amount must be positive, got {amount}")
    balance = get_balance(from_account)
    if amount > balance:
        raise RuntimeError(f"Insufficient funds: have ${balance:.2f}, need ${amount:.2f}")
    assert amount > 0, "Amount should be positive"
    assert balance >= amount, "Balance should be sufficient"
    return {"from": from_account, "to": to_account, "amount": amount, "status": "completed"}


def withdraw(balance: float, amount: float) -> float:
    if amount <= 0:
        raise ValueError(f"Amount must be positive, got {amount}")
    if amount > balance:
        raise ValueError(f"Insufficient funds: have ${balance}, need ${amount}")
    new_balance = balance - amount
    assert new_balance >= 0, "Balance should never be negative"
    return new_balance


print(transfer_funds("ACC-001", "ACC-002", 500))
try:
    transfer_funds("", "ACC-002", 100)
except ValueError as e:
    print(f"Validation error: {e}")
try:
    transfer_funds("ACC-999", "ACC-002", 100)
except ValueError as e:
    print(f"DB error: {e}")
print(withdraw(100, 30))
