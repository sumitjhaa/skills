# 1️⃣ SETUP — INSTALL & CONFIGURE

---

⏱️ **Time:** ~10 min | 🏁 **TL;DR:** Install git, set your name and email once, and you're ready to commit forever.

---

## 🔁 LAST TIME...

In [00-what-is-git.md](00-what-is-git.md), you learned git is a time machine with three states: Working → Staging → Repository.

---

## 🖥️ INSTALL

<details>
<summary>Click to expand: Install commands</summary>

```bash
# Linux (Debian/Ubuntu)
sudo apt update && sudo apt install git -y

# Linux (Fedora)
sudo dnf install git -y

# macOS
brew install git

# Windows
# Download from https://git-scm.com/download/win → defaults → "Git from command line"
```

```bash
git --version   # Verify: git version 2.4x.x
```

</details>

---

## ⚙️ ONE-TIME SETUP (DO THIS EXACTLY ONCE)

```bash
git config --global user.name  "Your Name"       # Stamps YOUR name on every commit
git config --global user.email "your@email.com"   # Stamps YOUR email
git config --global color.ui auto                 # Colorful output
git config --global init.defaultBranch main       # Modern default branch name
git config --global core.autocrlf input           # Cross-platform line endings
```

📌 **Without `user.name` + `user.email`, git refuses to commit.**

---

## 📋 CONFIG SCOPES

| Scope | File | Applies To |
|-------|------|-----------|
| `--system` | `/etc/gitconfig` | Everyone on this computer |
| `--global` | `~/.gitconfig` | Your account (all repos) |
| `--local` (default) | `.git/config` | This repo only |

```bash
git config --list --show-origin   # See every setting and where it's defined
```

👉 **Mnemonic:** "System for the machine, Global for you, Local for one repo"

---

## 🧠 KEY TAKEAWAYS

- **Install** with your package manager, then verify with `git --version`
- **`user.name` and `user.email`** are mandatory — git won't commit without them
- Config **scopes** let you override email per project (work vs personal)
- Run `git config --global` once and forget it
- `color.ui auto` makes git output readable

---

> **Next: [02-init.md](02-init.md) — Create your first repository**
