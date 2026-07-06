# 3️⃣ THE CORE LOOP — ADD, COMMIT, STATUS

---

⏱️ **Time:** ~15 min | 🏁 **TL;DR:** `git add` stages changes, `git commit` saves them, `git status` checks state.

---

## 🔁 LAST TIME...

In [02-init.md](02-init.md), you created your first repo with `git init` and made your first commit.

---

## 📦 THE THREE STATES

```
📝 WORKING DIRECTORY  ── git add ──→  📦 STAGING AREA  ── git commit ──→  💾 REPOSITORY
```

👉 **Mnemonic:** **W**orking → **S**taging → **R**epository = **We Save Records**

---

## 🔍 git status — Your Dashboard

```bash
git status        # Full verbose output
git status -s     # Short (ADHD-friendly)
```

```
# Short status symbols:
  M app.js        # Modified but NOT staged
 M  app.js        # Modified AND staged
 ?? new-file.js   # Untracked
 A  new.js        # Added (staged)
 D  old.js        # Deleted (staged)
```

💡 **Run `git status` after every command. It's your safety net.**

---

## ➕ git add — The Staging Area

```bash
git add app.js              # Stage ONE file
git add .                   # Stage ALL changes in current dir
git add -A                  # Stage ALL changes everywhere
git add -p                  # Stage interactively (pick hunks)
```

⚠️ **`git add .` is the #1 cause of accidental commits. Always `git status` first.**

---

## 💾 git commit — Taking the Snapshot

```bash
git commit -m "feat: add login"         # One-liner commit
git commit -am "fix: correct typo"      # Add + commit tracked files (skip git add)
git commit --amend -m "better msg"      # Fix last commit message
git add forgotten.js && git commit --amend --no-edit   # Add files to last commit
```

👉 **Mnemonic for `-am`:** "**A**dd + **M**essage = **A**ll-in-one **M**agic"

---

## 🧠 KEY TAKEAWAYS

- **Three states:** Working → Staging → Repository — you must `add` then `commit`
- **`git status -s`** is the fastest way to see what's happening
- **`git add -p`** prevents accidental commits by letting you review each change
- **`git commit --amend`** fixes the last commit (don't use on shared branches)
- **Run `git status`** before and after every command

---

> **Next: [04-log.md](04-log.md) — Reading history with git log**
