"""07-13-init-subclass.py — E-commerce: Plugin system with __init_subclass__."""

from typing import ClassVar


class PaymentPlugin:
    registry: ClassVar[dict[str, type["PaymentPlugin"]]] = {}

    def __init_subclass__(cls, name: str | None = None, **kwargs):
        super().__init_subclass__(**kwargs)
        final_name = name if name else getattr(cls, "name", cls.__name__.lower())
        cls.name = final_name
        PaymentPlugin.registry[final_name] = cls

    def process(self, amount: float) -> str:
        raise NotImplementedError


class StripePayment(PaymentPlugin, name="stripe"):
    def process(self, amount: float) -> str:
        return f"[Stripe] Charged ${amount:.2f} (fee: ${amount*0.029:.2f})"


class PayPalPayment(PaymentPlugin):
    name = "paypal"

    def process(self, amount: float) -> str:
        return f"[PayPal] Charged ${amount:.2f} (fee: ${amount*0.039:.2f})"


class CryptoPayment(PaymentPlugin, name="crypto"):
    def process(self, amount: float) -> str:
        return f"[Crypto] Charged ${amount:.2f} (fee: ${amount*0.01:.2f})"


def process_payment(method: str, amount: float) -> str:
    plugin = PaymentPlugin.registry.get(method)
    if not plugin:
        return f"Unknown method: {method}"
    return plugin().process(amount)


print(f"Available: {list(PaymentPlugin.registry.keys())}")
for method in ["stripe", "paypal", "crypto", "bitcoin"]:
    print(f"  {process_payment(method, 100.0)}")
