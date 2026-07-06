# 13️⃣ STASHING & TIDYING

⏱️ **Time:** ~10 min | 🏁 **TL;DR:** `git stash` shelves dirty work so you can switch branches. `git stash pop` brings it back. `git stash list` shows your shelf.

## 🔁 LAST TIME...

In [12-undo.md](12-undo.md) — `git restore`, `git reset`, `git revert`, `git clean`.

---

### `git stash` Basics

```bash
git stash push -m "WIP: login validation"     # Save with message
git stash list                                 # stash@{0}: On feat/login: …
git stash pop                                  # Apply + remove from list
git stash apply                                # Apply + keep in list
git stash drop stash@{2}                      # Delete specific stash
git stash clear                                # ⚠️ Delete ALL stashes
```

### Advanced Options

```bash
git stash --patch              # Pick specific hunks to stash
git stash --keep-index         # Stash only unstaged work
git stash -u                   # Include untracked files
git stash --all                # Stash everything (incl. ignored)
```

### `git stash branch`

```bash
git stash branch new-feature   # Creates branch, applies stash, drops entry
```

### Stash Conflicts

**`git stash pop` keeps the stash if there's a conflict.** Drop it manually.

```bash
git stash pop          # → CONFLICT!
# Fix markers → git add <file> → git stash drop
```

---

## 👉 MNEMONIC — **"Stash = shelf. `pop` = take off. `drop` = throw away. Conflict? Stash stays — drop it manually."**

## 🧠 KEY TAKEAWAYS

- **`git stash` before switching branches** with dirty work — saves everything
- **`git stash pop`** applies + removes; **`git stash apply`** keeps it in list
- **`git stash push -m "message"`** makes stashes findable later
- **`git stash branch`** turns stashed work into a real branch
- **Conflict on `pop`?** Stash is NOT dropped — fix then `git stash drop`

---

> **Next: [14-rebase.md](14-rebase.md) — Rebasing & rewriting history**
