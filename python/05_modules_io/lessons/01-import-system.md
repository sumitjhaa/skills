# 📦 Import System
<!-- ⏱️ 10 min read | 🟢 Easy | 🧠 Core -->

**What You'll Learn:** How Python's import system works — module search paths, import styles, `__init__.py`, and `if __name__ == "__main__"`.

> 💡 **TL;DR — The whole point:** `import` finds, compiles, and runs a `.py` file once, then caches it so you can reuse code across files.

## 🔗 Why This Matters
You've been writing everything in one file. Real apps spread across many files — models, views, utilities, config. The import system is how you stitch them together.

## The Concept
Python's import system lets you use code from other files and libraries. A **module** is any `.py` file. A **package** is a directory of modules with an `__init__.py` file.

Python searches for modules in `sys.path` — the current directory, `PYTHONPATH`, and standard library paths. When you `import`, Python finds the file, compiles it to bytecode (`.pyc`), and executes it once. The result is cached in `sys.modules`.

## Code Example

```python
"""Package structure for real apps — app config and utils."""

import sys
from pathlib import Path


def show_search_paths():
    """Display the first few module search paths."""
    return sys.path[:5]


def discover_packages(root: str = ".") -> list:
    """Find all packages (dirs with __init__.py) in a directory."""
    base = Path(root)
    return [
        str(p.relative_to(base))
        for p in base.rglob("__init__.py")
    ]


# Simulate a package structure
if __name__ == "__main__":
    print("Search paths:", show_search_paths()[:3])
    print("__name__ is:", repr(__name__))
```

## 🔍 How It Works
- `import` finds the module, compiles it, executes it — result cached in `sys.modules`
- `from ... import` binds names into the current namespace
- `importlib.reload()` re-executes the module code
- `__init__.py` marks a directory as a package (can be empty)
- `if __name__ == "__main__":` lets a file be both importable and runnable

## ⚠️ Common Pitfall
Circular imports: module A imports B, B imports A. Python will crash with `ImportError`. Restructure to avoid cycles.

## 🧠 Memory Aid
**"Find, Compile, Run, Cache"**: The four steps of every import. Like a chef finding a recipe, reading it, cooking it, then keeping it warm for reuse.

## 🏃 Try It
Create a directory `my_app/` with an empty `__init__.py` and a file `utils.py` containing a function `greet(name)`. Import and call it from a script in the parent directory.

## 🔗 Related
- [Math & Random →](./02-math-random.md)

## ➡️ Next
[Math & Random](./02-math-random.md)
