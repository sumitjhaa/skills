# 🎯 \_\_init\_subclass\_\_
<!-- ⏱️ 15 min read | 🔴 Mastery | 🧠 Mastery -->

**What You'll Learn:** Use `__init_subclass__` to auto-register subclasses, implement plugin systems, and replace metaclasses for common use cases.

> 💡 **TL;DR — The whole point:** `__init_subclass__` runs when a class is subclassed — it's a hook to modify or register every subclass without a metaclass.

## 🔗 Why This Matters
Plugin systems, factory registries, and UI component libraries all need to know about their subclasses. `__init_subclass__` is simpler than metaclasses for these patterns — it runs automatically when anyone subclasses your class.

## The Concept
`__init_subclass__(cls, **kwargs)` is called on the parent class whenever a child class is defined. It receives the child class and any extra keyword arguments from the class definition.

## Code Example
```python
"""E-commerce: Plugin system with auto-registration via __init_subclass__."""

from typing import ClassVar


class PaymentPlugin:
    registry: ClassVar[dict[str, type["PaymentPlugin"]]] = {}

    def __init_subclass__(cls, name: str | None = None, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-register with a readable name
        final_name = name if name else getattr(cls, "name", cls.__name__.lower())
        cls.name = final_name
        PaymentPlugin.registry[final_name] = cls
        print(f"[Plugin] Registered '{name}' → {cls.__name__}")

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
    plugin_cls = PaymentPlugin.registry.get(method)
    if not plugin_cls:
        return f"Unknown payment method: {method}"
    return plugin_cls().process(amount)


print("\n=== Registered payment plugins ===")
print(f"Available: {list(PaymentPlugin.registry.keys())}")

print("\n=== Processing payments ===")
for method in ["stripe", "paypal", "crypto", "bitcoin"]:
    print(f"  {process_payment(method, 100.0)}")
```

## 🔍 How It Works
- `__init_subclass__` is called automatically when `class StripePayment(PaymentPlugin):` is defined
- The `name` keyword in `class StripePayment(PaymentPlugin, name="stripe")` is passed as `**kwargs`
- `super().__init_subclass__(**kwargs)` ensures proper MRO when there's inheritance chains
- The registry pattern lets you discover all subclasses without explicit registration
- This is the backbone of plugin systems, factory patterns, and UI component frameworks

## ⚠️ Common Pitfall
Forgetting `super().__init_subclass__(**kwargs)` when mixing with other classes that also use `__init_subclass__`. Always call `super()` to maintain the chain.

## 🧠 Memory Aid
"`__init_subclass__` = 'when someone inherits from me, let me know.' It's like a callback for inheritance."

## 🏃 Try It
Create a `NotificationPlugin` base class with `__init_subclass__` that registers subclasses by name. Create `EmailNotification`, `SMSNotification`, and `PushNotification` plugins.

## 🔗 Related
- [Metaclasses](12-metaclasses.md) — more powerful class modification
- [\_\_set_name\_\_ & \_\_class_getitem\_\_](14-set-name-class-getitem.md) — descriptor protocol

## ➡️ Next
[__set_name__ & __class_getitem__](14-set-name-class-getitem.md)
