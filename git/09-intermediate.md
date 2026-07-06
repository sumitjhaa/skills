# 📂 Intermediate Moves

> **TL;DR** Seven power tools that solve real messes.

---

**📖 Story:** Your commits are a disaster, you need a commit from another branch, and you lost something — these tools fix all of it.
**👀 Visual:**
```text
Interactive Rebase (clean history):
Before: ●──●──●──●──● (5 messy)
After:  ●──●─────●    (3 clean, squashed)

Cherry-Pick (grab one commit):
main    ●──●──●
                  \
feature       ●──● ← picked from elsewhere
```

## Stash — save dirty work aside
**🛠️ Commands:**
| Do This | What Happens |
|---------|-------------|
| `git stash` | Save current changes (files go clean) |
| `git stash pop` | Restore most recent stash |
| `git stash list` | Show all stashes |
| `git stash branch name` | Create branch from a stash |

## Interactive Rebase — rewrite history
**🛠️ Commands:**
| Do This | What Happens |
|---------|-------------|
| `git rebase -i HEAD~N` | Edit last N commits |
| `pick` | Keep commit as-is |
| `reword` | Change commit message |
| `squash` | Combine with previous commit |
| `fixup` | Combine + discard message |
| `drop` | Delete commit |

## Cherry-Pick — grab one commit
**🛠️ Commands:**
| Do This | What Happens |
|---------|-------------|
| `git cherry-pick hash` | Apply that commit here |
| `git cherry-pick hash1 hash2` | Apply multiple |

## Bisect — find the bug
**🛠️ Commands:**
| Do This | What Happens |
|---------|-------------|
| `git bisect start` | Begin binary search |
| `git bisect good hash` | Mark known-good commit |
| `git bisect bad` | Mark current as bad |
| `git bisect run script` | Auto-find (script returns 0=good) |

## Reflog — safety net
**🛠️ Commands:**
| Do This | What Happens |
|---------|-------------|
| `git reflog` | Show EVERYTHING you've done |
| `git reset --hard HEAD@{2}` | Recover lost state |

## Tags — permanent bookmarks
**🛠️ Commands:**
| Do This | What Happens |
|---------|-------------|
| `git tag -a v1.0 -m "msg"` | Create annotated tag |
| `git push origin --tags` | Push all tags |

**🧪 Try:**
```
git stash && git stash pop    # save and restore work
git reflog                     # see your full history
```

**⚠️ Watch out:** Rebase rewrites history — never rebase commits pushed to a shared branch. Reflog expires after ~90 days.

**➡️ Next:** 10-advanced.md
