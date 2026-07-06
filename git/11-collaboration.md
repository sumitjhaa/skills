# 11️⃣ COLLABORATION WORKFLOWS

⏱️ **Time:** ~15 min | 🏁 **TL;DR:** Fork → clone → branch → PR. `origin` = your fork, `upstream` = original repo. Conventional commits (`feat:`, `fix:`). `gh pr create` from CLI.

## 🔁 LAST TIME...
In [10-remote.md](10-remote.md) — remotes, `push --force-with-lease`, fetch/prune, `pull --rebase`.

---

### Fork + Pull Request
```bash
git remote add upstream https://github.com/org/project.git
git fetch upstream && git merge upstream/main
git switch -c feat/thing && git push -u origin feat/thing
gh pr create --title "feat: …" --body "Closes #42" --base main
```

### Branch Naming & Conventional Commits
| Prefix | Purpose | Example |
|---|---|---|
| `feat/` | Feature | `feat/login-form` |
| `fix/` | Bug fix | `fix/null-pointer` |
| `chore/` | Maintenance | `chore/update-deps` |
| `docs/` | Docs | `docs/api-guide` |
| `refactor/` | Restructure | `refactor/auth-module` |

`<type>(<scope>): <desc>` — e.g. `feat(auth): add Google OAuth`. Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `style`, `perf`, `ci`, `build`.

### Email Patches & Trailers
```bash
git format-patch HEAD~3           # → 0001-*.patch (email these)
git am 0001-*.patch               # Apply as commits
git request-pull v1.0.0 <url>    # PR summary for maintainers
git interpret-trailers --trailer "Signed-off-by: You <you@email.com>"
# Trailers: Signed-off-by, Reviewed-by, Acked-by, Fixes: #N
```

### CI/CD & LFS
```bash
git clone --depth 50 <url>    # Shallow clone for CI
git lfs track "*.psd"         # Large binaries (>10MB)
```

**PR Checklist:** Branch convention ✓ | Conventional commits ✓ | Tests pass ✓ | No secrets ✓

---

## 👉 MNEMONIC — **"origin = my fork, upstream = their repo. Small PRs merge fast."**

## 🧠 KEY TAKEAWAYS
- **`origin` = your fork, `upstream` = original repo** — configure both
- **Conventional commits** enable automatic changelogs
- **`gh pr create`** opens PRs from the terminal
- **`git format-patch` + `git am`** = email collaboration (Linux kernel style)
- **Small, focused PRs** get reviewed and merged faster

---

> **Next: [12-undo.md](12-undo.md) — Undoing mistakes**
