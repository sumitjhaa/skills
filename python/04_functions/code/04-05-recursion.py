"""Directory tree traversal and cricket tournament permutations."""
from functools import lru_cache


def tree_depth(directories: dict, path: str = "/") -> list:
    paths = [path]
    for name, contents in directories.get(path, {}).items():
        paths.extend(tree_depth(contents, f"{path}{name}/"))
    return paths


def factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial(n - 1)


@lru_cache(maxsize=None)
def cricket_permutations(players: int) -> int:
    if players <= 1:
        return 1
    return players * cricket_permutations(players - 1)


def list_files(tree: dict, prefix: str = "") -> list:
    result = []
    for name, subtree in tree.items():
        path = f"{prefix}{name}"
        if subtree:
            result.extend(list_files(subtree, f"{path}/"))
        else:
            result.append(path)
    return result


file_system = {"/": {"home": {"/home": {"/home/user": {"/home/user/docs": {}, "/home/user/pics": {}}}}}}
print(tree_depth(file_system))
print(factorial(5))
print(cricket_permutations(11))
print(list_files({"a": {"b": {}, "c": {"d": {}}}}))
