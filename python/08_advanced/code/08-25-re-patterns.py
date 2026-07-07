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
