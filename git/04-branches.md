# 📂 Branches

> **TL;DR** Branches let you work on multiple versions of your code at the same time.

---

**📖 Story:** Branches are alternate realities — what if you explored a new feature without messing up the main timeline?

**👀 Visual:**
```text
main:  ●──●──●
            \
feature      ●──●──●  ← HEAD (you are here)
```

**🛠️ Commands:**
| Do This | What Happens |
|---------|-------------|
| `git branch` | List branches (* = current) |
| `git branch name` | Create a new branch |
| `git branch -d name` | Delete a merged branch |
| `git switch name` | Move HEAD to that branch |
| `git switch -c name` | Create + switch in one step |
| `git checkout name` | Old way to switch (still works) |
| `git checkout -b name` | Old way to create + switch |

**🧪 Try:**
```
git branch
git switch -c my-experiment
git branch
```

**⚠️ Watch out:** Detached HEAD = you checked out a commit instead of a branch. Fix with `git switch -c any-branch-name`.

**➡️ Next:** 05-merging.md
