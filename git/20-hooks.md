# 20️⃣ HOOKS — AUTOMATE EVERYTHING

⏱️ **Time:** ~10 min | 🏁 **TL;DR:** Hooks are scripts that run automatically on git events (commit, push, merge). Exit non-zero to abort the action. Share via `core.hooksPath`.

## 🔁 LAST TIME...

In [19-bisect.md](19-bisect.md), you learned to find bugs with `git bisect`.

---

### Available Hooks

| Hook | When It Runs | Exit Non-Zero = |
|------|-------------|----------------|
| `pre-commit` | Before commit message | ❌ Aborts commit |
| `prepare-commit-msg` | After default message | Edits message |
| `commit-msg` | After commit message editor | ❌ Aborts commit |
| `post-commit` | After commit completes | Can't abort |
| `pre-push` | Before push to remote | ❌ Aborts push |
| `post-merge` | After merge completes | Notification |
| `pre-rebase` | Before rebase starts | ❌ Aborts rebase |

### Example: pre-commit (block debugger statements)

```bash
#!/bin/bash
if git diff --cached | grep -n "debugger;" > /dev/null; then
  echo "❌ Remove debugger statements before committing!"
  exit 1
fi
```

### Example: pre-push (run tests)

```bash
#!/bin/bash
npm test || { echo "❌ Tests failed. Push aborted."; exit 1; }
```

### Share Hooks with Your Team

```bash
mkdir -p .githooks
# Create hook scripts in .githooks/
git config core.hooksPath .githooks
# → .githooks/ is committed. Everyone gets the hooks.
```

👉 **Mnemonic:** Hooks = "If this happens, run that." `pre-commit` = "Before commit, check everything."

---

## 🧠 KEY TAKEAWAYS

- **Hooks = scripts that auto-run on git events** — live in `.git/hooks/` or custom path
- **`pre-commit` and `pre-push`** are the most common — enforce linting, tests, secrets scanning
- **Exit non-zero to abort** the action (pre-commit, pre-push, commit-msg)
- **Share hooks with `core.hooksPath`** pointing to a committed `.githooks/` directory
- **Use a hook manager** like `pre-commit` (Python) or `husky` (JS) for complex setups

---

**Next: [21-advanced-tools.md](21-advanced-tools.md)**
