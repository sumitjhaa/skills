# 4️⃣ LOG — READING HISTORY

---

⏱️ **Time:** ~10 min | 🏁 **TL;DR:** `git log --oneline --graph --all` shows the full picture. Filter by time, author, file, or content.

---

## 🔁 LAST TIME...

In [03-core-loop.md](03-core-loop.md), you mastered the add-commit-status loop.

---

## 📜 BASIC LOG

```bash
git log                         # Full log
git log --oneline               # One line per commit
git log --oneline --graph --all # Visual tree (MOST USEFUL)
```

---

## 🎨 CUSTOM FORMAT

```bash
git log --format="%h %an %ar %s"
# abc123  Sumit  2 days ago  feat: add login
```

Key placeholders: `%h` (short hash), `%an` (author), `%ar` (relative date), `%s` (subject), `%d` (ref names).

---

## 🔍 FILTERS

```bash
# Time
git log --since="2024-01-01" --until="2024-06-01"
git log --after="2 weeks ago"

# Author
git log --author="Sumit"

# File
git log --oneline -- src/app.js              # Commits touching this file
git log --oneline --follow src/app.js        # Follow file renames

# Content (pickaxe)
git log -S "functionName" --oneline          # Added/removed this string

# Diff type
git log --diff-filter=A --oneline            # Only ADDED files
```

---

## 🏷️ SAVE AS ALIAS

```bash
git config --global alias.tree "log --oneline --graph --all --decorate"
git tree    # Your new superpower
```

👉 **Mnemonic:** "`git tree` = see the whole forest, not just the branches"

---

## 🧠 KEY TAKEAWAYS

- **`git log --oneline --graph --all`** is the single most useful git visualization
- Filter by **time**, **author**, **file** path, or **content** with `-S`
- **`--diff-filter`** finds commits that added/deleted/renamed specific files
- **Save `git tree` as an alias** — you'll use it dozens of times a day
- `--follow` tracks a file across renames

---

> **Next: [05-diff.md](05-diff.md) — Comparing changes with git diff**
