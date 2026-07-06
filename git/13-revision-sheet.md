# 📋 Revision Sheet — EVERYTHING at a Glance

> **TL;DR** Print this. Pin it. Use it daily.

---

## 🚀 Quick Start (New Project)

```
git init
git add .
git commit -m "initial"
git branch -M main
git remote add origin <url>
git push -u origin main
```

## 📥 Getting a Repo

| Command | What It Does |
|---------|-------------|
| `git init` | Create new empty repo |
| `git clone url` | Download remote repo locally |

## 📝 Daily Work

| Command | What It Does |
|---------|-------------|
| `git status` | What's changed? |
| `git add file` | Stage file |
| `git add .` | Stage all changes |
| `git commit -m "msg"` | Commit staged |
| `git commit --amend` | Fix last commit |
| `git diff` | See unstaged changes |
| `git log --oneline --graph` | See history visually |

## 🌿 Branches

| Command | What It Does |
|---------|-------------|
| `git branch` | List branches |
| `git branch name` | Create branch |
| `git switch name` | Switch to branch |
| `git switch -c name` | Create + switch |
| `git branch -d name` | Delete branch (safe) |
| `git branch -D name` | Force delete branch |
| `git merge name` | Merge branch into current |

## ⏪ Undo

| Situation | Command |
|-----------|---------|
| Discard file changes | `git restore file` |
| Unstage file | `git restore --staged file` |
| Undo commit (keep) | `git reset --soft HEAD~1` |
| Undo commit (lose) | `git reset --hard HEAD~1` |
| Safe undo (pushed) | `git revert hash` |
| Discard untracked | `git clean -fd` |

## ☁️ Remotes

| Command | What It Does |
|---------|-------------|
| `git remote -v` | Show remotes |
| `git fetch` | Download remote (no merge) |
| `git pull` | Fetch + merge |
| `git push` | Upload commits |
| `git push -u origin branch` | Upload + set upstream |
| `git push --force-with-lease` | Force push (safer) |

## 📦 Stash

| Command | What It Does |
|---------|-------------|
| `git stash` | Save changes aside |
| `git stash pop` | Restore + delete stash |
| `git stash list` | See all stashes |
| `git stash apply` | Restore (keep stash) |
| `git stash branch name` | Make branch from stash |

## 🔬 Advanced Tools

| Command | What It Does |
|---------|-------------|
| `git rebase -i HEAD~N` | Edit N commits interactively |
| `git cherry-pick hash` | Apply a specific commit here |
| `git bisect start` | Binary search to find bug commit |
| `git reflog` | View all HEAD movements (safety net) |
| `git tag -a v1.0 -m "msg"` | Tag current commit with version |
| `git worktree add path branch` | Checkout branch in another directory |

## ☠️ DANGEROUS Commands (use with care)

- `git reset --hard` — deletes uncommitted work permanently
- `git push --force` — overwrites remote history (use `--force-with-lease`)
- `git clean -fd` — deletes untracked files irreversibly
- `git branch -D name` — deletes unmerged branch for good

## 🧠 Mental Model

```
Working Dir ──add──▶ Stage ──commit──▶ Repo
    │                    │                  │
    │ restore            │ restore --staged │ reset / revert
    ▼                    ▼                  ▼
 discard              unstage            rewind / undo
```
