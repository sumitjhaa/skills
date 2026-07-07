# 🌳 Exception Hierarchy
<!-- ⏱️ 8 min read | 🟢 Easy | 🧠 Core -->

**What You'll Learn:** How Python's exception classes are organized, common built-in exceptions, and how to read tracebacks.

> 💡 **TL;DR — The whole point:** Exceptions form a family tree — catch the right ancestor to handle related errors together.

## 🔗 Why This Matters
Modules/IO gave you tools. Now learn what happens when tools break. The exception hierarchy helps you categorize errors: network errors, data errors, system errors — each with its own place in the tree.

## The Concept
Python exceptions form a hierarchy rooted at `BaseException`:
```
BaseException
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception
    ├── StopIteration
    ├── ArithmeticError → ZeroDivisionError
    ├── LookupError → IndexError, KeyError
    ├── ValueError
    ├── TypeError
    ├── OSError → FileNotFoundError
    └── RuntimeError → RecursionError
```
Catch `Exception` to catch most errors. Never catch `BaseException` directly.

## Code Example

```python
"""Network error handling and API error categorization."""


def call_api(endpoint: str) -> dict:
    """Simulate an API call that can fail in various ways."""
    import random
    error_type = random.choice(["network", "timeout", "auth", "rate_limit", None])

    if error_type == "network":
        raise ConnectionError(f"Cannot connect to {endpoint}")
    elif error_type == "timeout":
        raise TimeoutError(f"{endpoint} timed out")
    elif error_type == "auth":
        raise PermissionError(f"Authentication failed for {endpoint}")
    elif error_type == "rate_limit":
        raise RuntimeError("Rate limit exceeded — try again later")

    return {"status": 200, "data": {"endpoint": endpoint, "result": "ok"}}


def safe_api_call(endpoint: str) -> dict | None:
    """Call API and categorize the error."""
    try:
        return call_api(endpoint)
    except ConnectionError as e:
        print(f"[NETWORK] {e}")
    except TimeoutError as e:
        print(f"[TIMEOUT] {e}")
    except PermissionError as e:
        print(f"[AUTH] {e}")
    except RuntimeError as e:
        print(f"[SYSTEM] {e}")
    return None


result = safe_api_call("/users")
if result:
    print("API call succeeded:", result)
```

## 🔍 How It Works
- `except Exception` catches most errors (but not `SystemExit` or `KeyboardInterrupt`)
- `except LookupError` catches both `IndexError` and `KeyError`
- Read tracebacks bottom-to-top: last line = exception type + message
- `except:` (bare) catches everything including `KeyboardInterrupt` — avoid it

## ⚠️ Common Pitfall
Catching `BaseException` directly. This catches `SystemExit` and `KeyboardInterrupt`, making your program impossible to kill. Always catch `Exception` or a specific subclass.

## 🧠 Memory Aid
**"BaseException ← Exception ← YourError"**: Always inherit from `Exception` (or its subclasses). Never from `BaseException`.

## 🏃 Try It
Write a function `get_user_input()` that triggers `ValueError`, `TypeError`, or `KeyError` based on input. Catch each specifically and print a different message.

## 🔗 Related
- [Try/Except/Else/Finally →](./02-try-except.md)

## ➡️ Next
[Try / Except / Else / Finally](./02-try-except.md)
