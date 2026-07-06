# 9️⃣ MERGING & CONFLICTS

⏱️ **Time:** ~15 min | 🏁 **TL;DR:** `git merge name` combines branches. Conflicts show `<<<<<<<` markers — fix file, `git add`, `git commit`. Detached HEAD = orphan commits unless rescued.

## 🔁 LAST TIME...

In [08-branch.md](08-branch.md), you learned `git switch` and `git branch`. **Today:** Combining timelines.

## `git merge` — Joining Timelines

```bash
git switch main            # Go to receiving branch
git merge feat/login       # Merge feat INTO main (fast-forward if possible)
git merge --no-ff feat     # Force merge commit (preserves branch visual)
git merge --squash feat    # Squash into 1 commit
```

👉 **Mnemonic:** Merge = **"Weaving two timelines into one."**

## Merge Conflict Flow (4 Steps)

```bash
# Step 1: See what's conflicted
git status                # → both modified: index.html

# Step 2: Open file — find markers and edit
# <<<<<<< HEAD   ← YOUR version
# <title>My Site</title>
# =======
# <title>My Awesome Site</title>  ← THEIR version
# >>>>>>> feat
# Keep what you want, REMOVE markers and separators

# Step 3: Stage the resolved file
git add index.html

# Step 4: Complete the merge
git commit -m "merge: resolve conflict"
```

### Quick Options

```bash
git checkout --ours file.js    # Keep YOUR version
git checkout --theirs file.js  # Keep THEIR version
git merge --abort              # Cancel merge entirely
```

## Detached HEAD — Danger & Rescue

👉 **Mnemonic:** Detached HEAD = **"Ghost commits with no branch to haunt."**

```bash
# How you get in: checkout a commit hash, not a branch
git checkout abc1234

# Rescue: create a branch before switching away
git switch -c rescued-feature   # ✅ Commit is now safe on a branch
```

Also useful: `git mergetool` for visual conflict resolution, `git difftool --dir-diff` for side-by-side directory comparison, `git merge-file` to merge individual files outside a merge context, and `git rerere` to auto-resolve repeat conflicts.

## 🧠 KEY TAKEAWAYS

- **`--no-ff`** preserves branch history; **`--squash`** collapses into one commit
- **Conflict resolution:** 4 steps — `status` → fix `<<<<<` markers → `git add` → `git commit`
- **`--ours`** = your branch; **`--theirs`** = branch being merged in
- **`git merge --abort`** cancels the merge entirely
- **Detached HEAD + uncommitted work** → `git switch -c name` immediately

**Next: [10-remote.md](10-remote.md)** — Remote repositories
