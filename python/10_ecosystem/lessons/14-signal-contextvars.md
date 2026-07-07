# 📡 Signal, AtExit, FaultHandler & ContextVars — OS & Async Context
<!-- ⏱️ 20 min read | 🔴 Mastery | 🧠 Applied -->

**What You'll Learn:** `signal` for OS-level handlers, `atexit` for cleanup, `faulthandler` for crash debugging, and `contextvars` for async-safe request-scoped context.

> 💡 **TL;DR — The whole point:** `signal` lets Python respond to OS signals (SIGTERM → graceful shutdown). `atexit` registers cleanup functions. `faulthandler` dumps tracebacks on crashes. `contextvars` provides per-coroutine context (like thread-local storage for async) — essential for request IDs, user IDs, and tracing in async web apps.

## 🔗 Why This Matters
Production services must handle graceful shutdowns (SIGTERM), crash dumps (SIGSEGV), timeouts (SIGALRM), and per-request tracing (contextvars) without leaking state between concurrent requests.

## The Concept

| Module | Job |
|--------|-----|
| `signal` | handle OS signals (SIGTERM, SIGINT, SIGUSR1, SIGALRM) |
| `atexit` | register/unregister cleanup functions |
| `faulthandler` | enable traceback dumps on crash |
| `contextvars` | per-coroutine/thread context (immutable, fast) |

## Code Example

```python
"""Graceful shutdown, SIGALRM timeout, fault handler, and request tracing."""
import signal
import atexit
import faulthandler
import contextvars
import time
import sys
import asyncio
from typing import Any

faulthandler.enable()  # dump traceback on crash

# ── Graceful shutdown with signal ──
shutdown_requested = False

def handle_sigterm(signum: int, frame: Any) -> None:
    global shutdown_requested
    shutdown_requested = True
    print(f"\nSIGTERM received, shutting down gracefully...")

signal.signal(signal.SIGTERM, handle_sigterm)

# ── atexit cleanup ──
@atexit.register
def cleanup() -> None:
    print("Cleanup: closing database connections...")

# ── ContextVar for request tracing ──
request_id: contextvars.ContextVar[str] = contextvars.ContextVar("request_id")
user_id: contextvars.ContextVar[int] = contextvars.ContextVar("user_id", default=0)

async def handle_request(rid: str, uid: int) -> None:
    request_id.set(rid)
    user_id.set(uid)
    await asyncio.sleep(0.1)
    print(f"  Processing {request_id.get()} for user {user_id.get()}")

async def main() -> None:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(handle_request("req-1", 42))
        tg.create_task(handle_request("req-2", 99))
    print(f"Contexts are isolated: {request_id.get('not-set')}")

    # SIGALRM timeout example
    def timeout_handler(signum: int, frame: Any) -> None:
        raise TimeoutError("Operation timed out")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(1)
    try:
        time.sleep(5)
    except TimeoutError:
        print("SIGALRM: operation timed out after 1s")
    signal.alarm(0)  # disable alarm

asyncio.run(main())
```

## 🔍 How It Works
- `signal.signal(signum, handler)` — registers a handler for a signal; handler receives `(signum, frame)`
- `signal.alarm(sec)` — sends SIGALRM after `sec` seconds; `signal.alarm(0)` cancels
- `signal.pause()` — blocks until a signal arrives; `signal.set_wakeup_fd(fd)` writes a byte to `fd` on signal
- Common signals: `SIGTERM` (kill), `SIGINT` (Ctrl+C), `SIGUSR1`/`SIGUSR2` (user-defined), `SIGALRM` (timer)
- `atexit.register(fn)` — registers `fn()` to run at exit (LIFO order); `atexit.unregister(fn)` to remove
- `faulthandler.enable()` — installs a handler that dumps a Python traceback on `SIGSEGV`, `SIGABRT`, etc.
- `contextvars.ContextVar("name", default=x)` — defines a variable; `.set(value)` returns a `Token`; `.get()` reads; `contextvars.copy_context()` captures current context; `.run(fn)` executes in that context

## ⚠️ Common Pitfall
**Signal handlers must be simple.** `signal` handlers run in the main thread with limited C stack — most functions (including `print()`, `time.sleep()`) are unsafe. Use a flag + poll, or `signal.set_wakeup_fd()` with `asyncio`'s loop.add_reader.

**Fork + signals:** After `os.fork()`, signal handlers are inherited. In `spawn`-based multiprocessing, child processes have default handlers.

**contextvars vs threading.local:** `contextvars` works across `asyncio` tasks AND threads. `threading.local()` only works per-thread and leaks state across async tasks running on the same thread.

## 🧠 Memory Aid
"Signal = OS interrupts the process (SIGTERM=stop, SIGALRM=alarm clock). Atexit = 'clean up before exit' (LIFO). Faulthandler = 'print stack on crash.' ContextVar = 'request local for async' (immutable, fast, never leaks)."

## 🏃 Try It
Add `contextvars` to store `user_id` and `role` in a mock async web app. Write middleware that sets the context, and a handler that checks `role == 'admin'` before returning data.

## 🔗 Related
- [Socket Networking](13-socket-networking.md) — low-level networking
- [Asyncio Primitives Deep](12-asyncio-primitives-deep.md) — async patterns
- [Deployment & Monitoring](09-deployment-monitoring.md) — production concerns

## ➡️ Next
You've completed Phase 10! 🎉 Practice what you've learned with the [exercises](../practice/exercises.md).
