# 25️⃣ PRODUCTION WORKFLOWS

⏱️ **Time:** ~20 min | 🏁 **TL;DR:** Real teams combine git commands into repeatable workflows. This file covers branch protection, signed commits, releases, monorepos, GitOps, backup, and team automation.

---

## 🔁 LAST TIME...

In [24-pro.md](24-pro.md), you learned branching strategies, commit message rules, and `.gitattributes`.

**Today:** The workflows that separate pro teams from everyone else.

---

## 1. Branch Protection Rules

On GitHub/GitLab, protect `main` with these rules:

```
☑ Require a pull request before merging (1+ approvals)
☑ Dismiss stale approvals when new commits are pushed
☑ Require status checks to pass (CI, lint, test)
☑ Require branches to be up to date
☑ Require linear history (no merge commits — forces rebase)
☑ Include administrators (so even you can't bypass)
```

```bash
# GitHub CLI — set branch protection
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"checks":[{"context":"continuous-integration"}]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}'
```

## 2. CODEOWNERS — Automatic Reviewers

```
# File: .github/CODEOWNERS
# Each line: pattern → @team or @user

*                       @core-team
src/api/                @api-team @lead-engineer
src/frontend/           @frontend-team
*.md                    @docs-writer
package.json            @dependabot
```

👉 **CODEOWNERS auto-requests reviews when matching files change.**

## 3. GPG Signed Commits

```bash
# Generate a GPG key
gpg --full-generate-key
git config --global user.signingkey <KEY-ID>
git config --global commit.gpgsign true   # Sign ALL commits

# Add public key to GitHub: Settings → SSH and GPG keys → New GPG key
gpg --armor --export <KEY-ID>

# Verify signatures in log
git log --show-signature
git verify-commit HEAD
```

⚠️ **Set `git config --global tag.gpgsign true` to sign tags too.**

## 4. Semantic Versioning & Releases

```bash
# Tag format: vMAJOR.MINOR.PATCH
# v1.0.0   = first stable release
# v1.1.0   = new features (backward compatible)
# v2.0.0   = breaking changes

# Auto-generate changelog from conventional commits
git shortlog v1.0.0..HEAD --no-merges > CHANGELOG.md

# Or use semantic-release (automated version bump + publish)
npx semantic-release
# → Reads conventional commits → bumps version → tags → releases
```

## 5. Merge Strategy Decision Tree

```
                ┌─ Squash merge ── "One commit per PR, clean main"
Team policy?    ├─ Rebase merge ── "Every commit matters, linear"
                └─ Merge commit ── "Preserve branch topology"
```

| Strategy | Pros | Cons | Best for |
|----------|------|------|----------|
| Squash | Single clean commit on main | Loses individual commit history | Most teams |
| Rebase | Linear history, all commits kept | Forces conflict resolution per commit | Power users |
| Merge | Preserves exactly what happened | Cluttered history with merge commits | Audited projects |

## 6. Monorepo Strategies

```bash
# Sparse checkout — only the directories you need
git sparse-checkout init --cone
git sparse-checkout set packages/api packages/shared

# CODEOWNERS for path-based ownership
git check-attr --all packages/api/README.md  # Debug ownership rules

# Monorepo tools integrate with git diff:
npx nx affected:test --base=main   # Run tests only for changed packages
npx turbo run build --filter=...[main]  # Turborepo scoped builds
```

## 7. GitOps — Git as Deployment Source

```
  ┌──────────┐     ┌──────────┐     ┌──────────┐
  │ git push │────>│  CI/CD   │────>│ Deploy   │
  │ main     │     │ pipeline │     │ to prod  │
  └──────────┘     └──────────┘     └──────────┘
                        │
                        v
                  ┌──────────┐
                  │ ArgoCD   │
                  │ (watches │
                  │  git)    │
                  └──────────┘
```

```bash
# ArgoCD: cluster auto-syncs with git repo
# Flux: watches git, applies manifests to Kubernetes

# Promotion workflow:
git tag prod-v1.2.3                # Tag current main as production
git push origin prod-v1.2.3        # Trigger deployment
git revert prod-v1.2.3             # Rollback (safe undo of a release)
```

## 8. Git Backup & Disaster Recovery

```bash
# Full repo backup (all branches, all tags)
git bundle create backup-$(date +%Y%m%d).bundle --all

# Clone from bundle to verify
git clone backup-20240601.bundle backup-verify
cd backup-verify && git fsck --lost-found

# Mirror clone (full copy, including all refs)
git clone --mirror https://github.com/org/repo.git repo-backup.git
cd repo-backup.git && git gc --aggressive

# Schedule: daily bundle + weekly mirror
# Store: separate drive / S3 / different cloud
```

## 9. commitlint — Enforce Commit Conventions

```bash
# Install
npm install -g @commitlint/cli @commitlint/config-conventional
echo "module.exports = {extends: ['@commitlint/config-conventional']}" > commitlint.config.js

# Git hook to enforce
# .githooks/commit-msg:
#   npx commitlint -e $1 || exit 1

# Test locally:
echo "fix: resolve timeout" | npx commitlint   # ✅ passes
echo "fixed stuff" | npx commitlint             # ❌ fails
```

## 10. pre-commit Framework

```bash
# Install hooks declaratively (YAML-based)
# pip install pre-commit || npm install -g @commitlint/cz-commitlint

# File: .pre-commit-config.yaml
#   repos:
#     - repo: https://github.com/pre-commit/pre-commit-hooks
#       rev: v4.5.0
#       hooks:
#         - id: trailing-whitespace
#         - id: end-of-file-fixer
#     - repo: https://github.com/pre-commit/mirrors-eslint
#       rev: v8.0.0
#       hooks:
#         - id: eslint

# Install into git hooks:
pre-commit install    # → Creates .git/hooks/pre-commit
pre-commit run --all-files  # Run on everything (once)
```

👉 **pre-commit framework = declarative hooks your whole team shares.**

---

## 🧠 KEY TAKEAWAYS

- **Branch protection** prevents force-pushes to main and requires reviews + CI
- **GPG signing** proves commits came from you (enable `commit.gpgsign true`)
- **Semantic-release** automates version bumps from conventional commits
- **Monorepo tools** (Nx/Turborepo) use `git diff` to detect what changed
- **GitOps** uses git as the single source of truth for deployments
- **Regular bundles** (`git bundle create`) are your best offline backup
- **commitlint + pre-commit** automate quality before code ever reaches GitHub

---

**Congratulations. You've reached MENACE level. Now go ship.**
