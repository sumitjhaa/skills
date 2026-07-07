# 🎯 CSV Patterns: DictReader/DictWriter, Sniffer, Quoting
<!-- ⏱️ 12 min | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Use `DictReader`/`DictWriter`, `Sniffer`, and quoting options for production data export/import.

> 💡 **TL;DR — The whole point:** `csv.DictReader`/`DictWriter` handle rows as dicts (no manual indexing), `Sniffer` auto-detects CSV format (delimiter, quote char), and quoting options protect special characters.

## 🔗 Why This Matters
Exporting database queries to CSV, parsing user-uploaded files from unknown sources, and handling fields with commas or quotes are daily data engineering tasks.

## The Concept
`DictWriter` writes rows from dicts using a `fieldnames` list — no positional indexing. `DictReader` reads rows into `OrderedDict`s keyed by the header row. `Sniffer.sniff(sample)` analyzes a CSV sample and detects its dialect (delimiter, quote character, etc.). `quoting=csv.QUOTE_ALL` wraps every field in quotes to handle embedded commas and newlines safely.

## Code Example
```python
"""CSV patterns: DictReader/Writer, Sniffer, quoting — data pipelines"""
import csv, io

# --- 1. DictWriter: write from dicts (no manual indexing) ---
# Real use: Exporting database query results to CSV
fieldnames = ["name", "email", "score"]
rows = [
    {"name": "Alice", "email": "alice@example.com", "score": 95},
    {"name": "Bob", "email": "bob@test.com", "score": 87},
]

output = io.StringIO()  # In-memory file (use real file path in production)
writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
writer.writeheader()  # Writes fieldnames as first row
writer.writerows(rows)  # Writes all rows
print(f"CSV output:\n{output.getvalue()}")

# --- 2. Sniffer: auto-detect CSV format (delimiter, quote char) ---
# Real use: Reading CSVs from unknown sources (user uploads, third-party data)
sample = "name;age;city\nAlice;30;NYC\nBob;25;LAX"  # Semicolon-delimited
dialect = csv.Sniffer().sniff(sample)  # Detects delimiter=';', doublequote=True
print(f"Detected delimiter: '{dialect.delimiter}'")  # ';'
sniffed = list(csv.DictReader(io.StringIO(sample), dialect=dialect))
print(f"Parsed (sniffed): {sniffed}")

# --- 3. Quoting options: handle special characters (commas, quotes, newlines) ---
special = [{"text": "Hello, world!", "notes": 'He said "hi"'}]
out2 = io.StringIO()
w2 = csv.DictWriter(out2, fieldnames=["text", "notes"], quoting=csv.QUOTE_ALL)
w2.writeheader()
w2.writerows(special)
print(f"Quoted:\n{out2.getvalue()}")
```

## 🔍 How It Works
- `DictWriter(fieldnames=...)` maps dict keys to CSV columns — `extrasaction='ignore'` silently drops extra keys
- `writeheader()` writes `fieldnames` as the first row automatically
- `Sniffer().sniff(sample)` returns a `Dialect` object with detected `delimiter`, `quotechar`, `doublequote`, etc.
- `csv.QUOTE_ALL` wraps every field in quotes — use `QUOTE_NONNUMERIC`, `QUOTE_MINIMAL` (default), or `QUOTE_NONE` as needed
- Use `io.StringIO()` for in-memory CSV operations; pass a file path string to write directly

## ⚠️ Common Pitfall
`Sniffer.sniff()` needs a large enough sample — it may misdetect delimiters with very short samples. Always pass at least the header and a few rows. When it fails, fall back to a default dialect or ask the user.

## 🧠 Memory Aid
"DictWriter = 'dicts to CSV rows.' DictReader = 'CSV rows to dicts.' Sniffer = 'guess the CSV format.' QUOTE_ALL = 'safe from commas.'"

## 🏃 Try It
Write a list of dicts with `["id", "name", "bio"]` where `bio` contains commas and quotes. Export with `QUOTE_ALL` and verify it parses back correctly.

## 🔗 Related
- [JSON + CSV](../../../05_modules_io/lessons/06-json-csv.md) — CSV basics, reader/writer

## ➡️ Next
[GC & Weakref Patterns](29-gc-weakref-patterns.md)
