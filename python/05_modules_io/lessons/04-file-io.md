# 📄 File I/O
<!-- ⏱️ 10 min read | 🟢 Easy | 🧠 Core -->

**What You'll Learn:** How to read and write files using `open()`, context managers, and different file modes.

> 💡 **TL;DR — The whole point:** Files let your program remember data between runs — config files, logs, saved games, exported reports.

## 🔗 Why This Matters
Datetime showed you how to work with time. Now learn how to persist data — configuration files, log files, data exports. Without file I/O, everything disappears when the program ends.

## The Concept
Python's `open()` function returns a file object. Use modes to specify read (`"r"`), write (`"w"` — truncates), append (`"a"`), or exclusive create (`"x"`). Always use the `with` statement — it automatically closes the file, even if an error occurs.

Think of file I/O like a notebook:
- `"r"` — open and read what's written
- `"w"` — tear out all pages and start fresh
- `"a"` — add a new page at the end
- `"r+"` — read and edit any page

## Code Example

```python
"""Config files, log reading, and CSV export — data pipeline foundations."""

from pathlib import Path


def load_config(path: str) -> dict:
    """Load a simple key=value config file into a dict."""
    config = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, _, value = line.partition("=")
                config[key.strip()] = value.strip()
    return config


def write_log(path: str, entries: list) -> None:
    """Write log entries to a file, one per line."""
    with open(path, "a") as f:
        for entry in entries:
            f.write(f"{entry}\n")


def export_csv(path: str, data: list, headers: list) -> None:
    """Simple CSV export without csv module."""
    with open(path, "w") as f:
        f.write(",".join(headers) + "\n")
        for row in data:
            f.write(",".join(str(v) for v in row) + "\n")


with open("/tmp/config.txt", "w") as f:
    f.write("# App config\n")
    f.write("db_host=localhost\n")
    f.write("db_port=5432\n")
    f.write("debug=true\n")

print(load_config("/tmp/config.txt"))

write_log("/tmp/app.log", ["[INFO] Started", "[INFO] Connected"])
export_csv("/tmp/data.csv", [("Alice", 30), ("Bob", 25)], ["name", "age"])
print(Path("/tmp/data.csv").read_text())
```

## 🔍 How It Works
- `open()` returns a file object with an internal buffer
- `with` calls `f.__exit__()` which closes the file (even on exceptions)
- Writing is buffered; `f.flush()` forces write to disk
- Binary mode (`"rb"` / `"wb"`) reads/writes `bytes` — needed for images, audio

## ⚠️ Common Pitfall
Forgetting `newline=""` when writing CSV on Windows prevents extra blank lines. Always use `with open(path, "w", newline="")` for CSV.

## 🧠 Memory Aid
**"Read, Write, Append — RWA"**: The three basic modes. Like a tape: read plays, write records over, append adds to the end.

## 🏃 Try It
Write a `read_config(path)` that reads a JSON config file and returns the parsed dict. Handle `FileNotFoundError` by returning an empty dict.

## 🔗 Related
- [Datetime →](./03-datetime.md)
- [Pathlib & OS →](./05-pathlib-os.md)

## ➡️ Next
[Pathlib & OS](./05-pathlib-os.md)
