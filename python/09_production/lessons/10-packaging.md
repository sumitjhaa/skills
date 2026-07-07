# 🎯 Packaging & Distribution
<!-- ⏱️ 14 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Package your code with `pyproject.toml`, build distributable packages, and publish to PyPI with `flit` or `pdm`.

> 💡 **TL;DR — The whole point:** Packaging turns your code into something others can `pip install`. A `pyproject.toml` file defines your package metadata, dependencies, and build system.

## 🔗 Why This Matters
If you've ever wanted to share a library, contribute to open source, or deploy a reusable tool, you need to package it. `pyproject.toml` is the modern Python standard.

## The Concept
- `pyproject.toml` — the single source of truth for Python projects
- Build backends: `setuptools`, `flit_core`, `pdm-backend`, `hatchling`
- `pip install -e .` — editable install (symlinks your source)
- `python -m build` — creates `.tar.gz` (source) and `.whl` (wheel)
- Publishing: `twine upload dist/*` to PyPI

## Code Example
```python
"""
ecommerce_tools/ package on PyPI.

pyproject.toml:
    [build-system]
    requires = ["hatchling"]
    build-backend = "hatchling.build"

    [project]
    name = "ecommerce-tools"
    version = "0.1.0"
    description = "E-commerce utility functions"
    requires-python = ">=3.10"
    dependencies = ["httpx>=0.27"]

    [project.scripts]
    ecom-calc = "ecommerce_tools.cli:main"

Structure:
    ecommerce_tools/
        __init__.py
        pricing.py
        validation.py
        cli.py
"""

# ecommerce_tools/__init__.py
from .pricing import calculate_total, apply_discount
from .validation import validate_order, validate_sku

__all__ = ["calculate_total", "apply_discount", "validate_order", "validate_sku"]
__version__ = "0.1.0"
```

```python
"""ecommerce_tools/pricing.py — Core pricing functions."""

from typing import Optional


TAX_RATE = 0.08


def calculate_total(subtotal: float, discount: Optional[float] = None) -> float:
    if discount:
        subtotal *= 1 - discount
    return round(subtotal * (1 + TAX_RATE), 2)


def apply_discount(price: float, percent: float) -> float:
    if not 0 <= percent <= 100:
        raise ValueError("Percent must be 0-100")
    return round(price * (1 - percent / 100), 2)
```

```python
"""ecommerce_tools/validation.py — Order and SKU validation."""

import re

SKU_PATTERN = re.compile(r"^[A-Z]{3,4}-\d{3}$")


def validate_sku(sku: str) -> bool:
    return bool(SKU_PATTERN.match(sku))


def validate_order(items: list[tuple[str, int]]) -> tuple[bool, str]:
    if not items:
        return False, "Order must have at least one item"
    total_qty = sum(qty for _, qty in items)
    if total_qty > 100:
        return False, "Order exceeds maximum quantity of 100"
    return True, "OK"
```

```python
"""ecommerce_tools/cli.py — CLI entry point."""

import argparse
from .pricing import calculate_total


def main() -> None:
    parser = argparse.ArgumentParser(description="E-commerce calculator")
    parser.add_argument("subtotal", type=float)
    parser.add_argument("--discount", type=float, default=None)
    args = parser.parse_args()
    total = calculate_total(args.subtotal, args.discount)
    print(f"Total: ${total:.2f}")
```

## 🔍 How It Works
- `pyproject.toml` replaces `setup.py`, `setup.cfg`, `MANIFEST.in`
- `[project.scripts]` defines console entry points (CLI commands)
- `pip install -e .` installs in development mode (editable)
- `build` creates source dist (`.tar.gz`) and wheel (`.whl`)
- `twine upload dist/*` publishes to PyPI (or TestPyPI)
- Dependencies are installed automatically when users `pip install`

## ⚠️ Common Pitfall
Forgetting to increment the version before publishing. PyPI doesn't allow overwriting a published version. Use `__version__` in `__init__.py` and keep it in sync with `pyproject.toml`.

## 🧠 Memory Aid
"Packaging = `pyproject.toml` + `pip install -e .` + `build` + `twine upload`. pyproject.toml is 'I want to share this.'"

## 🏃 Try It
Create a minimal package with `pyproject.toml`, one module with a `hello()` function, and a CLI entry point. Install it with `pip install -e .` and run the command.

## 🔗 Related
- [Project Structure](01-project-structure.md) — src layout for packages
- [Docker for Python](11-docker-python.md) — packaging complete apps

## ➡️ Next
[Docker for Python](11-docker-python.md)
