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
