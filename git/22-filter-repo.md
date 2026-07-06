# 22️⃣ FILTER-REPO — REWRITE HISTORY

⏱️ **Time:** ~8 min | 🏁 **TL;DR:** `git filter-repo` rewrites history to remove secrets, files, or strings from ALL commits. Fast and safe. ⚠️ Only for repos you own — it changes every commit hash.

## 🔁 LAST TIME...

In [21-advanced-tools.md](21-advanced-tools.md), you learned blame, grep, describe, and custom aliases.

---

### Old Way: `git filter-branch` (Slow)

```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
```

### Modern Way: `git filter-repo` (Fast)

```bash
# Install: pip install git-filter-repo

# Remove a file from ALL history:
git filter-repo --path .env --invert-paths

# Remove a folder:
git filter-repo --path node_modules --invert-paths

# Replace a string across all commits:
git filter-repo --replace-text <(echo "OLD_API_KEY==>REPLACED")

# Change author email:
git filter-repo --email-callback \
  'return b"new@email.com" if b"old@email.com" else email'
```

### Alternative: fast-export + fast-import (Repo Migration)

```bash
# Export entire repo to a text stream
git fast-export --all > repo.export

# Import into a new repo (preserves all history)
cd /path/to/new-repo
git fast-import < ../repo.export

# Useful for: splitting repos, rewriting authors,
# changing commit metadata programmatically
```

### After Filtering: Force Push

```bash
git push origin --force --all
```

⚠️ **Only run on repos you own.** Every commit hash changes. Collaborators must re-clone.

👉 **Mnemonic:** filter-repo = "Go back in time and change history." `--invert-paths` = "Remove everything EXCEPT this path."

---

## 🧠 KEY TAKEAWAYS

- **`git filter-repo`** is the modern, fast replacement for `git filter-branch`
- **Remove files from all history** with `--path <file> --invert-paths`
- **Replace strings** across all commits with `--replace-text`
- **After rewriting, force push** — every commit hash has changed
- ⚠️ **Only for repos you own** — collaborators must re-clone after the rewrite

---

**Next: [23-maintenance.md](23-maintenance.md)**
