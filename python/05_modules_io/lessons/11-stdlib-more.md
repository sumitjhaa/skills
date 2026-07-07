# 🎯 More Practical Standard Library
<!-- ⏱️ 14 min | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Seven more essential stdlib modules — `decimal`, `configparser`, `glob`, `timeit`, `base64`, `zipfile`, and `tempfile` — for production Python work.

> 💡 **TL;DR — The whole point:** Before you `pip install`, check if Python's stdlib already has it: `decimal` for money, `configparser` for configs, `glob` for files, `timeit` for benchmarks, `base64` for API tokens, `zipfile` for archives, `tempfile` for scratch files.

## 🔗 Why This Matters
Real Python code needs more than syntax. You'll read config files (`configparser`), handle money accurately (`decimal`), find files by pattern (`glob`), benchmark performance (`timeit`), encode binary data safely (`base64`), create archives (`zipfile`), and manage temporary scratch files (`tempfile`). All stdlib — no `pip install`.

## The Concept

| Module | Use Case | Domain |
|--------|----------|--------|
| `decimal` | Precise money math (no float errors) | E-commerce, finance |
| `configparser` | Read `.ini` / `.cfg` configuration files | App configuration |
| `glob` | Find files matching a wildcard pattern | File processing |
| `timeit` | Micro-benchmark Python code snippets | Performance tuning |
| `base64` | Encode binary as URL-safe text | API tokens, auth headers |
| `zipfile` | Create/extract ZIP archives | Data export, backups |
| `tempfile` | Auto-cleaning temporary files | Testing, batch processing |

## Code Example

```python
"""More practical stdlib: decimal, configparser, glob, timeit, base64, zipfile, tempfile"""
from decimal import Decimal, ROUND_HALF_UP
from configparser import ConfigParser
import glob
import timeit
import base64
import zipfile
import tempfile
import os
from pathlib import Path

print("=== decimal — precise money math ===")
price = Decimal("19.99")
tax = price * Decimal("0.08")
total = price + tax
print(f"${price} + tax (${tax:.2f}) = ${total:.2f}")
print(f"Float would be: {19.99 * 1.08:.17f}  # imprecise!")
print(f"Rounded: {total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}")

print("\n=== configparser — .ini files ===")
cfg = ConfigParser()
cfg.read_string("[database]\nhost = localhost\nport = 5432\n")
print(f"DB: {cfg['database']['host']}:{cfg['database']['port']}")

print("\n=== glob — file pattern matching ===")
pattern = os.path.join(os.path.dirname(__file__) or ".", "05-*.py")
matches = sorted(glob.glob(pattern))
print(f"Found {len(matches)} files: {[Path(m).name for m in matches[:3]]}...")

print("\n=== timeit — benchmarking ===")
setup = "nums = list(range(1000))"
t_list = timeit.timeit("[x*2 for x in nums]", setup, number=10000)
t_gen = timeit.timeit("list(x*2 for x in nums)", setup, number=10000)
print(f"List comp: {t_list:.4f}s | Generator: {t_gen:.4f}s")

print("\n=== base64 — API-safe binary encoding ===")
token = base64.urlsafe_b64encode(b"user:api_key_12345").decode()
print(f"Encoded: {token}")
decoded = base64.urlsafe_b64decode(token.encode()).decode()
print(f"Decoded: {decoded}")

print("\n=== zipfile + tempfile ===")
with tempfile.TemporaryDirectory() as tmpdir:
    zip_path = Path(tmpdir) / "example.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("data.txt", "Hello from ZIP!")
    with zipfile.ZipFile(zip_path, "r") as zf:
        print(f"ZIP: {zf.namelist()} → {zf.read('data.txt').decode()}")
print("Temp dir auto-cleaned.")
```

## 🔍 How It Works
- `Decimal("19.99")` avoids float's binary representation errors — use strings, not floats
- `ConfigParser.read_string()` parses INI syntax without a file on disk
- `glob.glob("*.py")` returns all `.py` files matching the pattern in the current dir
- `timeit.timeit(stmt, setup, number=N)` runs the statement N times and returns total seconds
- `base64.urlsafe_b64encode()` produces URL-safe base64 (`-` and `_` instead of `+` and `/`)
- `ZipFile.writestr()` adds an in-memory string as a file inside the archive
- `TemporaryDirectory()` creates a temp folder that auto-deletes on context exit

## ⚠️ Common Pitfall
- `Decimal` from floats (`Decimal(0.1)`) still carries float error — always use string args: `Decimal("0.1")`
- `glob` without recursive (`**`) only matches in one directory — add `recursive=True`
- `timeit` measures wall-clock time, not CPU — other processes affect results

## 🧠 Memory Aid
"Float for physics, Decimal for money, ConfigParser for settings, glob for files, timeit for speed, base64 for tokens, ZipFile for archives, TempFile for scratch."

## 🏃 Try It
Write a function that reads a config file with `[pricing]` section (tax_rate, currency), then uses `decimal` to compute the final price of a list of items. Benchmark your implementation vs a float version.

## 🔗 Related
- [08-Useful Modules](08-useful-modules.md) — `hashlib`, `statistics`, `pprint`, `io.StringIO`
- [04-File I/O](04-file-io.md) — reading/writing files
- [06-JSON & CSV](06-json-csv.md) — data serialization
- [09-Hashlib, Secrets & UUID](09-hashlib-secrets-uuid.md) — more security modules

## ➡️ Next
[10-Subprocess & Shutil](10-subprocess-shutil.md)
