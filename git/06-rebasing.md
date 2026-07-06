# 📂 Rebasing

> **TL;DR** Rebasing replays your commits on top of another branch for a cleaner, linear history.

---

**📖 Story:** Time machine — take your commits and reapply them as if they started from a newer point.

**👀 Visual:**
```text
MERGE:  ●──●──●──────●  (extra merge commit)
            \      /
             ●──●──●

REBASE: ●──●──●──●──●──●  (linear, no merge bubble)
```

**🛠️ Commands:**
| Do This | What Happens |
|---------|-------------|
| `git rebase main` | Replay current branch's commits on top of main |
| `git rebase --onto newbase oldbase topic` | Move a branch to a totally different base |
| `git rebase --continue` | After fixing a conflict, continue rebasing |
| `git rebase --abort` | Panic button — undo the entire rebase |

**🧪 Try:**
```
git switch feature
git rebase main
```

**⚠️ Watch out:** **NEVER rebase commits that others have already pulled.** You rewrite history — it breaks everyone else's clone. Conflict fix: edit → `git add` → `git rebase --continue`.

**➡️ Next:** 07-remotes.md
