# 📂 Merging

> **TL;DR** Merging weaves two branch timelines back together into one.

---

**📖 Story:** Two developers worked in parallel — merging is how you combine their work into a single truth.

**👀 Visual:**
```text
Fast-forward (linear catch-up):
main:  ●──●──●──●──●  (just catches up to feature)

3-way merge (divergent histories):
main:  ●──●──●─────●  (merge commit with 2 parents)
            \       /
feature      ●──●──●
```

**🛠️ Commands:**
| Do This | What Happens |
|---------|-------------|
| `git merge feature` | Merge feature into current branch |
| `git merge --no-ff feature` | Force a merge commit (no fast-forward) |

**🧪 Try:**
```
git switch main
git merge my-experiment
```

**⚠️ Watch out:** Conflicts show `<<<<<<<`, `=======`, `>>>>>>>` markers. Fix the file, then `git add file` + `git commit`. Panic? `git merge --abort` undoes everything.

**➡️ Next:** 06-rebasing.md
