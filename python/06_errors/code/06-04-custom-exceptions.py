"""Domain-specific errors for a payment processing system."""


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


class TemperatureError(Exception):
    """Base for temperature errors."""


class TooHotError(TemperatureError):
    def __init__(self, temp: float, limit: float):
        self.temp = temp
        self.limit = limit
        super().__init__(f"temp {temp}° exceeds limit {limit}°")


class TooColdError(TemperatureError):
    def __init__(self, temp: float, limit: float):
        self.temp = temp
        self.limit = limit
        super().__init__(f"temp {temp}° below limit {limit}°")


def check_temperature(temp: float) -> str:
    if temp > 40:
        raise TooHotError(temp, 40)
    if temp < 0:
        raise TooColdError(temp, 0)
    return f"Temperature {temp}° is safe"


for bal, amt, card, attempt in [(500, 100, "1234", 1), (50, 100, "5678", 1), (500, 50, "9999", 4)]:
    try:
        result = f"Payment of ${amt:.2f} approved"
        print(f"OK: {result}")
    except InsufficientFundsError as e:
        print(f"Insufficient: {e}")

for temp in [25, 50, -5]:
    try:
        print(check_temperature(temp))
    except TooHotError as e:
        print(f"Too hot: {e}")
    except TooColdError as e:
        print(f"Too cold: {e}")
