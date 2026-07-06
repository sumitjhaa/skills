# 15️⃣ CHERRY-PICK — STEAL COMMITS

⏱️ **Time:** ~10 min | 🏁 **TL;DR:** `git cherry-pick` applies a specific commit to your current branch. `git range-diff` compares commit ranges. `git shortlog` groups commits by author. `git merge-base` finds the common ancestor of two branches.

## 🔁 LAST TIME...

In [14-rebase.md](14-rebase.md), you learned to replay commits on a new base with `git rebase`.

---

### `git cherry-pick` — Steal Commits

```bash
git cherry-pick abc1234              # Apply specific commit
git cherry-pick abc123..def456       # Apply range
git cherry-pick -n abc123            # No auto-commit (edit first)
git cherry-pick -x abc123            # Add source note in message
```

### `git range-diff` — Compare After Rebase

```bash
git tag old-position
git rebase -i HEAD~5
git range-diff old-position HEAD     # What changed during rebase
```

### `git shortlog` — Release Notes

```bash
git shortlog                          # Grouped by author
git shortlog -sn                      # Just counts
git shortlog v1.0.0..HEAD --no-merges # Changelog
```

### `git merge-base` — Common Ancestor

```bash
git merge-base main feat              # Where feat branched off
git diff main...feat                  # Diff from merge-base to feat
```

👉 **Mnemonic:** Cherry-pick = "Pick the cherry (commit) from another tree (branch)." Range-diff = "What changed between then and now?"

---

## 🧠 KEY TAKEAWAYS

- **`cherry-pick`** applies any commit to your current branch
- **`range-diff`** verifies nothing broke after rebasing
- **`shortlog`** generates release notes grouped by author
- **`merge-base`** finds the common ancestor between two branches

---

**Next: [16-tag.md](16-tag.md)**
