# 🔄 JSON & CSV
<!-- ⏱️ 10 min read | 🟡 Medium | 🧠 Applied -->

**What You'll Learn:** Read and write JSON and CSV — the two most common data interchange formats in the wild.

> 💡 **TL;DR — The whole point:** JSON for structured data (APIs, configs); CSV for tabular data (spreadsheets, databases). Master both for data exchange.

## 🔗 Why This Matters
Pathlib organizes files. But files contain data — and the two universal formats are JSON and CSV. APIs return JSON, spreadsheets export CSV, databases dump CSV. Knowing both is essential.

## The Concept
**JSON** (JavaScript Object Notation) maps naturally to Python dicts/lists. **CSV** (Comma-Separated Values) maps to rows and columns. Python's `json` and `csv` modules handle both with built-in support.

JSON is for nested structures (a user with an address). CSV is for flat tables (1000 users with the same fields).

## Code Example

```python
"""API response handling and data export/import with JSON & CSV."""

import json
import csv
from pathlib import Path


def fetch_api_response() -> dict:
    """Simulate an API response."""
    return {
        "status": "ok",
        "data": {
            "users": [
                {"id": 1, "name": "Eleven", "powers": ["telekinesis", "scream"]},
                {"id": 2, "name": "Mike", "powers": ["leadership"]},
                {"id": 3, "name": "Dustin", "powers": ["intelligence", "wit"]},
            ],
            "total": 3,
        },
    }


def save_users_json(users: list, path: str) -> None:
    """Save user data to JSON."""
    with open(path, "w") as f:
        json.dump(users, f, indent=2)


def load_users_json(path: str) -> list:
    """Load user data from JSON."""
    with open(path) as f:
        return json.load(f)


def users_to_csv(users: list, path: str) -> None:
    """Export users to CSV (flattening nested fields)."""
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "powers"])
        for u in users:
            writer.writerow([u["id"], u["name"], "; ".join(u["powers"])])


def csv_to_users(path: str) -> list:
    """Import users from CSV back to structured format."""
    users = []
    with open(path) as f:
        for row in csv.DictReader(f):
            users.append({
                "id": int(row["id"]),
                "name": row["name"],
                "powers": row["powers"].split("; "),
            })
    return users


response = fetch_api_response()
users = response["data"]["users"]
save_users_json(users, "/tmp/users.json")
users_to_csv(users, "/tmp/users.csv")
reloaded = csv_to_users("/tmp/users.csv")
print("JSON:", json.dumps(reloaded, indent=2))

Path("/tmp/users.json").unlink()
Path("/tmp/users.csv").unlink()
```

## 🔍 How It Works
- `json.dump(obj, file)` writes to a file; `json.dumps(obj)` returns a string
- `json.load(file)` reads from a file; `json.loads(string)` reads from a string
- `csv.DictReader` uses the first row as keys; `csv.DictWriter` needs `fieldnames`
- CSV `newline=""` prevents extra blank lines on Windows

## ⚠️ Common Pitfall
JSON keys and string values must be in double quotes (`"`). Single quotes (`'`) cause `json.decoder.JSONDecodeError`. Always use `json.dumps` to generate valid JSON.

## 🧠 Memory Aid
**"JSON = tree, CSV = table"**: JSON handles nested data (like a family tree). CSV handles flat data (like a spreadsheet).

## 🏃 Try It
Write a function `merge_csv_to_json(csv1_path, csv2_path, json_path)` that reads two CSV files, merges them by a common key, and writes the result as JSON.

## 🔗 Related
- [Pathlib & OS →](./05-pathlib-os.md)
- [Regex →](./07-regex.md)

## ➡️ Next
[Regex](./07-regex.md)
