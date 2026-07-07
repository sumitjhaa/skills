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
