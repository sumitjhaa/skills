# 12️⃣ UNDOING & FIXING MISTAKES

⏱️ **Time:** ~15 min | 🏁 **TL;DR:** `git restore --staged` = unstage. `git restore` = discard (⚠️ permanent). `git revert` = safe undo for shared branches. `git reset --hard` = nuke (local only).

## 🔁 LAST TIME...
In [11-collaboration.md](11-collaboration.md) — fork workflows, conventional commits, `gh pr create`, email patches.

---

### Undo Decision Tree
```
What to undo?       → Command
Unstage a file      → git restore --staged file
Discard changes     → git restore file (⚠️ PERMANENT)
Fix last commit     → git commit --amend
Remove commits      → git reset HEAD~1 (local) / git revert (shared)
Delete untracked    → git clean -i
```

### `git restore`
```bash
git restore --staged file.js     # Unstage (keep changes)
git restore file.js              # Discard (⚠️ no recovery)
git restore --source HEAD~2 f.js # From 2 commits ago
```

### `git reset` — Rewinding Time
| Mode | Working Dir | Staging | History |
|---|---|---|---|
| `--soft` | unchanged | unchanged | rewound |
| `--mixed` | unchanged | RESET | rewound |
| `--hard` | RESET | RESET | rewound |

### `git revert` — Safe Undo (Shared)
```bash
git revert abc123        # Creates inverse commit — history preserved
```
👉 **`reset` = rewrites history (YOUR branches). `revert` = adds undo commit (SAFE for shared).**

### `git clean` — Remove Untracked
```bash
git clean -n    # Dry run (show, don't delete)
git clean -i    # Interactive (choose files)
git clean -fd   # Delete untracked files + dirs
```

---

## 👉 MNEMONIC — **"restore --staged = unstage me. revert = safe undo for sharing. clean -n first, always."**

## 🧠 KEY TAKEAWAYS
- **`git restore --staged`** unstage safely; changes stay on disk
- **`git revert` for shared branches** — adds undo commit, history intact
- **`git reset --hard` is DESTRUCTIVE** — local branches only
- **`git clean -n` first** — dry run before deleting untracked files
- **`git reflog` rescues everything** — even after accidental `reset --hard`

---

> **Next: [13-stash.md](13-stash.md) — Stashing work**
