# 📂 Undo

> **TL;DR** Git gives you undo at every level — like Ctrl+Z for your whole project.

---

**📖 Story:** You spilled coffee on your work — git lets you un-spill at the file, stage, commit, or shared-history level.

**👀 Visual:**
```text
Three levels of reset:

--soft:  HEAD moves, stage+workdir kept
--mixed: HEAD moves, stage resets, workdir kept (default)
--hard:  HEAD moves, stage resets, workdir wiped

Revert (safe for shared repos):
Before: ●──●──●──●──●
                    ↑ HEAD
After:  ●──●──●──●──●──●
                        ↑ new undo commit
```

**🛠️ Reference:**
| Situation | Command | Safety |
|-----------|---------|--------|
| Undo changes in a file | `git restore file` | ⚠️ Loses edits |
| Unstage a file | `git restore --staged file` | ✅ Safe |
| Undo last commit, keep changes | `git reset --soft HEAD~1` | ✅ Safe |
| Undo last commit, lose changes | `git reset --hard HEAD~1` | ☠️ Loses work |
| Undo a shared commit | `git revert hash` | ✅ Safe |
| Delete untracked files | `git clean -fd` | ☠️ Deletes files |

**🧪 Try:**
```
echo oops > test.txt && git commit -am "bad commit"
git reset --soft HEAD~1   # undo commit, keep changes
git restore test.txt       # discard file changes
```

**⚠️ Watch out:** Never `reset --hard` or `clean` if you're not 100% sure — those delete work permanently. Use `revert` for commits others have seen.

**➡️ Next:** 09-intermediate.md
