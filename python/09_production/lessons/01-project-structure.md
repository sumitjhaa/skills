# 🎯 Project Structure
<!-- ⏱️ 12 min read | 🟢 Core | 🧠 Applied -->

**What You'll Learn:** Organize Python projects using the src layout, packages with `__init__.py`, absolute vs relative imports, and the `__name__ == "__main__"` guard.

> 💡 **TL;DR — The whole point:** A well-structured project is easy to navigate, test, and distribute — the src layout is the industry standard.

## 🔗 Why This Matters
Every production project needs organization. Without structure, you get import errors, circular dependencies, and `sys.path` hacks. Good structure prevents these from day one.

## The Concept
**Flat layout:** modules at the top level. **Src layout:** code under `src/` or a package directory. The src layout is preferred for distributable packages.

## Code Example
```python
"""
project/
├── src/
│   └── my_app/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/
├── pyproject.toml
└── requirements.txt
"""

# src/my_app/__init__.py
from .core import process_data
from .utils import format_result

__all__ = ["process_data", "format_result"]

# src/my_app/core.py
from .utils import validate_input


def process_data(data: list[float]) -> float:
    if not validate_input(data):
        raise ValueError("Invalid data")
    return sum(data) / len(data)


# src/my_app/utils.py
def validate_input(data: list[float]) -> bool:
    return len(data) > 0 and all(isinstance(x, (int, float)) for x in data)


def format_result(value: float) -> str:
    return f"Result: {value:.2f}"


# tests/test_core.py
from my_app import process_data


def test_process_data():
    assert process_data([1, 2, 3]) == 2.0
    assert process_data([10.0]) == 10.0
```

## 🔍 How It Works
- `__init__.py` marks a directory as a package
- `__all__` controls what `from package import *` exports
- **Absolute imports:** `from my_app.core import process_data`
- **Relative imports:** `from .utils import validate_input` (inside a package)
- `if __name__ == "__main__":` prevents code from running when imported
- `pyproject.toml` is the modern standard for package metadata

## ⚠️ Common Pitfall
Running scripts from inside the package directory causes import confusion. Always run from the project root, or use `python -m my_app.module`.

## 🧠 Memory Aid
"`__init__` = 'this directory is a package.' `__all__` = 'this is my public API.' `__name__ == '__main__'` = 'I'm being run directly.'"

## 🏃 Try It
Create a `src/calculator/` package with `__init__.py`, `operations.py`, and `validators.py`. Write a test file. Run it from the project root with `python -m pytest`.

## 🔗 Related
- [Virtual Environments](08-virtual-envs.md) — isolating project dependencies
- [Packaging & Distribution](10-packaging.md) — publishing your package

## ➡️ Next
[PEP 8 & Code Style](02-pep8-style.md)
