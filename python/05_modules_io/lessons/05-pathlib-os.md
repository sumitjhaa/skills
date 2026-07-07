# 📁 Pathlib & OS
<!-- ⏱️ 10 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** Navigate and manipulate the filesystem using `pathlib` (modern) and `os` (traditional) modules.

> 💡 **TL;DR — The whole point:** `Path` objects make file path handling intuitive — no more string concatenation or cross-platform issues.

## 🔗 Why This Matters
File I/O opened files. But how do you find files, create directories, rename, or organize a file tree? Pathlib and OS give you filesystem superpowers — like a file organizer robot.

## The Concept
The `pathlib` module (Python 3.4+) provides an object-oriented approach to filesystem paths. `Path` objects overload the `/` operator for joining paths, work cross-platform (Windows vs Linux), and offer methods for all common operations.

Think of `Path` objects like a file explorer in code — you can navigate, inspect, create, rename, and delete files and directories.

## Code Example

```python
"""File organization tools — backup script and directory cleanup."""

from pathlib import Path
import shutil
from datetime import datetime


def organize_by_extension(directory: str) -> dict:
    """Group files in a directory by extension."""
    base = Path(directory)
    groups = {}
    for f in base.iterdir():
        if f.is_file():
            ext = f.suffix.lower() or "no_extension"
            groups.setdefault(ext, []).append(f.name)
    return groups


def backup_file(path: str, backup_dir: str = "/tmp/backups") -> Path:
    """Copy a file to a timestamped backup location."""
    src = Path(path)
    backup = Path(backup_dir)
    backup.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = backup / f"{src.stem}_{timestamp}{src.suffix}"
    shutil.copy2(src, dest)
    return dest


def clean_temp_files(directory: str, older_than_days: int = 7) -> list:
    """Remove temp files older than specified days."""
    base = Path(directory)
    removed = []
    for f in base.glob("*.tmp"):
        age = (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days
        if age > older_than_days:
            f.unlink()
            removed.append(f.name)
    return removed


# Demo
tmp = Path("/tmp/organize_demo")
(tmp / "sub").mkdir(parents=True, exist_ok=True)
(tmp / "doc.txt").write_text("hello")
(tmp / "data.csv").write_text("a,b,c")
(tmp / "script.py").write_text("print('hi')")

print("Groups:", organize_by_extension(tmp))
backup = backup_file(tmp / "doc.txt")
print(f"Backed up to: {backup}")
print(f"Backup exists: {backup.exists()}")

shutil.rmtree(tmp)
backup.unlink()
```

## 🔍 How It Works
- `Path` objects overload `/` for joining — `Path("a") / "b" / "c.txt"` works cross-platform
- `Path.read_text()` / `write_text()` are convenience wrappers around `open()`
- `glob("**/*.py")` matches recursively; `rglob("*.py")` does the same
- `shutil.copy2` preserves metadata; `shutil.rmtree` removes directory trees

## ⚠️ Common Pitfall
Forgetting `parents=True` in `mkdir()`. Without it, creating nested directories fails. Always use `path.mkdir(parents=True, exist_ok=True)`.

## 🧠 Memory Aid
**"Path = smart string + actions"**: A `Path` is a string that knows how to join, split, check existence, read, write, and delete.

## 🏃 Try It
Write a function `find_large_files(directory, min_mb=10)` that uses `Path.rglob` to find all files larger than a threshold.

## 🔗 Related
- [File I/O →](./04-file-io.md)
- [JSON & CSV →](./06-json-csv.md)

## ➡️ Next
[JSON & CSV](./06-json-csv.md)
