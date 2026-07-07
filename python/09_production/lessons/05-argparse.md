# 🎯 Argparse
<!-- ⏱️ 12 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Build professional CLI tools with `argparse` — positional args, optional flags, subcommands, type validation, and help text.

> 💡 **TL;DR — The whole point:** `argparse` turns a Python script into a real CLI tool with `--help`, type checking, and subcommands.

## 🔗 Why This Matters
Any script that runs in production needs command-line arguments. `argparse` is in the standard library — no dependencies needed. It powers tools like `pytest`, `black`, and `uvicorn`.

## The Concept
- `ArgumentParser` — the CLI definition
- `add_argument()` — define positional, optional, and flag arguments
- `parse_args()` — parse from `sys.argv` (or a list for testing)
- Subcommands via `add_subparsers()` — like `git commit`, `git push`

## Code Example
```python
"""E-commerce: CLI tool for managing product inventory."""

import argparse
import json
from pathlib import Path
from typing import Any


DB_PATH = Path("inventory.json")


def load_inventory() -> list[dict[str, Any]]:
    if DB_PATH.exists():
        return json.loads(DB_PATH.read_text())
    return []


def save_inventory(inv: list[dict[str, Any]]) -> None:
    DB_PATH.write_text(json.dumps(inv, indent=2))


def cmd_add(args: argparse.Namespace) -> None:
    inv = load_inventory()
    if any(p["sku"] == args.sku for p in inv):
        print(f"Error: SKU {args.sku} already exists")
        return
    inv.append({"sku": args.sku, "name": args.name, "price": args.price, "qty": args.qty})
    save_inventory(inv)
    print(f"Added {args.name} (SKU: {args.sku})")


def cmd_list(args: argparse.Namespace) -> None:
    inv = load_inventory()
    if not inv:
        print("No products in inventory")
        return
    print(f"{'SKU':12s} {'Name':20s} {'Price':8s} {'Qty':4s}")
    print("-" * 44)
    for p in inv:
        print(f"{p['sku']:12s} {p['name']:20s} ${p['price']:<5.2f} {p['qty']:<4d}")


def cmd_search(args: argparse.Namespace) -> None:
    inv = load_inventory()
    query = args.query.lower()
    results = [p for p in inv if query in p["name"].lower()]
    if not results:
        print(f"No products matching '{args.query}'")
        return
    for p in results:
        print(f"  {p['sku']}: {p['name']} — ${p['price']:.2f} ({p['qty']} in stock)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Product Inventory CLI")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    add_p = subparsers.add_parser("add", help="Add a new product")
    add_p.add_argument("sku", help="Product SKU (e.g., LAP-001)")
    add_p.add_argument("name", help="Product name")
    add_p.add_argument("price", type=float, help="Product price")
    add_p.add_argument("--qty", type=int, default=1, help="Initial quantity")

    subparsers.add_parser("list", help="List all products")

    search_p = subparsers.add_parser("search", help="Search products by name")
    search_p.add_argument("query", help="Search query")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    commands = {"add": cmd_add, "list": cmd_list, "search": cmd_search}

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

## 🔍 How It Works
- `add_argument("sku")` — positional argument (required)
- `add_argument("--price", type=float)` — optional argument with type conversion
- `add_argument("--verbose", action="store_true")` — boolean flag
- `add_argument("--qty", type=int, default=1)` — optional with default
- `subparsers` creates subcommands like `add`, `list`, `search`
- `parse_args()` returns a `Namespace` object with all arguments as attributes

## ⚠️ Common Pitfall
Positional arguments are required by default. If you forget one, argparse shows a helpful error message — but if your logic accidentally ignores it, the bug is silent. Validate all args in your command handlers.

## 🧠 Memory Aid
"Argparse = `parser.add_argument()` + `parser.parse_args()`. Positional = required. `--flag` = optional. `action='store_true'` = boolean flag."

## 🏃 Try It
Add a `delete` subcommand that takes a `sku` positional argument and removes the product from inventory. Also add a `--force` flag that skips the confirmation prompt.

## 🆚 Alternatives: `click` & `typer`

For non-trivial CLIs, many developers prefer third-party libraries over argparse:

| Feature | `argparse` | `click` | `typer` |
|---------|------------|---------|---------|
| Boilerplate | High (parser → args → handling) | Medium (decorators) | Low (type hints) |
| Auto help | Yes | Yes | Yes |
| Subcommands | Manual (`add_subparsers`) | `@click.group()` | `app.command()` |
| Type validation | Manual (`type=int`) | `type=int` | Automatic from hints |
| Nested groups | Manual | `@group.group()` | Auto |
| Dependencies | stdlib | `pip install click` | `pip install typer` |

```python
# click version (same inventory CLI, ~50% less code)
import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument("sku")
@click.argument("name")
@click.argument("price", type=float)
@click.option("--qty", default=1, type=int)
def add(sku, name, price, qty):
    click.echo(f"Added {qty} × {sku}")


@cli.command()
@click.argument("query")
def search(query):
    click.echo(f"Searching for {query}")


if __name__ == "__main__":
    cli()
```

Use `argparse` for simple scripts (no dependencies). Switch to `click` for multi-command CLIs. Use `typer` if you're already using type hints and want the least code.

## 🔗 Related
- [Logging Deep](06-logging-deep.md) — logging in CLI tools
- [Pydantic & Settings](13-pydantic-settings.md) — config validation
- [Virtual Environments](08-virtual-envs.md) — installing third-party CLI packages

## ➡️ Next
[Logging Deep](06-logging-deep.md)
