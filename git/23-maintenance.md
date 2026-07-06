# 23️⃣ MAINTENANCE — GC, WORKTREE, SUBMODULE

⏱️ **Time:** ~12 min | 🏁 **TL;DR:** `git gc`/`git maintenance` → optimize. `git fsck`/`git prune` → check health. `git bundle` → transfer offline. `git archive` → export without `.git`. `git sparse-checkout` → partial clone. `git worktree` → multi-branch. `git submodule` → repo in repo.

## 🔁 LAST TIME...

In [22-filter-repo.md](22-filter-repo.md), you learned to rewrite history with filter-repo.

---

### Housekeeping: gc, fsck, prune, repack, commit-graph

```bash
git gc --aggressive                 # Compress & optimize
git maintenance start               # Auto-optimize (Git 2.30+)
git fsck --lost-found               # Check integrity, find dangling commits
git prune --dry-run                 # Remove dangling objects (preview)
git count-objects -v                # Show object count & disk usage
git repack -ad                      # Repack all objects into packs (faster clones)
git commit-graph write              # Build commit graph (speeds up log/branch)
git multi-pack-index write          # Optimize multi-pack index (large repos)
```

### Transport: bundle & archive

```bash
git bundle create repo.bundle --all # Full repo → single file (USB/email)
git clone repo.bundle new-repo      # Clone from file, no network
git archive --format=zip HEAD > project.zip  # Export without .git
```

### Partial Checkout: sparse-checkout

```bash
git sparse-checkout init --cone
git sparse-checkout set packages/my-app src/shared  # Only these folders
git sparse-checkout add docs                         # Add more folders
git sparse-checkout disable                          # Restore full checkout
```

### Multi-Branch: worktree

```bash
git worktree add ../project-hotfix hotfix/critical   # Two branches at once
git worktree list                                    # List all worktrees
git worktree remove ../project-hotfix                # Remove worktree
```

### Submodule Basics & Verification

```bash
git submodule add https://github.com/user/library.git lib/
git clone --recursive <url>                          # Clone with submodules
git submodule update --init --recursive              # Update after pull
git verify-commit abc123                             # Verify GPG signature
git instaweb                                         # Browse repo in browser
```

👉 **Mnemonic:** gc = "Take out the trash." fsck = "Doctor, check my repo." Bundle = "Git via USB stick." Sparse = "Only download what you need." Worktree = "Two branches at once."

---

## 🧠 KEY TAKEAWAYS

- **`git maintenance start`** runs auto-optimization in the background (Git 2.30+)
- **`git fsck --lost-found`** finds dangling commits you can still recover
- **`git bundle`** transfers a full repo via file — no network required
- **`git sparse-checkout`** lets you work with only part of a monorepo on disk
- **`git worktree`** enables simultaneous work on multiple branches from the same repo

---

**Next: [24-pro.md](24-pro.md)**
