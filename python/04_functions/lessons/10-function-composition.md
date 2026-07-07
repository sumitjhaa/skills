# 🔗 Function Composition
<!-- ⏱️ 10 min read | 🔴 Hard | 🧠 Mastery -->

**What You'll Learn:** How to combine functions into pipelines using composition, pipe patterns, and middleware chains.

> 💡 **TL;DR — The whole point:** Function composition chains functions so the output of one becomes the input of the next — like an assembly line.

## 🔗 Why This Matters
Error handling showed you how to manage failures in a call chain. Now learn how to *design* those chains intentionally — connecting functions like pipes in a data processing pipeline.

## The Concept
**Function composition** combines two or more functions to produce a new function. If `f(x)` and `g(x)` exist, `compose(f, g)(x)` = `f(g(x))`. A **pipe** does the reverse: `pipe(g, f)(x)` = `f(g(x))` — data flows left-to-right.

Think of it like an assembly line: raw materials go in (input), pass through stations (functions), and a finished product comes out. Each station transforms the work piece.

## Code Example

```python
"""Data processing pipeline — pipe patterns and middleware chains."""

from functools import reduce
import re


def pipe(*funcs):
    """Left-to-right function composition."""
    def applied(x):
        for f in funcs:
            x = f(x)
        return x
    return applied


def compose(*funcs):
    """Right-to-left function composition (mathematical)."""
    def applied(x):
        for f in reversed(funcs):
            x = f(x)
        return x
    return applied


def step(data: dict) -> dict:
    """Pipeline steps for processing a sales order."""

    def validate(order: dict) -> dict:
        if "items" not in order or not order["items"]:
            raise ValueError("Order has no items")
        return order

    def calculate_totals(order: dict) -> dict:
        order["subtotal"] = sum(item["price"] * item["qty"] for item in order["items"])
        order["tax"] = round(order["subtotal"] * 0.08, 2)
        order["total"] = round(order["subtotal"] + order["tax"], 2)
        return order

    def format_response(order: dict) -> dict:
        order["summary"] = (
            f"Order {order['id']}: {len(order['items'])} items, "
            f"total ${order['total']}"
        )
        return order

    return pipe(validate, calculate_totals, format_response)(data)


# Middleware chain — like Express.js or Django middleware
def middleware_chain(handlers: list):
    """Build a middleware pipeline where each handler wraps the next."""
    def chain(request):
        def run(index=0):
            if index < len(handlers):
                return handlers[index](request, lambda: run(index + 1))
            return request
        return run()
    return chain


order = {
    "id": "ORD-42",
    "items": [
        {"name": "Laptop", "price": 1200, "qty": 1},
        {"name": "Mouse", "price": 25, "qty": 2},
    ],
}

result = step(order)
print(result)
print(result["summary"])


# Middleware demo
def auth(req, next):
    print(f"[Auth] Checking {req.get('user', 'anonymous')}")
    return next()


def logger(req, next):
    print(f"[Log] Request: {req.get('action', 'unknown')}")
    return next()


pipeline = middleware_chain([auth, logger])
pipeline({"user": "alice", "action": "purchase"})
```

## 🔍 How It Works
- `pipe(f, g, h)(x)` = `h(g(f(x)))` — reads left-to-right like Unix pipes
- `compose(f, g, h)(x)` = `f(g(h(x)))` — reads right-to-left like math
- Middleware chains wrap each layer around the next — each handler calls `next()` to proceed
- Function composition is the foundation of decorators, middleware, and data pipelines

## ⚠️ Common Pitfall
Composing functions with incompatible signatures. Each function's output type must match the next function's input type. Use dictionaries for flexible pipelines.

## 🧠 Memory Aid
**"Pipe = data flows, Compose = functions stack"**: Data flows left-to-right through pipes; functions nest inside-out in compose.

## 🏃 Try It
Write a processing pipeline: `clean(text)` → `tokenize(text)` → `count_words(tokens)` → `sort_by_freq(word_counts)`. Use `pipe()` to chain them together.

## 🔗 Related
- [Error Handling in Functions →](./09-error-handling-functions.md)
- [Decorators →](./07-decorators.md)

## ➡️ Next
Continue to [Phase 05: Modules & IO](../../05_modules_io/lessons/01-import-system.md)
