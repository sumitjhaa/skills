# 19️⃣ BISECT — FIND THE BUG

⏱️ **Time:** ~10 min | 🏁 **TL;DR:** `git bisect` binary-searches through history to find the exact commit that introduced a bug. `git bisect run` automates it with a test script.

## 🔁 LAST TIME...

In [18-reflog.md](18-reflog.md), you learned to recover lost commits with `git reflog`.

---

### Manual Bisect

```bash
git bisect start                          # Start the process
git bisect bad                            # Mark current HEAD as broken
git bisect good v1.0.0                    # Mark a known working version
# Git checks out a commit halfway. You test:
git bisect good    # ← this commit works
git bisect bad     # ← this commit is broken
# Repeat until git announces the first bad commit
git bisect reset                          # End session
```

### Visualize the Bisect Range

```bash
git bisect visualize           # Opens gitk with good/bad highlighted
git bisect visualize --oneline # Text version of remaining range
```

### `git bisect run` — Fully Automated

```bash
git bisect start HEAD v1.0.0
git bisect run npm test
# Git: checkout → run test → mark good/bad → repeat → found it!

# Or use a custom script:
git bisect run ./check.sh
```

Script must exit 0 (good) or non-zero (bad).

👉 **Mnemonic:** Bisect = "Binary search through time." `bisect run` = "Test every candidate automatically."

---

## 🧠 KEY TAKEAWAYS

- **`git bisect`** performs a binary search O(log n) to find the first bad commit
- **Mark `bad` (broken) and `good` (working)** to define the search range
- **`git bisect run <script>`** automates the entire hunt — perfect for CI reproducers
- **`git bisect visualize`** shows remaining candidates in gitk or text
- **Always run `git bisect reset`** when done to restore your original HEAD

---

**Next: [20-hooks.md](20-hooks.md)**
