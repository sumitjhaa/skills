# 📂 Advanced Git

> **TL;DR** Peek under the hood and manage sub-projects, automation, and parallel work.

---

**📖 Story:** Git isn't magic — it's a content-addressable filesystem. And you can plug other repos into yours, run scripts on events, and work on two branches at once.

**👀 Visual:**
```text
Git internals:
Commit → Tree → [Blob: README.md, Blob: app.js]

Objects:
  blob   = file content
  tree   = directory (maps names → blobs/trees)
  commit = snapshot (points to tree + parent)

Submodules (repo in a repo):
  main-repo/ ← your code
    sub/     ← pinned version of another repo
```

## Git Internals

**🛠️ Commands:**
| Do This | What Happens |
|---------|-------------|
| `git hash-object file` | Get blob's SHA-1 |
| `git cat-file -p hash` | View any object |
| `git ls-tree hash` | List a tree's contents |

## Submodules — embed another repo

**🛠️ Commands:**
| Do This | What Happens |
|---------|-------------|
| `git submodule add url path` | Add a submodule |
| `git clone --recursive url` | Clone with all submodules |
| `git submodule update --init` | Pull submodule after clone |

## Hooks — auto-run scripts

**🛠️ Commands:**
| Do This | What Happens |
|---------|-------------|
| `.git/hooks/pre-commit` | Runs before each commit (lint) |
| `.git/hooks/pre-push` | Runs before push (tests) |
| `.git/hooks/commit-msg` | Validates commit message |

## Worktrees — two branches at once

**🛠️ Commands:**
| Do This | What Happens |
|---------|-------------|
| `git worktree add ../folder branch` | Checkout branch in new folder |
| `git worktree list` | Show all worktrees |
| `git worktree prune` | Clean up deleted worktrees |

**🧪 Try:**
```
echo hello | git hash-object --stdin   # see an object hash
```

**⚠️ Watch out:** Submodules pin a specific commit — don't forget to commit the submodule pointer update. Hook scripts must be made executable (`chmod +x`).

**➡️ Next:** 11-workflows.md
