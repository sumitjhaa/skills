# ⚠️ Warnings, AtExit & FaultHandler
<!-- ⏱️ 8 min read | 🔴 Hard | 🧠 Mastery -->

**What You'll Learn:** How to issue warnings, register cleanup handlers, and debug crashes with faulthandler.

> 💡 **TL;DR — The whole point:** `warnings` for non-fatal alerts, `atexit` for guaranteed cleanup, `faulthandler` for crash forensics.

## 🔗 Why This Matters
ExceptionGroup handles multiple errors. But some issues aren't errors — they're deprecation warnings or cleanup tasks. `warnings` warns users, `atexit` runs cleanup on shutdown, `faulthandler` dumps tracebacks on crashes.

## The Concept
Three modules for three edge cases:
- **warnings** — soft alerts (deprecated functions, config changes)
- **atexit** — register cleanup functions that run at normal interpreter exit
- **faulthandler** — dump Python tracebacks on segfaults or crashes (debugging)

These are your safety nets: warnings tell users something is off, atexit ensures cleanup, faulthandler helps debug the worst crashes.

## Code Example

```python
"""warnings, atexit, and faulthandler — cleanup handlers and crash debugging."""

import warnings
import atexit
import faulthandler
import os


def old_api_function():
    """Old function that still works but emits a deprecation warning."""
    warnings.warn("old_api_function is deprecated, use new_api_function instead", DeprecationWarning, stacklevel=2)
    return "old result"


def new_api_function():
    return "new result"


@atexit.register
def cleanup_temp_files():
    """Cleanup handler — runs at normal interpreter exit."""
    temp_file = "/tmp/atexit_cleanup_test.txt"
    if os.path.exists(temp_file):
        os.remove(temp_file)
        print(f"[ATEXIT] Cleaned up {temp_file}")


@atexit.register
def say_goodbye():
    print("[ATEXIT] Application shutting down gracefully")


# Enable faulthandler — dumps tracebacks on crash
faulthandler.enable()


# Demo: warnings
warnings.filterwarnings("once", category=DeprecationWarning)
result = old_api_function()
print(f"Function returned: {result}")

# Trigger it again — won't warn twice due to "once" filter
result2 = old_api_function()

# atexit demo — create a temp file that cleanup_temp_files will remove
Path("/tmp/atexit_cleanup_test.txt").write_text("clean me up")
print("Created temp file for atexit cleanup")

print("Program ending — atexit handlers will fire now")
```

## 🔍 How It Works
- `warnings.warn("msg", Category)` issues a warning — user sees it but code continues
- `warnings.filterwarnings("once")` shows each warning only once
- `atexit.register(func)` registers a function to call at normal interpreter exit
- `faulthandler.enable()` installs a signal handler that dumps tracebacks on crash
- Warnings go to `stderr` by default; can be redirected to logging

## ⚠️ Common Pitfall
Treating warnings as errors. Warnings are informational — the code still runs. If you want to halt on warnings, use `warnings.filterwarnings("error")`.

## 🧠 Memory Aid
**"warn = soft alert, atexit = final farewell, faulthandler = crash detective"**: Three tools for three stages — before (warn), at end (atexit), on crash (faulthandler).

## 🏃 Try It
Write a function `read_config_deprecated(path)` that emits a `DeprecationWarning`. Register an atexit handler that logs "Config read complete". Test both success and error scenarios.

## 🔗 Related
- [ExceptionGroup →](./07-exceptiongroup.md)
- [Logging →](./06-logging.md)

## ➡️ Next
This is the last lesson in Phase 06. Try the [integration project](../code/integration-mission-impossible.py) to practice everything together!
