# 🔁 Recursion
<!-- ⏱️ 10 min read | 🟡 Medium | 🧠 Applied -->

**What You'll Learn:** How a function can call itself to solve problems that have repeated sub-structure.

> 💡 **TL;DR — The whole point:** Recursion breaks a big problem into smaller copies of itself until it hits a trivial base case.

## 🔗 Why This Matters
Flat lists are easy with loops, but what about directory trees, nested menus, or tournament brackets? Recursion handles problems of *any* depth with the same logic.

## The Concept
Every recursive function has two parts:
- **Base case**: the simplest version that returns immediately
- **Recursive case**: calls itself with a smaller/narrower input

Think of recursion like Russian nesting dolls — to count the dolls, you open the outer one, then count what's inside (which is the same problem, just smaller).

## Code Example

```python
"""Directory tree traversal and cricket tournament permutations."""

from functools import lru_cache


def tree_depth(directories: dict, path: str = "/") -> list:
    """Recursively list all paths in a directory tree."""
    paths = [path]
    for name, contents in directories.get(path, {}).items():
        paths.extend(tree_depth(contents, f"{path}{name}/"))
    return paths


def factorial(n: int) -> int:
    """n! — permutations of n items."""
    if n <= 1:          # base case
        return 1
    return n * factorial(n - 1)   # recursive case


@lru_cache(maxsize=None)
def cricket_permutations(players: int) -> int:
    """Number of ways to arrange batting order (memoized)."""
    if players <= 1:
        return 1
    return players * cricket_permutations(players - 1)


file_system = {
    "/": {
        "home": {"/home": {"/home/user": {"/home/user/docs": {}, "/home/user/pics": {}}}},
        "var": {"/var": {"/var/log": {}}},
    }
}

print(tree_depth(file_system))        # ['/', '/home/', '/home/user/', ...]
print(factorial(5))                   # 120
print(cricket_permutations(11))       # 39916800 (11 batting order permutations)
```

## 🔍 How It Works
- Every recursive call pushes a new frame onto the call stack
- Python limits recursion depth (default ~1000) to prevent stack overflow
- **Memoization** (`@lru_cache`) caches results — transforms O(2ⁿ) to O(n)
- Iteration is usually faster, but recursion is more natural for trees, graphs, and divide-and-conquer

## ⚠️ Common Pitfall
Forgetting the base case → infinite recursion → `RecursionError`. Always write the base case *first*, then the recursive case.

## 🧠 Memory Aid
**"Base then bounce"**: Write the stop condition (base case) first, then the self-call (recursive case). Handle the smallest input first.

## 🏃 Try It
Write a recursive `list_files(path: dict, prefix="")` that prints all "files" (leaf paths) in a nested dict. Given `{"a": {"b": {}, "c": {"d": {}}}}`, it should print `a/b`, `a/c/d`.

## 🔗 Related
- [Lambda & Higher-Order Functions →](./04-lambda-hof.md)
- [Generators →](./06-generators.md)

## ➡️ Next
[Generators](./06-generators.md)
