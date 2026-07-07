# 🎯 pathlib Deep: rglob, with_suffix, stat, read_text/write_text
<!-- ⏱️ 12 min | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Use `rglob`, `with_suffix`, `stat`, `relative_to`, `resolve`, and `read_text`/`write_text` for production file operations.

> 💡 **TL;DR — The whole point:** `pathlib` gives you an OOP interface to the filesystem — recursively find files (`rglob`), rename extensions (`with_suffix`), read file metadata (`stat`), and read/write files in one line.

## 🔗 Why This Matters
Log rotation needs to find all `.log` files, rename them to `.bak`, check sizes, and calculate relative paths. These are daily tasks for any backend or DevOps developer.

## The Concept
`Path.rglob(pattern)` recursively finds all files matching a glob pattern. `Path.with_suffix(new_suffix)` returns a new path with a different extension. `.stat()` returns file metadata (size, mtime). `relative_to(base)` strips a base path to show the relative path. `resolve()` returns the absolute canonical path. `read_text`/`write_text` read and write files in one concise call.

## Code Example
```python
"""pathlib patterns: file operations, glob, log rotation — real dev workflows"""
from pathlib import Path
import tempfile, os, shutil

# Set up temp workspace simulating a real app's log directory
tmp = Path(tempfile.mkdtemp())
(tmp / "logs" / "2024" / "01").mkdir(parents=True)  # Creates all missing dirs

# write_text: concise file writing vs open/close boilerplate
(tmp / "logs" / "2024" / "01" / "app.log").write_text("[INFO] Started\n[ERROR] timeout\n")
(tmp / "logs" / "2024" / "01" / "db.log").write_text("[INFO] Connected\n")

# rglob: recursive glob to find ALL .log files in subtree
log_files = list(tmp.rglob("*.log"))
print(f"  Found {len(log_files)} log files")

# with_suffix: rename extension (e.g., .csv → .csv.bak before processing)
for f in log_files:
    backup = f.with_suffix(".log.bak")  # Only changes extension
    shutil.copy2(f, backup)  # Preserves metadata (mtime, etc.)

# stat: file size & mtime for log rotation / cleanup decisions
for f in log_files:
    st = f.stat()
    print(f"  {f.name}: {st.st_size}B, modified {st.st_mtime:.0f}")

# relative_to: get relative path from a base directory
for f in tmp.rglob("*"):
    if f.is_file():
        print(f"  Relative: {f.relative_to(tmp)}")

# resolve: get absolute path (resolves symlinks, ., ..)
print(f"  Abs: {tmp.resolve()}")

# Cleanup
shutil.rmtree(tmp)
print("  Cleanup done")
```

## 🔍 How It Works
- `rglob("*.log")` walks the entire directory tree returning every file matching `*.log`
- `with_suffix(".bak")` replaces the final suffix — `/path/file.log` → `/path/file.log.bak`
- `.stat()` returns an `os.stat_result` with `st_size` (bytes), `st_mtime` (modification timestamp), and more
- `relative_to(base)` computes the relative path between `base` and the path
- `resolve()` resolves all symlinks and normalizes `..` and `.` to an absolute path
- `read_text()` / `write_text()` handle opening, reading/writing, and closing in one call

## ⚠️ Common Pitfall
`with_suffix` replaces the *last* suffix only. `file.tar.gz.with_suffix(".zip")` gives `file.tar.zip`, not `file.zip`. To replace multiple suffixes, use `with_name(stem + ".zip")`.

## 🧠 Memory Aid
"rglob = 'find everywhere.' with_suffix = 'change extension.' stat = 'file info.' relative_to = 'where am I relative to base?' resolve = 'full real path.'"

## 🏃 Try It
Create a temp directory with nested `.txt` files. Use `rglob("*.txt")` to find them, print their sizes with `stat().st_size`, and rename them to `.txt.bak` using `with_suffix`.

## 🔗 Related
- [pathlib + os](../../../05_modules_io/lessons/05-pathlib-os.md) — pathlib basics and os module integration

## ➡️ Next
[Regex Patterns](25-re-patterns.md)
