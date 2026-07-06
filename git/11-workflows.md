# 📂 Workflows

> **TL;DR** Four battle-tested ways to collaborate with git — pick the one that fits your team.

---

**📖 Story:** Same tool, different styles — like solo camping vs. a construction crew.
## Feature Branch — most common
**👀 Visual:**
```text
main ●──●──●────●────●
        \      /    /
feat     ●──●──●──●
```

**🛠️ How it works:**
1. Branch from `main` for each feature
2. Commit, push, open a PR
3. Merge → delete the branch

## GitFlow — releases & hotfixes

**👀 Visual:**
```text
main  ●─────────●── v2.0
       \       /
dev    ●──●──●──●──●
         \    /
feature  ●──●
```

**🛠️ How it works:**
| Branch | Purpose |
|--------|---------|
| `main` | Production (only merges from release/hotfix) |
| `develop` | Integration |
| `feature/*` | New work (→ develop) |
| `release/*` | Polish for release (→ main + develop) |
| `hotfix/*` | Emergency fix (→ main + develop) |

---

## Trunk-Based — CI/CD speed

**👀 Visual:**
```text
main ●──●──●──●──●──●──● (many commits/day)
```

**🛠️ How it works:**
- Short-lived branches (hours, not days)
- Merge to `main` many times a day
- Feature flags instead of long-lived branches
- Heavy automated testing on every push

---

## Forking — open source

**👀 Visual:**
```text
upstream ●──●──●
              ↑ PR
fork     ●──●──●
```

**🛠️ How it works:**
1. Fork the repo on GitHub
2. Clone your fork
3. Branch → commit → push to your fork
4. Open PR to the original repo

---

**🧪 Try:** Pick one workflow. For most teams, Feature Branch is the safest start.

**⚠️ Watch out:** GitFlow is overkill for small teams. Trunk-Based needs good tests. Forking adds sync overhead. Pick the simplest that works.

**➡️ Next:** You're done! 🎉
