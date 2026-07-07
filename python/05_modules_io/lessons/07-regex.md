# 🔍 Regex
<!-- ⏱️ 12 min read | 🔴 Hard | 🧠 Applied -->

**What You'll Learn:** Use regular expressions to search, match, extract, replace, and split strings with the `re` module.

> 💡 **TL;DR — The whole point:** Regex is a mini-language for pattern matching in text — like a metal detector for specific string patterns.

## 🔗 Why This Matters
JSON/CSV gave you structured data. But what about unstructured text — log files, user input, HTML, emails? Regex finds patterns in any string.

## The Concept
A **regular expression** is a sequence of characters that defines a search pattern. The `re` module compiles the pattern into bytecode and uses it to scan text. Raw strings (`r"..."`) prevent Python from interpreting backslashes.

Think of regex like a search engine on steroids — instead of exact matches, you search by pattern: "find me anything that looks like a phone number" or "extract all email addresses".

## Code Example

```python
"""Log parsing, data validation, and text extraction with regex."""

import re


def parse_log_line(line: str) -> dict | None:
    """Parse a log line: TIMESTAMP LEVEL MODULE: MESSAGE"""
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (ERROR|WARN|INFO) ([\w.]+): (.+)"
    m = re.match(pattern, line)
    if m:
        return {"timestamp": m.group(1), "level": m.group(2), "module": m.group(3), "message": m.group(4)}
    return None


def extract_emails(text: str) -> list:
    """Extract all email addresses from text."""
    return re.findall(r"[\w.]+@[\w.]+\.\w+", text)


def validate_phone(phone: str) -> bool:
    """Validate US phone number formats."""
    return bool(re.fullmatch(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", phone.strip()))


def redact_passwords(text: str) -> str:
    """Redact password=... patterns in config files."""
    return re.sub(r"(password|passwd|pwd)=(\S+)", r"\1=***REDACTED***", text, flags=re.IGNORECASE)


logs = [
    "2024-01-15 10:30:45 ERROR db.connection: Connection refused",
    "2024-01-15 10:31:12 INFO app.startup: Server started on port 8080",
]

for line in logs:
    print(parse_log_line(line))

text = "Contact: eleven@lab.gov or mike@hawkins.org for tips."
print("Emails:", extract_emails(text))
print("Valid phone?", validate_phone("(555) 123-4567"))
print("Redacted:", redact_passwords("db_password=supersecret123"))
```

## 🔍 How It Works
- `re.search` finds first match anywhere in string
- `re.match` checks only from position 0
- `re.findall` returns all non-overlapping matches as a list
- `re.sub` replaces matched patterns
- `re.fullmatch` requires the entire string to match
- Compile with `re.compile(pattern)` for repeated use

## ⚠️ Common Pitfall
Greedy vs lazy matching. `.+` is greedy (matches as much as possible). `.+?` is lazy (matches as little as possible). Use `.*?` for minimal matches.

## 🧠 Memory Aid
**"Regex sees characters, not words"**: You're telling Python what the text looks like at the character level — digits, letters, whitespace, positions.

## 🏃 Try It
Write a function `extract_hashtags(text)` that uses `re.findall` to extract all hashtags (words starting with `#`) from a string.

## 🔗 Related
- [JSON & CSV →](./06-json-csv.md)
- [Useful Modules →](./08-useful-modules.md)

## ➡️ Next
[Useful Standard Library Modules](./08-useful-modules.md)
