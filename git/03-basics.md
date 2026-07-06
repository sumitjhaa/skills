# 📂 The Basics: Add, Commit, Diff, Ignore

> **TL;DR** Stage changes with `add`, save a checkpoint with `commit`, and ignore junk with `.gitignore`.

---

**📖 Story:** Shopping cart — `add` puts items in your cart (stage), `commit` checks out (saves). You can review the receipt with `diff` before paying.

**👀 Visual:**
```text
Create file ──git add──▶ 📋 Staged ──git commit──▶ 🗃️ History

  touch hello.js       git add hello.js       git commit -m "add hello"

                                                  git log --oneline
                                                  1a2b3c4 add hello
```

**🛠️ Commands:**

| Do This | What Happens |
|---------|-------------|
| `git add <file>` | Stage a single file |
| `git add .` | Stage all changed files in current dir |
| `git add -A` | Stage all changes everywhere in repo |
| `git add -p` | Interactive: stage parts of a file (hunks) |
| `git commit -m "msg"` | Save staged changes with a message |
| `git commit --amend` | Edit last commit message or add forgotten files |
| `git diff` | Show unstaged changes (what you haven't `add`-ed) |
| `git diff --staged` | Show staged changes (what will commit) |

**🧪 Try:**
```
echo "hi" > test.txt && git add test.txt && git commit -m "first file"
```

**⚠️ Watch out:** `git commit` only commits what's staged — use `git diff --staged` to verify before committing.

**📄 .gitignore — keep junk out:**
```
# Patterns Git will ignore:
node_modules/     # dependency folder
.env              # secrets file
*.log             # all log files
/build            # build output folder
!important.log    # exception: track this log
```

**➡️ Next:** [04-branching.md](04-branching.md)
