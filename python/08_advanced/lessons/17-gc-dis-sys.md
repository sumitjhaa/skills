# 🎯 gc, dis, sys deep — Python Internals
<!-- ⏱️ 16 min read | 🔴 Mastery | 🧠 Mastery -->

**What You'll Learn:** Debug memory cycles with `gc`, read CPython bytecode with `dis`, and inspect runtime state with `sys` deep dives.

> 💡 **TL;DR — The whole point:** `gc` finds and breaks circular references, `dis` shows you what CPython actually executes, and `sys` gives access to reference counts, frame objects, audit hooks, and the interpreter internals.

## 🔗 Why This Matters
Memory leaks in long-running servers, understanding why list comprehensions are faster than loops, security audit hooks, and debugging "why is this object still alive?" — these tools are essential for production Python.

## The Concept
- `gc` — generational garbage collector. `gc.collect()` triggers a collection. `gc.get_objects()` lists all tracked objects. `gc.get_referrers(obj)` finds who holds a reference. `gc.freeze()` moves objects to the oldest generation (speeds up collection in long-running processes)
- `dis` — disassembler. `dis.dis(func)` prints CPython bytecode. `LOAD_FAST` loads a local variable, `CALL_FUNCTION` calls a function. Understanding bytecode explains performance differences
- `sys` deep — `getrefcount()` returns reference count (always ≥1 because of the arg itself). `_getframe()` returns the current frame. `settrace()` sets a per-thread trace function. `audit()` raises audit events for security hooks

## Code Example
```python
"""Find circular references, compare loop vs comprehension bytecode, trace calls."""

import gc, dis, sys


# ─── gc: Find circular references ───
class Node:
    def __init__(self):
        self.ref = None

a, b = Node(), Node()
a.ref, b.ref = b, a     # circular
gc.collect()
nodes = [o for o in gc.get_objects() if isinstance(o, Node)]
print(f"Circular refs tracked: {len(nodes)}")

# ─── dis: Why comprehension is faster ───
def with_loop(n):
    r = []
    for i in range(n):
        r.append(i * 2)
    return r

def with_comp(n):
    return [i * 2 for i in range(n)]

dis.dis(with_loop)
dis.dis(with_comp)
# Note: comprehension has fewer LOAD_FAST + CALL_FUNCTION bytecode steps

# ─── sys: Trace function calls ───
def tracer(frame, event, arg):
    if event == "call":
        print(f"  -> {frame.f_code.co_name}")
    return tracer

sys.settrace(tracer)
result = sum([1, 2, 3])
sys.settrace(None)
print(f"Sum traced: {result}")
```

## 🔍 How It Works
- CPython uses reference counting (fast, deterministic) + generational GC (catches cycles). Gen 0 (young, collected often), Gen 1, Gen 2 (old, collected rarely). `gc.set_threshold(700, 10, 10)` tunes collection frequency
- `dis` output: column 1 = line number, column 2 = byte address, column 3 = opcode name, column 4 = argument (variable name or constant). `LOAD_CONST 0` loads constant at index 0. `CALL_FUNCTION n` calls with n args
- `sys.getsizeof` returns the shallow size of an object. `sys.getrefcount` includes the temporary reference from the function argument. `sys._getframe().f_back` walks up the call stack

## ⚠️ Common Pitfall
`gc.get_objects()` returns ALL tracked objects (thousands in a typical process). Always filter by type or use `gc.get_referrers(obj)` to find specific leaks. `sys.getrefcount()` returns 1 more than you expect (the arg itself creates a reference).

## 🧠 Memory Aid
"`gc` = cycle breaker. `dis` = Python's decompiler. `sys` deep = getrefcount, getframe, settrace. `gc.freeze()` = 'these objects are permanent, stop scanning them'. Bytecode: LOAD_FAST = local var, STORE_FAST = assign."

## 🏃 Try It
Write a function that uses `gc.get_referrers` to find what's holding a reference to an object that should have been garbage collected. Use `sys._getframe()` to print the current call stack in a decorator.

## 🔗 Related
- [Weakref & ContextVars](13-weakref-contextvars.md) — weak references avoid cycles
- [Advanced importlib & inspect](14-advanced-importlib-inspect.md) — frame inspection

## ➡️ Next
[collections.abc & __match_args__](18-collections-abc-match-args.md)
