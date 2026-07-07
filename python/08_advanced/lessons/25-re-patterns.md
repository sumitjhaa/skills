# 🎯 Regex Patterns: Compiled, Named Groups, Lookahead, VERBOSE
<!-- ⏱️ 14 min | 🔴 Advanced | 🧠 Applied -->

**What You'll Learn:** Use `re.compile` with `VERBOSE`, named groups `(?P<name>)`, lookahead `(?=)`, and `finditer` for production log parsing.

> 💡 **TL;DR — The whole point:** Compiled regex with `VERBOSE` lets you write readable, commented patterns; named groups give self-documenting matches; lookahead finds context without consuming; `finditer` iterates matches memory-efficiently.

## 🔗 Why This Matters
Parsing Nginx access logs, extracting structured data from unstructured text, validating formats — regex is the tool, and these advanced patterns make it maintainable and efficient.

## The Concept
`re.compile(r"...", re.VERBOSE)` lets you spread patterns across lines with comments and whitespace. Named groups `(?P<name>...)` let you access matches by name instead of numeric index. Lookahead `(?=...)` checks for a pattern without including it in the match. `finditer` yields `Match` objects lazily instead of building a list of strings.

## Code Example
```python
"""Regex patterns: compiled, named groups, lookahead, verbose — log parsing"""
import re

# Compile with VERBOSE: multi-line pattern with comments for readability
# Real use: parsing Apache/Nginx access logs
log_pat = re.compile(r"""
    (\d+\.\d+\.\d+\.\d+) \s+   # IP address — group 1
    \S+ \s+ \S+ \s+            # ident & authuser (skip)
    \[([^\]]+)\] \s+            # timestamp in brackets — group 2
    "(GET|POST|PUT|DELETE) \s+  # HTTP method — group 3
    (/\S*)                      # Path — group 4
""", re.VERBOSE)

log = '192.168.1.1 - - [10/Jan/2024:13:55:36] "GET /api/users HTTP/1.1" 200 2326'
m = log_pat.search(log)
if m:
    print(f"  IP={m.group(1)}, Time={m.group(2)}")
    print(f"  Method={m.group(3)}, Path={m.group(4)}")
    print(f"  Span: {m.span(1)}")  # (0, 11) — start/end of IP match

# Named groups: (?P<name>...) more readable than numbered groups
date_pat = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})")
d = date_pat.search("Event on 2024-01-15")
print(f"  Year={d.group('year')}, Month={d.group('month')}")

# Lookahead: find ERROR only when followed by 'timeout' (not 'permission')
text = "ERROR timeout ERROR permission ERROR timeout"
matches = re.findall(r"ERROR (?=timeout)", text)
print(f"  Timeout errors: {len(matches)}")

# finditer: memory-efficient iteration over matches (no giant list)
for match in re.finditer(r"\d+", "abc 123 def 456"):
    print(f"  Found '{match.group()}' at {match.start()}")
```

## 🔍 How It Works
- `re.VERBOSE` ignores whitespace and `#` comments inside the pattern — essential for complex patterns
- `(?P<name>...)` captures into a named group accessed via `match.group('name')`
- Lookahead `(?=pattern)` matches the position where `pattern` follows, without consuming characters
- `re.finditer(pattern, string)` returns an iterator of `Match` objects — use when you have many matches to avoid building a list
- `match.span(group)` returns `(start, end)` tuple of the match position

## ⚠️ Common Pitfall
In `VERBOSE` mode, literal spaces must be written as `\s` or `[ ]`. A plain space character is ignored. Also, the `#` character starts a comment — use `\#` for a literal `#`.

## 🧠 Memory Aid
"VERBOSE = 'regex with comments.' Named groups = `?P<name>` = 'name your capture.' Lookahead = `?=` = 'check without eating.' finditer = 'lazy match list.'"

## 🏃 Try It
Write a `VERBOSE` pattern to parse a CSV line `"Alice",30,"New York"` into named groups. Use named groups for name, age, city.

## 🔗 Related
- [Regex](../../../05_modules_io/lessons/07-regex.md) — regex basics, groups, character classes

## ➡️ Next
[JSON Patterns](26-json-patterns.md)
