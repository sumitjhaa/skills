"""Package structure for real apps — app config and utils."""
import sys
from pathlib import Path


def show_search_paths() -> list:
    return sys.path[:5]


def discover_packages(root: str = ".") -> list:
    base = Path(root)
    return [str(p.relative_to(base)) for p in base.rglob("__init__.py")]


print("Search paths:", show_search_paths()[:3])
print("__name__:", repr(__name__))

if __name__ == "__main__":
    print("Script executed directly")
