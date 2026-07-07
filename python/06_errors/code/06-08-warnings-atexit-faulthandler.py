"""warnings, atexit, and faulthandler — cleanup handlers and crash debugging."""
import warnings
import atexit
import faulthandler
import os
from pathlib import Path


def old_api_function():
    warnings.warn("old_api_function is deprecated, use new_api_function instead", DeprecationWarning, stacklevel=2)
    return "old result"


def new_api_function():
    return "new result"


@atexit.register
def cleanup_temp_files():
    temp_file = "/tmp/atexit_cleanup_test.txt"
    if os.path.exists(temp_file):
        os.remove(temp_file)
        print(f"[ATEXIT] Cleaned up {temp_file}")


@atexit.register
def say_goodbye():
    print("[ATEXIT] Application shutting down gracefully")


def read_config_deprecated(path: str) -> str:
    warnings.warn("read_config_deprecated is deprecated, use read_config instead", DeprecationWarning, stacklevel=2)
    return f"Config from {path}"


faulthandler.enable()
warnings.filterwarnings("once", category=DeprecationWarning)

result = old_api_function()
print(f"Result: {result}")
result2 = old_api_function()
print(f"Second call (no warning): {result2}")

cfg = read_config_deprecated("/tmp/config.txt")
Path("/tmp/atexit_cleanup_test.txt").write_text("clean me up")
print("Created temp file — atexit will clean it")
print("Program ending — handlers will fire now")
