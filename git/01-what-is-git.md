# 📂 What Is Git?

> **TL;DR** Git tracks file changes so you can save checkpoints, switch timelines, and never lose work.

---

**📖 Story:** Like save slots in a video game — `commit` is saving, `branch` is a parallel what-if timeline, `checkout` is loading a save.

**👀 Visual:**
```text
📝 Working Dir  ──git add──▶  📋 Stage  ──git commit──▶  🗃️ Repo
     │                              │
     ◀──git restore──┘    ◀──git restore --staged──┘
```

**🔑 Key Terms:**

| Term | What it is (1 line) |
|------|---------------------|
| **Repo** | Your project folder + Git's hidden `.git` database |
| **Commit** | A snapshot of all staged files at a moment in time |
| **Branch** | A movable pointer to one commit — the default is `main` |
| **HEAD** | "You are here" pointer showing your current commit |
| **Remote** | A copy of your repo on another machine (e.g. GitHub) |

**🧪 Try:**
```
git --version   # check it's installed
git help        # view all commands
```

**⚠️ Watch out:** Git only tracks files you explicitly tell it about (via `add`).

**➡️ Next:** [02-setup.md](02-setup.md)
