# 🦋 GIT CHEAT SHEET — 1-Page Quick Reference

---

## 🔄 CORE LOOP

| Action | Command |
|--------|---------|
| Check state | `git status` / `git status -s` |
| Stage file | `git add <file>` |
| Stage all | `git add .` |
| Stage hunks | `git add -p` |
| Commit | `git commit -m "type: message"` |
| Commit all tracked | `git commit -am "type: message"` |
| Fix last commit | `git add . && git commit --amend --no-edit` |
| View history | `git log --oneline --graph --all --decorate` |
| View commit | `git show` |
| Diff unstaged | `git diff` |
| Diff staged | `git diff --staged` |
| Word diff | `git diff --word-diff` |
| Delete file (stage) | `git rm <file>` |
| Rename file (stage) | `git mv <old> <new>` |

---

## 🌿 BRANCHING

| Action | Command |
|--------|---------|
| List branches | `git branch` |
| Create branch | `git branch <name>` |
| Create + switch | `git switch -c <name>` |
| Switch branch | `git switch <name>` |
| Switch previous | `git switch -` |
| Delete branch (safe) | `git branch -d <name>` |
| Delete branch (force) | `git branch -D <name>` |
| Merge into current | `git merge <name>` |
| Force merge commit | `git merge --no-ff <name>` |
| Abort merge | `git merge --abort` |
| Pick ours/theirs | `git checkout --ours <file>` / `--theirs <file>` |

---

## 🌐 REMOTE

| Action | Command |
|--------|---------|
| Clone (full) | `git clone <url>` |
| Clone (shallow) | `git clone --depth 1 <url>` |
| Push (first time) | `git push -u origin HEAD` |
| Push | `git push` |
| Safe force push | `git push --force-with-lease` |
| Delete remote branch | `git push origin --delete <name>` |
| Pull (rebase) | `git pull --rebase` |
| Pull (ff-only) | `git pull --ff-only` |
| Fetch | `git fetch` |
| Fetch + prune | `git fetch --prune` |
| List remotes | `git remote -v` |
| Add remote | `git remote add <name> <url>` |

---

## ↩️ UNDOING

| Action | Command |
|--------|---------|
| Unstage file | `git restore --staged <file>` |
| Discard changes | `git restore <file>` |
| Undo commit (keep) | `git reset --soft HEAD~1` |
| Undo commit (unstage) | `git reset HEAD~1` |
| Delete commit (⚠️) | `git reset --hard HEAD~1` |
| Safe undo (new commit) | `git revert <hash>` |
| Restore from old commit | `git restore --source HEAD~2 <file>` |
| Browse reflog | `git reflog` |
| Recover from reflog | `git reset --hard HEAD@{N}` |

---

## 📦 STASH

| Action | Command |
|--------|---------|
| Stash changes | `git stash` |
| Stash with message | `git stash push -m "msg"` |
| Stash hunks | `git stash --patch` |
| Stash only unstaged | `git stash --keep-index` |
| Stash + untracked | `git stash -u` |
| List stashes | `git stash list` |
| Apply top stash | `git stash pop` |
| Apply + keep | `git stash apply` |
| Delete stash | `git stash drop` |
| Delete all stashes | `git stash clear` |
| Show stash diff | `git stash show -p` |
| Stash → branch | `git stash branch <name>` |

---

## ⚔️ ADVANCED

| Action | Command |
|--------|---------|
| Rebase onto main | `git rebase main` |
| Interactive rebase | `git rebase -i HEAD~N` |
| Rebase --onto | `git rebase --onto <target> <upstream> <branch>` |
| Continue after fix | `git rebase --continue` |
| Cherry-pick commit | `git cherry-pick <hash>` |
| Cherry-pick range | `git cherry-pick A..B` |
| Auto-squash | `git commit --fixup HEAD && git rebase -i --autosquash` |
| Range-diff | `git range-diff A B` |
| Contributor summary | `git shortlog -sn` |
| Create tag | `git tag -a v1.0 -m "msg"` |
| Delete tag | `git tag -d v1.0` |
| Find merge base | `git merge-base A B` |
| Continue merge | `git merge --continue` |

---

## 💀 MENACE

| Action | Command |
|--------|---------|
| Search tracked files | `git grep "pattern"` |
| Who modified this? | `git blame <file>` |
| Find bug (bisect) | `git bisect start && git bisect bad/good` |
| Automated bisect | `git bisect run <script>` |
| Describe commit | `git describe --tags --always` |
| Bundle repo | `git bundle create file.bundle --all` |
| Export without .git | `git archive --format=zip HEAD > project.zip` |
| Visual web browser | `git instaweb` |
| Integrity check | `git fsck` |
| Optimize repo | `git gc --aggressive` |
| Count objects | `git count-objects -v` |
| Partial checkout | `git sparse-checkout set <dir>` |
| Worktree | `git worktree add <path> <branch>` |
| Check ignore | `git check-ignore <file>` |
| Check attributes | `git check-attr --all <file>` |
| Verify signature | `git verify-commit <hash>` |

---

## 🏷️ CONFIG

| Action | Command |
|--------|---------|
| Set name (global) | `git config --global user.name "Name"` |
| Set email (global) | `git config --global user.email "e@mail"` |
| Set name (local) | `git config --local user.email "e@work.com"` |
| Default branch | `git config --global init.defaultBranch main` |
| Color always | `git config --global color.ui auto` |
| Set editor | `git config --global core.editor "code --wait"` |
| Create alias | `git config --global alias.tree "log --oneline --graph --all"` |
| SSH auth test | `ssh -T git@github.com` |

---

## 📝 CONVENTIONAL COMMITS

```
  feat:     New feature
  fix:      Bug fix
  chore:    Maintenance, deps
  docs:     Documentation
  refactor: Code restructure
  test:     Tests
  style:    Formatting
  perf:     Performance
  ci:       CI config
  build:    Build system
```

**Format:** `<type>(<scope>): <description>`
**Subject:** ≤ 50 chars. **Body:** wrap at 72. **Imperative mood.**
