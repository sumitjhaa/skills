# 📂 Setup & First Repo

> **TL;DR** Install Git, tell it who you are, then `init` (start fresh) or `clone` (copy from GitHub).

---

**📖 Story:** Like naming your character before saving your game — Git stamps every commit with your name + email.

**👀 Visual:**
```text
git init:  my-folder/      git clone:  GitHub ───▶ my-folder/
           └── .git/                            └── .git/
               ├── objects                           ├── objects
               ├── refs                              ├── refs
               └── HEAD                              └── HEAD
```

**🛠️ Commands:**

| Do This | What Happens |
|---------|-------------|
| `git --version` | Show installed Git version |
| `git config --global user.name "You"` | Set your name for all future commits |
| `git config --global user.email "you@..."` | Set your email for all future commits |
| `git init` | Create new empty repo in current folder |
| `git clone <url>` | Download a remote repo + full history |
| `git status` | Show what's changed/untracked/staged |
| `git log --oneline` | Show commit history (1 line each) |

**🧪 Try:**
```
git init my-project && cd my-project && git status
```

**⚠️ Watch out:** `git init` inside an existing repo creates a nested repo — use `git init` only once per project.

**➡️ Next:** [03-basics.md](03-basics.md)
