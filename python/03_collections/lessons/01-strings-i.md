# 🎯 Strings I: Indexing & Slicing
<!-- ⏱️ 8 min read | 🟢 Easy | 🧠 Core -->

**What You'll Learn:** Access individual characters by index, extract substrings with slicing, reverse strings, and understand why strings can't be changed in place.

> 💡 **TL;DR — The whole point:** `string[index]` gets one character; `string[start:stop:step]` extracts a substring; strings are **immutable** — you can't change them in place.

## 🔗 Why This Matters
You've used strings since Phase 01 — but only as whole values. Real-world data processing is about extracting pieces: the hashtag from a tweet, the domain from an email, the gene sequence from a DNA strand. Indexing and slicing are the scalpel for cutting strings into exactly the pieces you need.

## The Concept

A string is a sequence of characters. Python lets you reach into that sequence with **indexing** — square brackets with a number. Index `0` is the first character. Negative indices count from the end (`-1` is the last character).

**Slicing** grabs a range with `[start:stop:step]`. `start` is inclusive, `stop` is exclusive, `step` controls direction and stride. Leave any part blank for sensible defaults. A step of `-1` reverses the string. Bonus: out-of-range slices don't error — they return whatever's available.

Strings are **immutable** — `text[0] = "J"` raises a `TypeError`. Every string operation creates a new string.

## Code Example

```python
"""DNA sequence analysis — extracting codons with indexing and slicing"""

# A DNA sequence (simplified)
dna = "ATGCGTACGTTAG"
#       0123456789...

print(f"DNA Sequence: {dna}")
print(f"Length: {len(dna)} bases")

# Indexing — individual bases
print("\n=== Single Base Access ===")
print(f"  First base (index 0): {dna[0]}")
print(f"  Last base (index -1): {dna[-1]}")
print(f"  Third base (index 2): {dna[2]}")

# Slicing — extracting codons (triplets)
print("\n=== Codon Extraction ===")
print(f"  First codon [0:3]: {dna[0:3]}")     # ATG
print(f"  Second codon [3:6]: {dna[3:6]}")    # CGT
print(f"  Third codon [6:9]: {dna[6:9]}")     # ACG

# Slice shorthand
print("\n=== Slice Shorthand ===")
print(f"  First 4 bases [:4]: {dna[:4]}")       # ATGC
print(f"  From base 4 onward [4:]: {dna[4:]}")  # TACGTTAG
print(f"  Last 3 bases [-3:]: {dna[-3:]}")      # TAG

# Step and reverse
print("\n=== Stepping ===")
print(f"  Every 2nd base [::2]: {dna[::2]}")        # AGCACG
print(f"  Every 3rd base [::3]: {dna[::3]}")        # AGTG
print(f"  Reversed [::-1]: {dna[::-1]}")             # GATTGCATGCGTA
print(f"  Reverse every 2nd [::-2]: {dna[::-2]}")    # GACGGA

# Immutability demonstration
print("\n=== Immutability ===")
print(f"  Strings cannot be modified in place.")
print(f"  dna[0] = 'T' would raise TypeError.")
```

## 🔍 How It Works

- `dna[0]` — first character at position 0; all indexing starts at 0
- `dna[-1]` — last character; negative indices wrap around from the end
- `dna[0:3]` — characters at indices 0, 1, 2 (stop is exclusive, so 3 is NOT included)
- `dna[:4]` — from start to index 3 (blank start = beginning)
- `dna[4:]` — from index 4 to the end (blank stop = end)
- `dna[-3:]` — from 3rd-from-last to the end
- `dna[::2]` — full string, stepping by 2: takes indices 0, 2, 4, ...
- `dna[::-1]` — step of -1 walks backward through the string
- Strings immutable: any operation that seems to change a string actually creates a new one

## ⚠️ Common Pitfall

Index out of range: `dna[50]` raises `IndexError` if the string is shorter than 51 characters. Slicing is forgiving (returns empty string or partial), but direct indexing will crash. Also, confusing `start:stop` as inclusive-inclusive — remember `stop` is exclusive: `"hello"[0:4]` gives `"hell"`, not `"hello"`.

## 🧠 Memory Aid

**"Index 0 is the starting line, negative is the finish line. The colon `:` is the portal — what goes before is where you start, what goes after is where you stop (but don't cross the stop line!)."** Think of platform 9¾ at King's Cross — step through the colon into the sliced substring.

## 🏃 Try It

Run the code file:
```bash
python code/03-01-strings-i.py
```
Then create your own string with a social media hashtag like `"#PythonIsAwesome"` and extract just the `"Python"` part using slicing.

## 🔗 Related

- [Strings II: Methods](02-strings-ii.md) — methods that build on indexing and slicing
- [Lists I](03-lists-i.md) — same indexing/slicing rules apply to lists

## ➡️ Next

→ [02 — Strings II: Methods](02-strings-ii.md)
