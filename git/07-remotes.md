# 📂 Remotes

> **TL;DR** Remotes sync your local repo with a server so you can collaborate (or back up your code).

---

**📖 Story:** Cloud sync for your code — a remote is the shared copy everyone pushes to and pulls from.

**👀 Visual:**
```text
Local: ●──●──●──●  ──push──▶  Remote: ●──●──●──●
Local: ●──●──●──●  ◀─pull────  Remote: ●──●──●──●
```

**🛠️ Commands:**
| Do This | What Happens |
|---------|-------------|
| `git remote -v` | List remotes and their URLs |
| `git remote add name url` | Add a new remote |
| `git fetch origin` | Download remote data (does NOT merge) |
| `git pull origin main` | Fetch + merge remote changes |
| `git push origin main` | Upload your commits to the remote |
| `git push -u origin main` | Push + set upstream (next time just `git push`) |
| `git fetch --prune` | Fetch + delete local refs to deleted remote branches |

**🧪 Try:**
```
git remote -v
git fetch --prune
```

**⚠️ Watch out:** If `git push` is rejected, someone else pushed first. Pull their changes, fix conflicts, then push again.

**➡️ Next:** README.md
