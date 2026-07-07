"""08-17-gc-dis-sys.py — Circular reference detection, bytecode disassembly, tracing."""

import gc
import dis
import sys


def find_circular_refs():
    class Node:
        def __init__(self):
            self.ref = None

    a, b = Node(), Node()
    a.ref, b.ref = b, a
    gc.collect()
    refs = [obj for obj in gc.get_objects() if isinstance(obj, Node)]
    print(f"Node instances tracked: {len(refs)}")
    return refs


def disassemble_comprehension():
    def with_loop(n):
        result = []
        for i in range(n):
            result.append(i * 2)
        return result

    def with_comp(n):
        return [i * 2 for i in range(n)]

    print("\n--- Loop bytecode ---")
    dis.dis(with_loop)
    print("\n--- Comprehension bytecode ---")
    dis.dis(with_comp)


def trace_calls():
    def tracer(frame, event, arg):
        if event == "call":
            print(f"  -> calling {frame.f_code.co_name}")
        return tracer

    def inner():
        return 42

    sys.settrace(tracer)
    result = inner()
    sys.settrace(None)
    print(f"Traced call returned {result}")


if __name__ == "__main__":
    find_circular_refs()
    disassemble_comprehension()
    trace_calls()
