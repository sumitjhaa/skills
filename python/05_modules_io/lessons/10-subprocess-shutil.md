# 🖥️ Subprocess & Shutil
<!-- ⏱️ 10 min read | 🟡 Medium | 🧠 Applied -->

**What You'll Learn:** Run shell commands with `subprocess` and perform high-level file operations with `shutil`.

> 💡 **TL;DR — The whole point:** `subprocess` lets Python run any command-line tool; `shutil` handles file/directory operations that `pathlib` can't.

## 🔗 Why This Matters
Hashlib/secrets handle data security. But what about system tasks — backups, archiving, running git commands, or moving files around? Subprocess and shutil bridge Python with the operating system.

## The Concept
**subprocess** spawns new processes, connects to their input/output/error pipes, and gets return codes. Use it to run git, ffmpeg, curl, or any command-line tool from Python.

**shutil** provides high-level file operations: copy entire directory trees, move files, create archives (zip/tar), and disk usage queries.

Think of subprocess as Python's way of saying "hey shell, run this for me" and shutil as a super-powered file manager.

## Code Example

```python
"""Running shell commands, file operations, and archiving."""

import subprocess
import shutil
from pathlib import Path


def run_command(cmd: list) -> dict:
    """Run a shell command and capture output."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def create_backup(source_dir: str, output_name: str) -> Path:
    """Create a compressed zip archive of a directory."""
    base = Path(source_dir)
    output = Path(output_name)
    return Path(shutil.make_archive(str(output.with_suffix("")), "zip", base))


def disk_usage(path: str = "/") -> dict:
    """Get disk usage information."""
    usage = shutil.disk_usage(path)
    return {
        "total_gb": round(usage.total / (1024**3), 2),
        "used_gb": round(usage.used / (1024**3), 2),
        "free_gb": round(usage.free / (1024**3), 2),
        "percent_used": round(usage.used / usage.total * 100, 1),
    }


print("Disk usage:", disk_usage("/"))

# Run a command
result = run_command(["echo", "Hello from subprocess!"])
print(f"Command result: {result['stdout']}")

# Create backup demo
tmp = Path("/tmp/backup_demo")
(tmp / "docs").mkdir(parents=True, exist_ok=True)
(tmp / "docs" / "readme.txt").write_text("Important data")
(tmp / "config.ini").write_text("[settings]\nversion=1.0")

archive = create_backup(tmp, "/tmp/project_backup")
print(f"Backup created: {archive} ({archive.stat().st_size} bytes)")

# Cleanup
shutil.rmtree(tmp)
archive.unlink()
```

## 🔍 How It Works
- `subprocess.run(cmd, capture_output=True, text=True)` runs a command and returns `CompletedProcess`
- Use `shell=True` carefully — it's a security risk with user input
- `shutil.make_archive` creates .zip, .tar, .gztar, .bztar, .xztar
- `shutil.disk_usage` returns a named tuple with total, used, free bytes

## ⚠️ Common Pitfall
Using `shell=True` with user input. Never do `subprocess.run(f"rm {user_input}", shell=True)` — it's a command injection vulnerability. Pass arguments as a list instead.

## 🧠 Memory Aid
**"subprocess = Python talks to shell, shutil = Python manages files"**: Two tools for system interaction — one for commands, one for files.

## 🏃 Try It
Write a function `git_status(directory)` that runs `git status --short` in the given directory and returns the output as a string. Handle errors if the directory isn't a git repo.

## 🔗 Related
- [Hashlib, Secrets & UUID →](./09-hashlib-secrets-uuid.md)
- [Pathlib & OS →](./05-pathlib-os.md)

## ➡️ Next
Continue to [Phase 06: Errors](../../06_errors/lessons/01-exception-hierarchy.md)
