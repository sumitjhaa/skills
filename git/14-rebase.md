# 14️⃣ REBASE — REPLAY HISTORY ON A NEW BASE

⏱️ **Time:** ~15 min | 🏁 **TL;DR:** `git rebase` replays your branch commits on top of another branch for clean linear history. Interactive rebase (`-i`) lets you squash, reword, reorder, or drop commits.

## 🔁 LAST TIME...

In [13-stash.md](13-stash.md), you learned to shelve work with `git stash`.

---

### `git rebase main` — The Basics

```bash
git switch feat
git rebase main         # Replay feat's commits after main's tip
```

### Interactive Rebase

```bash
git rebase -i HEAD~3    # Pick, reword, edit, squash, fixup, drop, exec
```

| Command | Effect |
|---------|--------|
| `pick` | Keep commit as-is |
| `reword` | Change commit message |
| `edit` | Stop to edit files |
| `squash` | Merge with previous |
| `fixup` | Merge, discard message |
| `drop` | Delete commit |
| `exec` | Run shell command |

### `git rebase --onto` — The Power Tool

```bash
# Cut <branch> off at <upstream>, paste onto <target>
git rebase --onto main release feat
```

### `--autosquash` & `--exec`

```bash
git commit --fixup HEAD            # Create fixup! commit
git rebase -i --autosquash HEAD~3  # Auto-order fixups
git rebase -i --exec "npm test"    # Test each commit
```

### Safety Nets

```bash
git rebase --abort     # Cancel rebase
git rebase --continue  # Continue after resolving conflicts
git rebase --skip      # Skip problematic commit
```

👉 **Mnemonic:** Rebase = "Replay my commits on top of yours." `--onto` = "Cut from X, paste onto Y."

---

## 🧠 KEY TAKEAWAYS

- **Rebase = replay commits on a new base** — creates linear history
- **Never rebase commits others have pulled** — you rewrite their history
- **`rebase --onto`** cuts from one base and pastes on another (most powerful git command)
- **`--autosquash`** auto-orders fixup commits during interactive rebase
- **Use `--abort`/`--continue`/`--skip`** to manage rebase safely

---

**Next: [15-cherry-pick.md](15-cherry-pick.md)**
