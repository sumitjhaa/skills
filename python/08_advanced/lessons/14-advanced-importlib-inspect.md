# 🎯 Advanced importlib & inspect
<!-- ⏱️ 16 min read | 🔴 Mastery | 🧠 Mastery -->

**What You'll Learn:** Use `importlib` for dynamic reloading, `importlib.resources` for package data, and `inspect` for stack/signature introspection.

> 💡 **TL;DR — The whole point:** `importlib` dynamically loads and reloads modules at runtime. `inspect` examines live objects — functions, classes, stack frames, signatures.

## 🔗 Why This Matters
Plugin loaders, hot-reload dev servers, CLI frameworks, and testing tools all need runtime introspection. `importlib` powers Django's migration loading. `inspect` powers pytest's fixture discovery. These modules make the dynamic Python that frameworks rely on.

## The Concept
- `importlib.import_module(name)` — dynamically import a module
- `importlib.reload(module)` — reload an already-imported module
- `importlib.resources.files(package)` — access package data files
- `inspect.signature(func)` — get function parameter info
- `inspect.getmembers(obj)` — list all members of an object
- `inspect.currentframe()` — get the current stack frame
- `inspect.stack()` — get the full call stack

## Code Example
```python
"""E-commerce: Plugin loader with importlib, CLI handler with inspect."""

from importlib import import_module, resources
from typing import Any, Callable
import inspect
import textwrap


# ─── Plugin loader ───
class PluginLoader:
    def __init__(self):
        self._plugins: dict[str, Any] = {}

    def load_plugin(self, module_name: str, class_name: str) -> Any:
        module = import_module(module_name)
        plugin_cls = getattr(module, class_name)
        self._plugins[module_name] = plugin_cls
        return plugin_cls

    def reload_plugin(self, module_name: str) -> Any:
        module = import_module(module_name)
        if module.__spec__:
            from importlib import reload
            module = reload(module)
        return module

    def get_plugins(self) -> dict[str, Any]:
        return dict(self._plugins)


# Simulated plugin module
if "payment_stripe" not in __import__("sys").modules:
    import types
    stripe_module = types.ModuleType("payment_stripe")
    stripe_module.__dict__.update({
        "StripeProcessor": type("StripeProcessor", (), {
            "process": lambda self, amount: f"[Stripe] ${amount}"
        }),
        "name": "stripe",
    })
    __import__("sys").modules["payment_stripe"] = stripe_module


# ─── CLI framework with inspect ───
class CLI:
    def __init__(self):
        self._commands: dict[str, Callable] = {}

    def command(self, func: Callable) -> Callable:
        sig = inspect.signature(func)
        doc = inspect.getdoc(func) or ""
        self._commands[func.__name__] = func

        # Auto-generate help from signature
        params = [
            f"  {name}: {p.annotation.__name__ if p.annotation is not inspect.Parameter.empty else 'any'}"
            for name, p in sig.parameters.items()
        ]
        print(f"[CLI] Registered '{func.__name__}' with params:\n" + "\n".join(params))
        if doc:
            print(f"  Help: {textwrap.shorten(doc, width=40)}")
        return func

    def run(self, command_name: str, **kwargs: Any) -> str:
        cmd = self._commands.get(command_name)
        if not cmd:
            return f"Unknown command: {command_name}"
        return cmd(**kwargs)


cli = CLI()


@cli.command
def create_order(customer: str, total: float, items: int = 0) -> str:
    """Create a new order for a customer."""
    return f"Order created for {customer}: ${total:.2f}"


@cli.command
def apply_discount(price: float, percent: float) -> str:
    """Apply a percentage discount."""
    discounted = price * (1 - percent / 100)
    return f"${price:.2f} → ${discounted:.2f} ({-percent}%)"


# ─── Importlib resources (requires a package with data files) ───
print("\n=== Loading plugins ===")
loader = PluginLoader()
plugin = loader.load_plugin("payment_stripe", "StripeProcessor")
print(f"Loaded: {plugin().process(100.0)}")

print("\n=== CLI commands ===")
print(cli.run("create_order", customer="Alice", total=150.0, items=3))
print(cli.run("apply_discount", price=100.0, percent=10))

print("\n=== Inspection demo ===")
print(f"CLI commands: {list(cli._commands.keys())}")
sig = inspect.signature(create_order)
for name, param in sig.parameters.items():
    print(f"  param '{name}': default={param.default}")
```

## 🔍 How It Works
- `import_module('module.name')` — returns the module object (same as `import` statement)
- `reload(module)` — re-executes the module code (for hot-reloading)
- `importlib.resources` — access data files inside packages without `__file__` hacks
- `inspect.signature(func)` — returns a `Signature` with parameter names, annotations, defaults
- `inspect.getmembers(obj)` — returns `(name, value)` pairs for all attributes
- `inspect.currentframe()` — returns the current execution frame (for debugging/tracing)
- `inspect.stack()` — returns the full call stack as a list of frame records

## ⚠️ Common Pitfall
`reload()` doesn't update references to old objects. If another module has `from plugin import X`, they still reference the old `X`. Only the module itself is updated. Use `import_module` again to get fresh references.

## 🧠 Memory Aid
"importlib = 'import strings.' inspect = 'look at things.' `import_module` = dynamic import. `signature` = 'show me the function's contract.'"

## 🏃 Try It
Write a `function_inspector` function that takes any callable and prints: name, signature, docstring, source file, line number. Test it on `create_order` and a lambda.

## 🔗 Related
- [Packaging](../09_production/lessons/10-packaging.md) — distributing modules
- [Typing Deep](09-typing-deep.md) — annotations for inspect to read

## ➡️ Next
Review and practice with [Exercises](../practice/exercises.md)
