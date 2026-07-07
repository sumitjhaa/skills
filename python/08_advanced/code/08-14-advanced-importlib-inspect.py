"""08-14-advanced-importlib-inspect.py — Plugin loader, CLI framework."""

from importlib import import_module
from typing import Any, Callable
import inspect
import textwrap


class PluginLoader:
    def __init__(self):
        self._plugins: dict[str, Any] = {}

    def load_plugin(self, module_name: str, class_name: str) -> Any:
        module = import_module(module_name)
        plugin_cls = getattr(module, class_name)
        self._plugins[module_name] = plugin_cls
        return plugin_cls

    def get_plugins(self) -> dict[str, Any]:
        return dict(self._plugins)


import types
stripe_module = types.ModuleType("payment_stripe")
stripe_module.__dict__.update({
    "StripeProcessor": type("StripeProcessor", (), {
        "process": lambda self, amount: f"[Stripe] ${amount}"
    }),
})
import sys
sys.modules["payment_stripe"] = stripe_module


class CLI:
    def __init__(self):
        self._commands: dict[str, Callable] = {}

    def command(self, func: Callable) -> Callable:
        sig = inspect.signature(func)
        self._commands[func.__name__] = func
        params = [
            f"  {name}: {p.annotation.__name__ if p.annotation is not inspect.Parameter.empty else 'any'}"
            for name, p in sig.parameters.items()
        ]
        print(f"[CLI] '{func.__name__}'\n" + "\n".join(params))
        return func

    def run(self, command_name: str, **kwargs: Any) -> str:
        cmd = self._commands.get(command_name)
        if not cmd:
            return f"Unknown: {command_name}"
        return cmd(**kwargs)


cli = CLI()


@cli.command
def create_order(customer: str, total: float, items: int = 0) -> str:
    return f"Order for {customer}: ${total:.2f}"


@cli.command
def apply_discount(price: float, percent: float) -> str:
    discounted = price * (1 - percent / 100)
    return f"${price:.2f} → ${discounted:.2f}"


loader = PluginLoader()
plugin = loader.load_plugin("payment_stripe", "StripeProcessor")
print(f"\nLoaded plugin: {plugin().process(100.0)}")

print("\n=== CLI ===")
print(cli.run("create_order", customer="Alice", total=150.0, items=3))
print(cli.run("apply_discount", price=100.0, percent=10))
