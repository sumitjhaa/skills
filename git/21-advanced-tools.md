# 21️⃣ ADVANCED TOOLS — BLAME, GREP, DESCRIBE & MORE

⏱️ **Time:** ~12 min | 🏁 **TL;DR:** `git blame` → who touched each line. `git grep` → search tracked files. `git describe` → version name from tags. `git notes`/`git replace` → annotate without changing. `git bugreport`/`git check-attr` → debug. Custom aliases → your own commands.

## 🔁 LAST TIME...

In [20-hooks.md](20-hooks.md), you learned to automate with git hooks.

---

### `git blame` — Who Knows This Code?

```bash
git blame -L 10,20 app.js       # Only lines 10-20
git blame -w app.js             # Ignore whitespace changes
git blame -e app.js             # Show email instead of name
git blame -C app.js             # Detect lines moved from other files
```

💡 Blame is about **context**, not blame. "Who should review my change?"

### `git grep` — Search Tracked Files

```bash
git grep "TODO" -- "*.js" "*.ts"   # Filter by file type
git grep -c "searchTerm"           # Count per file
git grep -l "TODO" | xargs git grep -l "FIXME"  # AND search
```

### `git describe` — Human-Readable Version Names

```bash
git describe --tags --always
# → v1.0.0-5-gabc1234  (tag, commits since, abbreviated hash)
```

### `git notes` / `git replace`

```bash
git notes add abc123 -m "Introduced a known bug"  # Annotate commit
git replace abc123 def456                          # Swap objects
```

### `git bugreport` / `git check-attr`

```bash
git bugreport                         # Generate debug info for bug reports
git check-attr --all app.js           # Check gitattributes rules
```

### Custom Git Aliases

```bash
git config --global alias.tree "log --oneline --graph --all --decorate"
git config --global alias.pushf "push --force-with-lease"
git config --global alias.amend "commit --amend --no-edit"
```

👉 **Mnemonic:** Blame = "Who knows this code?" Describe = "Name this commit in human language." Aliases = "Your personal git commands."

---

### More Tools

```bash
git check-mailmap <email>          # Check how mailmap resolves an email
git column -c mode=dense           # Format git output in columns (scripting)
```

---

## 🧠 KEY TAKEAWAYS

- **`git blame -L range -w -C`** pinpoints who changed specific lines, ignoring whitespace and following code moves
- **`git grep`** searches only tracked files (not node_modules) — faster than system grep
- **`git describe`** creates a unique human-readable version string from the nearest tag
- **`git notes`** annotates commits without changing the commit hash
- **Custom aliases** turn complex pipelines into simple commands (`git tree`, `git pushf`)

---

**Next: [22-filter-repo.md](22-filter-repo.md)**
