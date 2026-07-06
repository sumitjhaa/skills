# 7️⃣ RM & MV — REMOVING AND RENAMING

---

⏱️ **Time:** ~5 min | 🏁 **TL;DR:** `git rm` deletes + stages. `git mv` renames + stages. Always use these instead of raw `rm`/`mv`.

---

## 🔁 LAST TIME...

In [06-ignore.md](06-ignore.md), you learned to exclude junk with `.gitignore` and `--assume-unchanged`.

---

## 🗑️ git rm — Delete + Stage

```bash
git rm old-file.js              # Delete file AND stage the deletion
git rm --cached config.js       # Remove from git BUT keep on disk
git rm -r old-folder/           # Remove a directory
git rm -n old-file.js           # Dry run (show what WOULD be removed)
```

💡 **Always use `git rm` instead of `rm` — it stages the deletion automatically.**

`git rm --cached` is useful when you accidentally committed a file that should be in `.gitignore`.

---

## ✏️ git mv — Rename + Stage

```bash
git mv old-name.js new-name.js   # Rename AND stage in one command
```

Same as the manual approach:

```bash
mv old-name.js new-name.js       # Rename on disk
git add -A                       # Git detects the rename by content
```

📌 **Git detects renames automatically (by content similarity), but `git mv` makes it explicit.**

👉 **Mnemonic:** "`rm` removes + stages, `mv` renames + stages — git does both steps for you"

---

## 🧠 KEY TAKEAWAYS

- **`git rm`** removes a file and stages the deletion in one step
- **`git rm --cached`** untracks a file but keeps your local copy
- **`git mv`** renames a file and stages the rename
- Both commands save you from the two-step manual process
- Git auto-detects renames via content similarity — `git mv` is explicit but not required

---

> **Next: [08-branch.md](08-branch.md) — Parallel universes with branches**
