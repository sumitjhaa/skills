# 6️⃣ IGNORE — KEEPING JUNK OUT

---

⏱️ **Time:** ~5 min | 🏁 **TL;DR:** `.gitignore` patterns tell git which files to never track. `git check-ignore -v` debugs which rule matched.

---

## 🔁 LAST TIME...

In [05-diff.md](05-diff.md), you compared changes with `git diff` and `git show`.

---

## 📄 .gitignore Patterns

```gitignore
# Ignore specific files and directories
secrets.env
node_modules/
build/
dist/

# Ignore by extension
*.log
*.tmp

# Ignore all .env files EXCEPT the example
.env
!.env.example

# Ignore files in any directory named 'temp'
temp/

# Ignore only at root (not subdirectories)
/build/
```

Generate a starter `.gitignore`: https://www.toptal.com/developers/gitignore

---

## 🔍 Debugging Ignored Files

```bash
git check-ignore secret.env         # Silent → not ignored
git check-ignore -v secret.env      # Shows WHICH rule matched
# → .gitignore:5:*.env  secret.env
```

---

## 🙈 Pretend a File Doesn't Exist (Local Only)

```bash
git update-index --assume-unchanged config.local.js
# Git stops tracking changes in this file

# Undo:
git update-index --no-assume-unchanged config.local.js
```

⚠️ **`--assume-unchanged` is LOCAL only — doesn't push/pull.**

👉 **Mnemonic:** "`.gitignore` for everyone, `--assume-unchanged` for just you"

---

## 🧠 KEY TAKEAWAYS

- **`.gitignore`** keeps build artifacts, secrets, and dependencies out of version control
- Use **`!`** to un-ignore specific files within an ignored pattern (e.g., `!.env.example`)
- **`git check-ignore -v`** tells you exactly which rule is blocking a file
- **`git update-index --assume-unchanged`** hides local changes from a tracked file
- Commit `.gitignore` to the repo so everyone benefits

---

> **Next: [07-rm-mv.md](07-rm-mv.md) — Removing and renaming files**
