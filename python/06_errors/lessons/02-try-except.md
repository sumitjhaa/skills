# 🎯 Try / Except / Else / Finally
<!-- ⏱️ 12 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** How to catch and handle exceptions using try/except blocks, the else and finally clauses, and EAFP vs LBYL.

> 💡 **TL;DR — The whole point:** `try` the risky code, `except` the error, `else` runs on success, `finally` always cleans up.

## 🔗 Why This Matters
The hierarchy showed you exception types. Now learn the pattern: `try` the dangerous operation, `except` the expected failure, `else` for the happy path, `finally` for guaranteed cleanup.

## The Concept
Think of try/except like a safety net:
- `try` — the tightrope (risky code)
- `except` — the net (catch errors)
- `else` — the applause (runs if no fall)
- `finally` — packing up (always runs)

Python prefers **EAFP** (Easier to Ask Forgiveness than Permission): try the operation, handle failure. Opposite is **LBYL** (Look Before You Leap): check conditions first.

## Code Example

```python
"""File operations and database transactions with robust error handling."""


def read_user_data(filepath: str) -> dict:
    """Read user data from a JSON file with full error handling."""
    result = {"status": "unknown", "data": None}

    try:
        with open(filepath, "r") as f:
            import json
            data = json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] File {filepath} not found")
        result["status"] = "not_found"
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON: {e}")
        result["status"] = "invalid_data"
    except PermissionError:
        print(f"[ERROR] Permission denied for {filepath}")
        result["status"] = "no_permission"
    else:
        # Runs only if no exception occurred
        print(f"[OK] Loaded {len(data)} records")
        result["status"] = "success"
        result["data"] = data
    finally:
        # Always runs — logging, cleanup
        print(f"[LOG] Read attempt for {filepath}: {result['status']}")

    return result


print(read_user_data("/tmp/nonexistent.json"))
print(read_user_data("/tmp/empty.json"))

# EAFP vs LBYL example
# LBYL: if os.path.exists(f) and f.readable(): open it
# EAFP: try: open it; except OSError: handle it

with open("/tmp/empty.json", "w") as f:
    f.write("not valid json")

print(read_user_data("/tmp/empty.json"))
```

## 🔍 How It Works
- Python walks `except` blocks in order — catches the first matching type
- `else` only runs when no exception occurred in `try`
- `finally` always runs (even with `return`, `break`, or unhandled exception)
- Catch specific exceptions — bare `except:` catches `KeyboardInterrupt` too

## ⚠️ Common Pitfall
Putting too much code in `try`. Only wrap the *specific* line that might raise. Too broad a `try` can hide bugs in unrelated code.

## 🧠 Memory Aid
**"Try the thing, Except the fail, Else the win, Finally the cleanup"**: Four clauses, four jobs. If you only need one, use `try`/`except`. If you need cleanup, add `finally`.

## 🏃 Try It
Write a function `safe_divide_list(values, divisor)` that tries to divide each value, catches `ZeroDivisionError` and `TypeError`, and returns a list of results with `None` for failed items.

## 🔗 Related
- [Exception Hierarchy →](./01-exception-hierarchy.md)
- [Raise & Assert →](./03-raise-assert.md)

## ➡️ Next
[Raise & Assert](./03-raise-assert.md)
