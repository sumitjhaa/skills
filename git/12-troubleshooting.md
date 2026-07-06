# 🔧 Troubleshooting — "X Happened, Now What?"

> **TL;DR** Quick fixes for the 10 most common Git disasters.

---

## 💥 Problems & Fixes

| # | Problem | Fix |
|---|---------|-----|
| 1 | Wrong commit message | `git commit --amend` |
| 2 | Forgot files in commit | `git add . && git commit --amend --no-edit` |
| 3 | Committed on main instead of branch | `git branch feat && git reset --hard HEAD~1 && git switch feat` |
| 4 | Need to undo a pushed commit | `git revert hash` (safe) |
| 5 | Merge conflict | Find `<<<<<<<` markers, fix, `git add`, `git commit` |
| 6 | Detached HEAD | `git switch -c new-branch` |
| 7 | Lost commits | `git reflog` → find hash → `git branch rescue hash` |
| 8 | Push rejected | `git pull --rebase` then push again |
| 9 | File won't stop appearing | Add to `.gitignore`. If tracked: `git rm --cached file` |
| 10 | SSH permission denied | `ssh-keygen -t ed25519`, add pub key to GitHub |

| Panic | Emergency Exit |
|-------|---------------|
| Merge going wrong | `git merge --abort` |
| Rebase going wrong | `git rebase --abort` |
| Everything broken | `git reflog` then `git reset --hard hash` |
