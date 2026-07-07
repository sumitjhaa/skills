# 👥 ExceptionGroup
<!-- ⏱️ 8 min read | 🔴 Hard | 🧠 Mastery -->

**What You'll Learn:** How to group multiple exceptions together and handle them with `except*` (Python 3.11+).

> 💡 **TL;DR — The whole point:** `ExceptionGroup` bundles multiple errors into one — like handling multiple API failures that all happened at once.

## 🔗 Why This Matters
Logging records individual errors. But sometimes multiple things fail simultaneously — you tried 5 API endpoints and 3 failed. `ExceptionGroup` lets you collect and handle all failures together.

## The Concept
`ExceptionGroup` is a collection of exceptions that are raised together. You catch them with `except*` (star) which matches any exception in the group that matches the specified type. Unmatched exceptions remain in the group.

Think of `except*` like a sieve: errors matching your filter are caught; everything else falls through.

## Code Example

```python
"""Error aggregation — multiple API calls that all can fail."""

import random


def check_service(service_name: str) -> str:
    """Simulate a health check that may fail."""
    roll = random.randint(1, 10)
    if roll <= 3:
        raise ConnectionError(f"{service_name} is unreachable")
    if roll <= 5:
        raise TimeoutError(f"{service_name} timed out")
    return f"{service_name} is healthy"


def check_all_services(services: list) -> list:
    """Check all services and collect failures into an ExceptionGroup."""
    results = []
    errors = []
    for service in services:
        try:
            results.append(check_service(service))
        except (ConnectionError, TimeoutError) as e:
            errors.append(e)

    if errors:
        raise ExceptionGroup("Multiple service failures", errors)
    return results


services = ["database", "cache", "auth", "api-gateway", "payment"]

try:
    random.seed(42)
    results = check_all_services(services)
    print("All services healthy:", results)
except* ConnectionError as e:
    print(f"[NETWORK] Connection errors: {len(e.exceptions)}")
    for exc in e.exceptions:
        print(f"  - {exc}")
except* TimeoutError as e:
    print(f"[TIMEOUT] Timeout errors: {len(e.exceptions)}")
    for exc in e.exceptions:
        print(f"  - {exc}")
```

## 🔍 How It Works
- `ExceptionGroup("message", [exc1, exc2, ...])` creates a group
- `except* ExceptionType` catches all exceptions of that type *within* the group
- Unmatched exceptions propagate up in a new ExceptionGroup
- Nested ExceptionGroups are supported
- Python 3.11+ only — check `sys.version_info` for compatibility

## ⚠️ Common Pitfall
Using `except` instead of `except*` with `ExceptionGroup`. Regular `except` catches the whole group as one object. Use `except*` to unpack and handle individual exceptions within.

## 🧠 Memory Aid
**"Group = batch, except* = sieve"**: ExceptionGroup batches multiple errors; `except*` sifts through them, catching only the type you specify.

## 🏃 Try It
Write a `validate_batch(data_list)` function that validates each item in a list and raises an `ExceptionGroup` containing all `ValueError`s found.

## 🔗 Related
- [Logging →](./06-logging.md)
- [Warnings, AtExit, FaultHandler →](./08-warnings-atexit-faulthandler.md)

## ➡️ Next
[Warnings, AtExit & FaultHandler](./08-warnings-atexit-faulthandler.md)
