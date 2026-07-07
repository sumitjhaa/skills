# 🧰 Useful Standard Library Modules
<!-- ⏱️ 10 min read | 🟡 Medium | 🧠 Applied -->

**What You'll Learn:** Practical standard library modules — `hashlib`, `statistics`, `pprint`, `io.StringIO`, `tempfile`, `glob` — no `pip install` needed.

> 💡 **TL;DR — The whole point:** Python's standard library is a treasure chest. These five modules solve everyday problems: hashing, stats, pretty-printing, in-memory files, and temp files.

## 🔗 Why This Matters
Regex handles text patterns. These modules handle other common tasks: hash passwords (`hashlib`), analyze data (`statistics`), debug output (`pprint`), mock files (`StringIO`), and create temporary files (`tempfile`).

## The Concept
These modules are part of Python's "batteries included" philosophy. Before you `pip install` anything, check if the standard library has what you need.

| Module | When to Use |
|--------|-------------|
| `hashlib` | Password hashing, data integrity checks |
| `statistics` | Mean, median, mode, stdev of small datasets |
| `pprint` | Debugging complex nested data structures |
| `io.StringIO` | Testing file operations without real files |
| `tempfile` | Creating temp files/dirs that auto-clean |

## Code Example

```python
"""hashlib, statistics, pprint — password hashing, data analysis, debug output."""

import hashlib
import statistics
from pprint import pprint
from io import StringIO


def hash_password(password: str) -> str:
    """Hash a password with SHA-256 + salt (simplified — use bcrypt in prod)."""
    salt = "static_salt"  # In production, use a random salt per user
    return hashlib.sha256((password + salt).encode()).hexdigest()


def analyze_survey(data: list) -> dict:
    """Compute survey statistics."""
    return {
        "mean": round(statistics.mean(data), 2),
        "median": statistics.median(data),
        "stdev": round(statistics.stdev(data), 2) if len(data) > 1 else 0,
        "min": min(data),
        "max": max(data),
    }


# Test file operations without writing to disk
def process_data(data: str) -> str:
    """Simulate file processing using StringIO."""
    buf = StringIO(data)
    lines = [line.strip().upper() for line in buf if line.strip()]
    return "\n".join(lines)


stored = hash_password("my_secure_password")
print(f"Hashed password: {stored[:20]}...")

ratings = [4, 5, 3, 4, 5, 2, 4, 5, 5, 4]
pprint(analyze_survey(ratings))

data = process_data("  hello  \n  world  \n\n  python  ")
print(f"Processed:\n{data}")
```

## 🔍 How It Works
- `hashlib` uses OpenSSL under the hood — supports SHA-1, SHA-256, MD5, etc.
- `statistics` functions handle edge cases (empty data, single values)
- `pprint` sorts dict keys and indents nested structures for readability
- `StringIO` behaves like a file object but lives in memory
- `tempfile.NamedTemporaryFile` creates a file that's deleted when closed

## ⚠️ Common Pitfall
Using MD5 or SHA-1 for password storage. They're too fast — use `bcrypt` or `hashlib.pbkdf2_hmac` for password hashing. SHA-256 is fine for data integrity.

## 🧠 Memory Aid
**"Batteries included"**: Before installing a third-party library, check if the stdlib has what you need. Often it does.

## 🏃 Try It
Use `StringIO` to simulate reading a CSV file. Write data to a `StringIO`, seek to 0, then use `csv.DictReader` to read it back.

## 🔗 Related
- [Regex →](./07-regex.md)
- [Hashlib, Secrets, UUID →](./09-hashlib-secrets-uuid.md)

## ➡️ Next
[Hashlib, Secrets & UUID](./09-hashlib-secrets-uuid.md)
