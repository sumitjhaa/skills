"""Error propagation through a chain of API calls — payment processing."""


def validate_payment(card_number: str, amount: float) -> None:
    if not card_number or len(card_number) < 13:
        raise ValueError(f"Invalid card number: {card_number}")
    if amount <= 0:
        raise ValueError(f"Invalid amount: {amount}")


def charge_card(card_number: str, amount: float) -> dict:
    validate_payment(card_number, amount)
    if amount > 10000:
        raise RuntimeError("Amount exceeds authorization limit")
    return {"status": "charged", "amount": amount, "card_last4": card_number[-4:]}


def process_order(order: dict) -> dict:
    try:
        payment = charge_card(order["card"], order["total"])
        return {**order, "payment": payment, "status": "completed"}
    except ValueError as e:
        return {**order, "status": "failed", "error": str(e)}
    except RuntimeError as e:
        raise RuntimeError(f"Order {order['id']} failed: {e}") from e


def get_user(id: int) -> dict:
    if id < 0:
        raise ValueError(f"Invalid user ID: {id}")
    return {"id": id, "name": f"User_{id}"}


def fetch_profile(user_id: int) -> dict:
    try:
        return get_user(user_id)
    except ValueError as e:
        return {"error": str(e)}


orders = [
    {"id": "ORD-1", "card": "4111111111111111", "total": 50.00},
    {"id": "ORD-2", "card": "1234", "total": 25.00},
    {"id": "ORD-3", "card": "4111111111111111", "total": 50000},
]

for o in orders:
    try:
        result = process_order(o)
        print(f"{result['id']}: {result['status']}")
    except RuntimeError as e:
        print(f"{o['id']}: ESCALATED — {e}")

print(fetch_profile(42))
print(fetch_profile(-1))
