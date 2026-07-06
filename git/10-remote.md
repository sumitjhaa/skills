# 🔟 REMOTE REPOSITORIES

⏱️ **Time:** ~15 min | 🏁 **TL;DR:** `git push -u origin HEAD` sets upstream. `git pull --rebase` keeps history clean. `--force-with-lease` is safe; `--force` is dangerous.

## 🔁 LAST TIME...

In [09-merge.md](09-merge.md), you learned merging and conflict resolution. **Today:** Share your code.

## `git clone` — Download a Remote

```bash
git clone <url>                          # Full history, all branches
git clone --depth 1 <url>                # Shallow (latest commit only)
git clone --branch feat --single-branch  # One branch only
git clone --bare <url>                   # Server clone (no working files)
```

## `git push` — Send Changes Up

```bash
git push -u origin HEAD          # Push + set upstream (do once, then just git push)
git push --force-with-lease      # Safe force push (checks remote hasn't changed)
git push --force                 # DANGEROUS — blindly overwrites
git push --dry-run               # Preview what would push
```

👉 **Mnemonic:** `--force-with-lease` = **"Force, but check the lease first."**

## `git pull` — Get Remote Changes

```bash
git pull --rebase                # Fetch + rebase (linear history)
git pull --ff-only               # Only if fast-forward possible
git pull --autostash             # Stash uncommitted work, pull, unstash
```

💡 `git config --global pull.rebase true && git config --global pull.ff only`

## `git fetch` — Peek Without Merging

```bash
git fetch                        # Download remote data (no merge)
git fetch --prune                # Also delete stale remote-tracking branches
```

## `git remote` — Managing Remotes

```bash
git remote -v                    # List remotes with URLs
git remote add upstream <url>    # Add upstream remote (forks)
```

## SSH & PAT Setup

```bash
ssh-keygen -t ed25519 -C "your@email.com"   # Generate key pair
cat ~/.ssh/id_ed25519.pub                    # Copy → GitHub Settings → SSH keys
ssh -T git@github.com                        # Test: "Hi you! You've authenticated."

# PAT: GitHub → Settings → Developer settings → Personal access tokens
# Use token as password for HTTPS auth
```

## 🧠 KEY TAKEAWAYS

- **`git push -u origin HEAD`** sets upstream once; after that just `git push`
- **`--force-with-lease`** checks remote hashes; never use bare `--force`
- **`git pull --rebase`** keeps history linear (set as global default)
- **`git fetch`** peeks; **`git pull`** peeks + merges
- **SSH keys or PAT** required to authenticate with GitHub

**Next: [11-collaboration.md](11-collaboration.md)** — Fork, PR, and team workflows
