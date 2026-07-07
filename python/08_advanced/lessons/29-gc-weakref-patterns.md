# 🎯 GC & Weakref Patterns: finalize, gc.collect, Observer Pattern
<!-- ⏱️ 15 min | 🔴 Advanced | 🧠 Applied -->

**What You'll Learn:** Use `weakref.ref` for observer patterns, `weakref.finalize` for reliable cleanup, and `gc.collect` for memory leak debugging.

> 💡 **TL;DR — The whole point:** `weakref` lets you reference objects without preventing garbage collection — perfect for observer patterns and caches; `weakref.finalize` is more reliable than `__del__`; `gc.collect()` manually runs the garbage collector to detect circular references.

## 🔗 Why This Matters
Memory leaks in long-running apps crash servers. Observer pattern subscribers that aren't properly cleaned up cause callback leaks. Database connections need guaranteed cleanup. These patterns prevent resource leaks.

## The Concept
`weakref.ref(callback)` holds a weak reference — calling `ref()` returns the object or `None` if collected. `weakref.finalize(obj, func)` schedules `func` to run when `obj` is garbage collected — more reliable than `__del__` because it works with circular references. `gc.collect()` forces a full garbage collection cycle and returns the number of collected objects (useful for debugging).

## Code Example
```python
"""GC & weakref: memory leak detection, observer pattern, auto-cleanup cache"""
import gc, weakref, sys

class EventBus:
    """Observer pattern: subscribers held as weak refs so they can be garbage collected"""
    def __init__(self):
        self._subscribers: list[weakref.ref] = []  # Weak refs — won't prevent GC

    def subscribe(self, callback):
        self._subscribers.append(weakref.ref(callback))  # No strong reference kept

    def emit(self, event: str):
        alive = []
        for ref in self._subscribers:
            cb = ref()  # Returns None if callback was garbage collected
            if cb is not None:
                cb(event)
                alive.append(ref)
        self._subscribers = alive  # Remove dead (collected) subscribers

def on_event(msg):
    """Callback — would be GC'd if bus didn't hold weak refs"""
    print(f"  Event: {msg}")

# --- Usage ---
bus = EventBus()
bus.subscribe(on_event)
bus.emit("user_login")  # Prints "Event: user_login"

# --- GC introspection (debugging memory leaks) ---
circular = {}  # Create circular reference
circular["self"] = circular  # obj points to itself — ref count never reaches 0
n = gc.collect()  # Force GC collection — returns number of collected objects
print(f"GC collected {n} unreachable objects")

# --- weakref.finalize: cleanup without __del__ (more reliable) ---
class DatabaseConnection:
    def close(self):
        print("  Connection closed")

db = DatabaseConnection()
weakref.finalize(db, db.close)  # Calls db.close() when db is garbage collected
del db  # Triggers finalize (more reliable than __del__)
```

## 🔍 How It Works
- `weakref.ref(obj)` returns a weak reference object — call `ref()` to get the object or `None` if collected
- `weakref.finalize(obj, func)` registers `func` to run on object destruction — works even with circular references where `__del__` fails
- `gc.collect()` returns the count of unreachable objects collected — use it to detect circular reference leaks
- The `EventBus` pattern iterates subscribers, calling `ref()` on each — `None` means that subscriber has been GC'd and is removed (self-cleaning)

## ⚠️ Common Pitfall
`weakref.ref` cannot be used with all objects — `list`, `dict`, `int`, `str`, `tuple`, and `None` (for most Python implementations) don't support weak references. You'll get `TypeError: cannot create weak reference to 'list' object`. Use a wrapper class or a `WeakSet`/`WeakValueDictionary` instead.

## 🧠 Memory Aid
"weakref = 'reference without keeping alive.' finalize = 'cleanup when object dies.' gc.collect = 'garbage day, force a cleanup.' circular = 'ref that points to itself = GC needed.'"

## 🏃 Try It
Create a `WeakValueDictionary` cache that maps user IDs to user objects. Show that when the last strong reference to a user is deleted, it automatically disappears from the cache.

## 🔗 Related
- [GC + dis + sys](17-gc-dis-sys.md) — `gc` module deep, `getrefcount`, `getsizeof`
- [Weakref + ContextVars](13-weakref-contextvars.md) — `WeakValueDictionary`, `WeakSet`

## ➡️ Next
[Mock & Patch Patterns](30-mock-patch-mock.md)
