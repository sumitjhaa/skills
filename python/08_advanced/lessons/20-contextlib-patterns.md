# 🎯 contextlib Patterns: ExitStack, suppress, nullcontext, @contextmanager
<!-- ⏱️ 14 min | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Use `ExitStack`, `suppress`, `nullcontext`, and `@contextmanager` for production resource management.

> 💡 **TL;DR — The whole point:** `contextlib` gives you advanced context manager tools — dynamically manage N resources, suppress expected errors, use no-op placeholders, and time blocks with `@contextmanager`.

## 🔗 Why This Matters
Database transactions need rollback on error, file cleanup must happen even if some opens fail, and you often need to capture stdout or time an operation. These patterns are day-to-day tools for any Python developer.

## The Concept
`ExitStack` lets you enter multiple context managers dynamically (all cleaned up on exception). `suppress` swallows specific exceptions. `nullcontext` is a no-op placeholder for optional resources. `@contextmanager` turns a generator into a context manager with try/finally for guaranteed cleanup.

## Code Example
```python
"""contextlib patterns: timing, transactions, output capture — real dev tools"""
from contextlib import contextmanager, ExitStack, suppress, redirect_stdout, nullcontext
import time, io, os, tempfile

# @contextmanager: timer with try/finally (always runs cleanup)
@contextmanager
def timed(operation_name: str):
    print(f"  Starting {operation_name}...")
    start = time.perf_counter()
    try:
        yield  # Context body runs here
    finally:
        elapsed = time.perf_counter() - start  # Runs even if exception raised
        print(f"  {operation_name} took {elapsed:.3f}s")

# ExitStack: open N files — ALL auto-closed, even if one open() fails
def read_logs(filenames: list[str]):
    with ExitStack() as stack:
        files = [stack.enter_context(open(f)) for f in filenames]
        return [f.read() for f in files]

# suppress: ignore expected errors without try/except boilerplate
def safe_delete(path: str):
    with suppress(FileNotFoundError, PermissionError):
        os.remove(path)
        print(f"  Deleted {path}")

# redirect_stdout: capture print() output to a string
buf = io.StringIO()
with redirect_stdout(buf):
    print("This goes to buffer, not console")
output = buf.getvalue()

# Usage demo
with timed("API call"):
    time.sleep(0.01)
with suppress(ValueError):
    int("not_a_number")  # Silently ignored, no traceback
with nullcontext("fallback"):  # No-op, useful for optional DB vs no-DB paths
    pass
tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
tmp.write(b"hello\n"); tmp.close()
safe_delete(tmp.name)
print(f"  Captured: {repr(output.strip())}")
```

## 🔍 How It Works
- `ExitStack.enter_context()` adds a manager to the stack — all are exited (cleaned up) when the `with` block exits, even if an exception occurs mid-way
- `suppress(ExcType)` catches the specified exception and continues — no `try/except` boilerplate
- `nullcontext(value)` returns the value and does nothing on enter/exit — use it as a placeholder where you'd normally use a real context manager
- `@contextmanager` wraps a generator; everything before `yield` is `__enter__`, everything after is `__exit__`

## ⚠️ Common Pitfall
Forgetting `try/finally` inside `@contextmanager`. If the yield is inside a `try` without a `finally`, an exception in the context body will skip cleanup code. Always use `try: yield finally: cleanup`.

## 🧠 Memory Aid
"ExitStack = 'open N things, close them all on exit.' suppress = 'shh, I know it might fail.' @contextmanager = 'yield = the boundary between setup and teardown.'"

## 🏃 Try It
Write a `@contextmanager` that acquires a `threading.Lock` on enter and releases it on exit. Then use `ExitStack` to acquire 3 locks in one block.

## 🔗 Related
- [Context Managers Deep](06-context-managers-deep.md) — class-based context managers

## ➡️ Next
[Functools Patterns](21-functools-patterns.md)
