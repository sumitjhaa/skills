# 🎯 codecs, unicodedata, difflib, textwrap — Text Processing Deep
<!-- ⏱️ 14 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Master encoding/decoding with `codecs`, Unicode introspection with `unicodedata`, text diffs with `difflib`, and pretty-printing with `textwrap`.

> 💡 **TL;DR — The whole point:** `codecs` handles text encoding/decoding including BOM and custom codecs, `unicodedata` inspects every Unicode character, `difflib` finds the closest matches and shows diffs, and `textwrap` formats text to fit terminal widths.

## 🔗 Why This Matters
NLP pipelines normalize Unicode (NFD decomposes "é" into "e" + combining accent for consistent comparison). Code review tools use `difflib` for side-by-side diffs. CLI tools use `textwrap` for help text. `codecs.open()` is the correct way to read files with unknown encodings.

## The Concept
- `codecs.encode(s, 'rot_13')` / `codecs.decode(b, 'hex')`. `codecs.open(path, 'r', encoding='utf-8-sig')` strips BOM automatically. Register custom codecs with `codecs.register`
- `unicodedata.lookup('SNOWMAN')` → `'☃'`. `unicodedata.name('☃')` → `'SNOWMAN'`. `unicodedata.category('A')` → `'Lu'` (Letter uppercase). Normalization forms: NFC (composed), NFD (decomposed), NFKC/NFKD (compatible — strips formatting)
- `difflib.SequenceMatcher` = ratio of similarity. `get_close_matches(word, list, n, cutoff)` = fuzzy matching. `unified_diff` = git-style diff. `HtmlDiff` = colorized HTML diff
- `textwrap.wrap(text, width)` → list of lines. `fill` = `'\n'.join(wrap(...))`. `dedent` removes common leading whitespace. `indent` adds prefix. `shorten` = truncate with ellipsis

## Code Example
```python
"""Unicode normalization for user input, spell checker, text diff view, CLI help."""

import unicodedata, difflib, textwrap


# ─── Unicode normalization for search ───
def normalize_input(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()

assert normalize_input("café") == "cafe"
print(f"char 'é' → name={unicodedata.name('é')}, cat={unicodedata.category('é')}")

# ─── difflib: "Did you mean?" suggestions ───
def suggest(word: str, options: list[str]) -> list[str]:
    return difflib.get_close_matches(word, options, n=3, cutoff=0.6)

cmds = ["commit", "checkout", "clone", "branch", "push"]
print(f"Did you mean 'comit'? → {suggest('comit', cmds)}")

# ─── difflib: unified diff ───
before = ["def hello():", '    print("world")']
after = ["def greet():", '    print("hello")', '    print("world")']
diff = difflib.unified_diff(before, after, fromfile="old.py", tofile="new.py")
print("\n".join(diff))

# ─── textwrap: Format CLI help ───
help_text = "This command initializes a new repository with the specified configuration options."
print(textwrap.fill(help_text, width=40))
print(textwrap.shorten(help_text, width=30))
```

## 🔍 How It Works
- Unicode normalization forms: NFC = "é" as one codepoint (U+00E9), NFD = "e" + combining accent (U+0065 U+0301). NFKC/NFKD also replace characters like ﬁ → fi for search
- `difflib.SequenceMatcher` uses the Ratcliff/Obershelp algorithm (longest contiguous matching subsequence). Ratio = 2 * M / T where M = sum of match lengths, T = total characters
- `textwrap` respects existing newlines. `replace_whitespace=True` (default) converts tabs to spaces. `break_long_words=True` prevents overflow at width boundary
- `codecs` BOM: `utf-8-sig` reads/strips BOM, `utf-16`/`utf-32` use BOM for endianness detection

## ⚠️ Common Pitfall
NFD normalization does NOT make strings ASCII-safe. `'ñ'.encode('ascii', 'ignore')` silently drops characters. Always check with unicodedata.category after normalization. `difflib.get_close_matches` is O(n*m) — don't use on millions of words without indexing.

## 🧠 Memory Aid
"`codecs` = encoding plumbing. `unicodedata` = Unicode encyclopedia. `difflib` = fuzzy matcher + diff. `textwrap` = word wrap. NFC = composed (1 char). NFD = decomposed (2+ chars). `get_close_matches` = 'did you mean?'"

## 🏃 Try It
Write a `slugify` function that normalizes Unicode to NFKD, removes non-ASCII characters, lowercases, and replaces spaces with hyphens. Then write a simple spellchecker that reads a dictionary and suggests corrections.

## 🔗 Related
- [Modules & IO: codecs](../05_modules_io/lessons/12-filesystem.md) — file encoding basics
- [Comprehensions Deep](07-comprehensions-deep.md) — text processing pipelines

## ➡️ Next
Review and practice with [Exercises](../practice/exercises.md)
