# 5️⃣ DIFF & SHOW — COMPARING CHANGES

---

⏱️ **Time:** ~10 min | 🏁 **TL;DR:** `git diff` before committing catches mistakes. `git show` views any commit or file.

---

## 🔁 LAST TIME...

In [04-log.md](04-log.md), you learned to read history with `git log --oneline --graph --all`.

---

## 📊 git diff — See Changes Before Committing

```bash
git diff                   # Unstaged changes (working vs staging)
git diff --staged          # Staged changes (staging vs last commit)
git diff HEAD              # All uncommitted changes (staged + unstaged)
git diff --word-diff       # Word-level (better for long lines)
git diff --stat            # Files + insertions/deletions stats
git diff --name-only       # Only filenames
```

💡 **Always `git diff` before `git commit` — catches 90% of mistakes.**

---

## 🔄 Branch Comparison

```bash
git diff main..feat            # Diff between branch tips
git diff main...feat           # Diff from where feat branched off main
git diff main feat -- app.js   # Diff of ONE file between branches
git diff HEAD~3..HEAD          # Last 3 commits worth of changes
```

- `..` = compare the tips of two branches
- `...` = compare where they diverged (merge-base)

---

## 🔍 git show — Swiss Army Knife

```bash
git show                          # Show latest commit (full diff)
git show abc1234                  # Show a specific commit
git show --stat abc1234           # Show only file stats
git show abc1234:path/to/file.js  # Show file as it was in that commit
git show --staged                 # Show staged changes
git show v1.0.0                   # Show a tag
```

👉 **Mnemonic:** "`git show` shows ANYTHING git knows — commits, files, tags"

---

## 🧠 KEY TAKEAWAYS

- **`git diff`** shows unstaged changes; **`git diff --staged`** shows what'll commit
- **`--word-diff`** is essential for long lines or prose
- Use **`..`** to compare branch tips, **`...`** to compare from merge-base
- **`git show`** can view any commit, file-at-commit, or tag
- Always **`git diff`** before committing to catch accidental changes

---

> **Next: [06-ignore.md](06-ignore.md) — Keeping junk out with .gitignore**
