# 📋 COMPLETE GIT COMMAND INDEX

Every command in this guide, where to find it, what it does.

---

## A

| Command | File | What It Does |
|---------|------|-------------|
| `git add .` | 03-core-loop | Stage all changes |
| `git add -A` | 03-core-loop | Stage all changes (everywhere) |
| `git add -N` | 03-core-loop | Track file without staging |
| `git add -p` | 03-core-loop | Stage interactively (hunk by hunk) |
| `git add -u` | 03-core-loop | Stage only tracked files |
| `git add <file>` | 03-core-loop | Stage specific file |
| `git am` | 11-collaboration | Apply patches from email |
| `git apply` | 11-collaboration | Apply patch to working directory |
| `git archive` | 23-maintenance | Export repo without .git |

## B

| Command | File | What It Does |
|---------|------|-------------|
| `git bisect start` | 19-bisect | Begin binary search for bug |
| `git bisect bad` | 19-bisect | Mark current commit as buggy |
| `git bisect good` | 19-bisect | Mark commit as working |
| `git bisect reset` | 19-bisect | End bisect session |
| `git bisect run` | 19-bisect | Automated bisect with script |
| `git bisect visualize` | 19-bisect | View bisect progress graph |
| `git blame` | 21-advanced-tools | Show who last modified each line |
| `git branch` | 08-branch | List branches |
| `git branch -d` | 08-branch | Delete branch (safe) |
| `git branch -D` | 08-branch | Delete branch (force) |
| `git branch -m` | 08-branch | Rename branch |
| `git branch -v` | 08-branch | List with last commit |
| `git branch --merged` | 08-branch | List merged branches |
| `git branch --no-merged` | 08-branch | List unmerged branches |
| `git bundle` | 23-maintenance | Bundle repo for file transfer |
| `git bugreport` | 21-advanced-tools | Generate bug report |

## C

| Command | File | What It Does |
|---------|------|-------------|
| `git cat-file -p` | 17-internals | Pretty-print any object |
| `git cat-file -t` | 17-internals | Show object type |
| `git cat-file -s` | 17-internals | Show object size |
| `git check-attr` | 21-advanced-tools | Check gitattributes for file |
| `git check-ignore` | 06-ignore | Check if file is ignored |
| `git checkout` | 08-branch | Switch branch |
| `git checkout -b` | 08-branch | Create + switch branch |
| `git checkout --` | 12-undo | Discard file changes |
| `git checkout --detach` | 09-merge | Force detached HEAD |
| `git checkout --ours` | 09-merge | Keep our version in conflict |
| `git checkout --theirs` | 09-merge | Keep their version in conflict |
| `git cherry-pick` | 15-cherry-pick | Apply specific commit |
| `git column` | 21-advanced-tools | Format output in columns |
| `git commit-graph write` | 23-maintenance | Build commit graph (speed up log) |
| `git clean -n` | 12-undo | Dry run (show files to delete) |
| `git clean -f` | 12-undo | Delete untracked files |
| `git clean -fd` | 12-undo | Delete untracked files + dirs |
| `git clean -i` | 12-undo | Interactive clean |
| `git clean -fX` | 12-undo | Delete only ignored files |
| `git check-mailmap` | 21-advanced-tools | Check mailmap resolution for an email |
| `git clone` | 10-remote | Copy a remote repo |
| `git clone --depth` | 10-remote | Shallow clone |
| `git clone --branch` | 10-remote | Clone specific branch/tag |
| `git clone --single-branch` | 10-remote | Clone only one branch |
| `git clone --bare` | 10-remote | Bare clone (server) |
| `git clone --recursive` | 10-remote | Clone with submodules |
| `git commit` | 03-core-loop | Commit staged changes |
| `git commit -m` | 03-core-loop | Commit with inline message |
| `git commit -am` | 03-core-loop | Add + commit tracked files |
| `git commit --amend` | 03-core-loop | Fix last commit |
| `git commit -S` | 03-core-loop | Sign commit with GPG |
| `git commit-tree` | 17-internals | Create commit from tree (plumbing) |
| `git config` | 01-setup | Set configuration |
| `git config --global` | 01-setup | Set global config |
| `git config --local` | 01-setup | Set repo config |
| `git config --system` | 01-setup | Set system config |
| `git config --list` | 01-setup | List all config |
| `git config --list --show-origin` | 01-setup | List config + source file |
| `git config --unset` | 01-setup | Remove a config key |
| `git config --edit` | 01-setup | Open config in editor |
| `git config --get` | 01-setup | Get single config value |
| `git config --get-all` | 01-setup | Get all values for key |
| `git count-objects` | 23-maintenance | Count objects and disk usage |
| `git credential` | 10-remote | Manage stored credentials |

## D

| Command | File | What It Does |
|---------|------|-------------|
| `git describe` | 21-advanced-tools | Human-readable commit name |
| `git diff` | 05-diff | Show unstaged changes |
| `git diff --staged` | 05-diff | Show staged changes |
| `git diff --cached` | 05-diff | Same as --staged |
| `git diff --stat` | 05-diff | Show stats only |
| `git diff --name-only` | 05-diff | Show file names only |
| `git diff --name-status` | 05-diff | Show file names + status |
| `git diff --word-diff` | 05-diff | Word-level diff |
| `git diff --color-words` | 05-diff | Colored word diff |
| `git diff --check` | 05-diff | Check whitespace errors |
| `git difftool` | 09-merge | Launch visual diff tool |
| `git difftool --dir-diff` | 09-merge | Directory comparison side-by-side |

## F

| Command | File | What It Does |
|---------|------|-------------|
| `git fetch` | 10-remote | Download remote without merging |
| `git fetch --prune` | 10-remote | Fetch + clean stale refs |
| `git fetch --unshallow` | 10-remote | Un-shallow a shallow clone |
| `git filter-branch` | 22-filter-repo | Rewrite history (old way) |
| `git filter-repo` | 22-filter-repo | Rewrite history (fast way) |
| `git format-patch` | 11-collaboration | Create patch files |
| `git fast-export` | 22-filter-repo | Export repo to text stream |
| `git fast-import` | 22-filter-repo | Import from text stream |
| `git for-each-ref` | 17-internals | Iterate over all refs |
| `git fsck` | 23-maintenance | Check repo integrity |
| `git fsck --lost-found` | 23-maintenance | Find dangling objects |

## G

| Command | File | What It Does |
|---------|------|-------------|
| `git gc` | 23-maintenance | Garbage collection |
| `git gc --aggressive` | 23-maintenance | Aggressive optimization |
| `git grep` | 21-advanced-tools | Search tracked files |

## H

| Command | File | What It Does |
|---------|------|-------------|
| `git hash-object` | 17-internals | Compute SHA-1 of content |
| `git hash-object -w` | 17-internals | Hash AND store in .git |
| `git help` | 01-setup | Open help in browser |
| `git help -a` | 01-setup | List all commands |
| `git help -g` | 01-setup | List concept guides |
| `git hooks` | 20-hooks | pre-commit, pre-push, etc. |

## I

| Command | File | What It Does |
|---------|------|-------------|
| `git init` | 02-init | Create new repo |
| `git init --bare` | 10-remote | Create bare repo |
| `git instaweb` | 23-maintenance | Browse repo in browser |
| `git interpret-trailers` | 11-collaboration | Add structured footers |

## L

| Command | File | What It Does |
|---------|------|-------------|
| `git log` | 04-log | View commit history |
| `git log --oneline` | 04-log | Condensed history |
| `git log --graph --all` | 04-log | Visual branch tree |
| `git log --format` | 04-log | Custom output format |
| `git log --left-right` | 04-log | Show which side of merge each commit is |
| `git log --reflog` | 18-reflog | Show reflog as git log |
| `git log --since` | 04-log | Filter by date |
| `git log --author` | 04-log | Filter by author |
| `git log --grep` | 04-log | Filter by message |
| `git log -S` | 04-log | Filter by content change |
| `git log --diff-filter` | 04-log | Filter by change type |
| `git log --follow` | 04-log | Follow file renames |
| `git log --stat` | 04-log | Show file stats |
| `git log -p` | 04-log | Show diff in log |
| `git log -L` | 21-advanced-tools | Line range history |
| `git ls-remote` | 10-remote | List remote refs without cloning |
| `git ls-files --stage` | 17-internals | List staged files with hashes |
| `git ls-tree` | 17-internals | List tree contents |
| `git lfs track` | 11-collaboration | Track large files with LFS |
| `git lfs ls-files` | 11-collaboration | List LFS-tracked files |
| `git lfs pull` | 11-collaboration | Pull LFS files |
| `git lfs install` | 11-collaboration | Install LFS hooks |

## M

| Command | File | What It Does |
|---------|------|-------------|
| `git maintenance` | 23-maintenance | Auto-optimize repo |
| `git merge` | 09-merge | Merge branch into current |
| `git merge --no-ff` | 09-merge | Force merge commit |
| `git merge --ff-only` | 09-merge | Only fast-forward |
| `git merge --squash` | 09-merge | Squash merge (one commit) |
| `git merge --abort` | 09-merge | Cancel merge |
| `git merge --continue` | 09-merge | Continue after conflict resolution |
| `git merge-base` | 15-cherry-pick | Find common ancestor of two branches |
| `git mergetool` | 09-merge | Launch visual merge tool |
| `git merge-file` | 09-merge | Merge individual files (non-merge context) |
| `git multi-pack-index write` | 23-maintenance | Optimize multi-pack index |
| `git mv` | 07-rm-mv | Rename/move tracked file |

## N

| Command | File | What It Does |
|---------|------|-------------|
| `git notes add` | 21-advanced-tools | Annotate commit |

## P

| Command | File | What It Does |
|---------|------|-------------|
| `git prune` | 23-maintenance | Remove dangling objects |
| `git pull` | 10-remote | Fetch + merge |
| `git pull --rebase` | 10-remote | Fetch + rebase |
| `git pull --ff-only` | 10-remote | Pull only if fast-forward |
| `git pull --autostash` | 10-remote | Auto-stash before pull |
| `git push` | 10-remote | Upload to remote |
| `git push -u` | 10-remote | Push + set upstream |
| `git push --force-with-lease` | 10-remote | Safe force push |
| `git push --force` | 10-remote | Dangerous force push |
| `git push --dry-run` | 10-remote | Show what would push |
| `git push --delete` | 10-remote | Delete remote branch |
| `git push --all` | 10-remote | Push all branches |
| `git push --follow-tags` | 10-remote | Push tags too |
| `git push --atomic` | 10-remote | Push only if ALL refs succeed |
| `git push --signed` | 10-remote | GPG-sign the push cert |

## R

| Command | File | What It Does |
|---------|------|-------------|
| `git range-diff` | 15-cherry-pick | Compare commit ranges |
| `git read-tree` | 17-internals | Read tree into index |
| `git rebase` | 14-rebase | Replay commits on new base |
| `git rebase -i` | 14-rebase | Interactive rebase |
| `git rebase --onto` | 14-rebase | Targeted rebase (power tool) |
| `git rebase --autosquash` | 14-rebase | Auto-order fixup commits |
| `git rebase --exec` | 14-rebase | Run command after each commit |
| `git rebase --abort` | 14-rebase | Cancel rebase |
| `git rebase --skip` | 14-rebase | Skip problematic commit |
| `git rebase --continue` | 14-rebase | Continue after fixing conflicts |
| `git reflog` | 18-reflog | View local activity log |
| `git remote -v` | 10-remote | List remotes |
| `git remote add` | 10-remote | Add remote |
| `git remote remove` | 10-remote | Remove remote |
| `git remote rename` | 10-remote | Rename remote |
| `git remote show` | 10-remote | Show remote details |
| `git remote prune` | 10-remote | Clean stale tracking refs |
| `git remote set-url` | 10-remote | Change remote URL |
| `git remote set-head` | 10-remote | Set default branch for remote |
| `git replace` | 21-advanced-tools | Replace objects |
| `git repack` | 23-maintenance | Repack objects into packs |
| `git request-pull` | 11-collaboration | Generate pull request text |
| `git rerere` | 09-merge | Reuse recorded resolution |
| `git reset --soft` | 12-undo | Undo commit, keep staged |
| `git reset --mixed` | 12-undo | Undo commit, unstage |
| `git reset --hard` | 12-undo | Delete commit + changes |
| `git reset --keep` | 12-undo | Reset, keep unstaged changes |
| `git reset --merge` | 12-undo | Safe reset (abort if conflict) |
| `git restore` | 12-undo | Discard working changes |
| `git restore --staged` | 12-undo | Unstage file |
| `git restore -p` | 12-undo | Interactive discard |
| `git restore --source` | 12-undo | Restore from old commit |
| `git revert` | 12-undo | Safe undo (new commit) |
| `git rev-list` | 17-internals | List commit objects |
| `git rev-parse` | 17-internals | Resolve reference to hash |
| `git rm` | 07-rm-mv | Delete file + stage deletion |
| `git rm --cached` | 07-rm-mv | Remove from tracking, keep file |

## S

| Command | File | What It Does |
|---------|------|-------------|
| `git shortlog` | 15-cherry-pick | Contributor summary |
| `git show-ref` | 17-internals | Show SHA-1 of a ref |
| `git show` | 05-diff | View any object |
| `git show --stat` | 05-diff | Show with stats |
| `git show --staged` | 05-diff | Show staged changes |
| `git sparse-checkout` | 23-maintenance | Partial checkout |
| `git stash` | 13-stash | Save work temporarily |
| `git stash push -m` | 13-stash | Stash with message |
| `git stash --patch` | 13-stash | Interactive stash (hunk by hunk) |
| `git stash list` | 13-stash | List stashes |
| `git stash pop` | 13-stash | Apply + remove top stash |
| `git stash apply` | 13-stash | Apply + keep stash |
| `git stash drop` | 13-stash | Delete stash |
| `git stash clear` | 13-stash | Delete ALL stashes |
| `git stash show -p` | 13-stash | Show stash diff |
| `git stash branch` | 13-stash | Turn stash into branch |
| `git stash --keep-index` | 13-stash | Stash only unstaged |
| `git stash -u` | 13-stash | Include untracked |
| `git status` | 03-core-loop | Check working directory state |
| `git status -s` | 03-core-loop | Short status |
| `git status --porcelain` | 01-setup | Stable status for scripts |
| `git submodule` | 23-maintenance | Repo inside a repo |
| `git submodule foreach` | 23-maintenance | Run command in each submodule |
| `git submodule status` | 23-maintenance | Show submodule status |
| `git submodule summary` | 23-maintenance | Show submodule changes |
| `git submodule sync` | 23-maintenance | Sync submodule remote URLs |
| `git switch` | 08-branch | Switch branch |
| `git switch -c` | 08-branch | Create + switch |
| `git symbolic-ref` | 17-internals | Read/update HEAD ref |

## T

| Command | File | What It Does |
|---------|------|-------------|
| `git tag` | 16-tag | List tags |
| `git tag -a` | 16-tag | Create annotated tag |
| `git tag -s` | 16-tag | Create signed tag |
| `git tag -d` | 16-tag | Delete tag |
| `git tag -v` | 16-tag | Verify signed tag |

## U

| Command | File | What It Does |
|---------|------|-------------|
| `git update-index --assume-unchanged` | 06-ignore | Ignore local changes to file |
| `git update-index --skip-worktree` | 06-ignore | Ignore local changes (sturdier) |
| `git update-ref` | 17-internals | Move branch pointer |

## V

| Command | File | What It Does |
|---------|------|-------------|
| `git verify-commit` | 23-maintenance | Verify GPG signature |
| `git verify-tag` | 23-maintenance | Verify tag signature |
| `git --version` | 01-setup | Show git version |

## W

| Command | File | What It Does |
|---------|------|-------------|
| `git worktree add` | 23-maintenance | Checkout branch in separate dir |
| `git worktree add --detach` | 23-maintenance | Worktree in detached HEAD |
| `git worktree list` | 23-maintenance | List worktrees |
| `git worktree lock` | 23-maintenance | Lock worktree (prevent prune) |
| `git worktree unlock` | 23-maintenance | Unlock worktree |
| `git worktree prune` | 23-maintenance | Remove stale worktree records |
| `git worktree remove` | 23-maintenance | Remove worktree |
| `git write-tree` | 17-internals | Write index as tree object |

---

## 📁 SPECIAL FILES

| File | Section | What It Does |
|------|---------|-------------|
| `.mailmap` | 02-init, 24-pro | Fix duplicate author names in log |
| `.gitkeep` | 02-init, 24-pro | Track empty directories (convention) |
| `.gitattributes` | 24-pro | Line endings, merge strategies |
| `.gitignore` | 06-ignore | Patterns to ignore |

---

## 🔧 CONFIG & CLI

| Command | File | What It Does |
|---------|------|-------------|
| `git -C <path>` | 01-setup | Run git as if in that directory |
| `git --no-pager` | 01-setup | Disable pager for command |
| `git -c key=value` | 01-setup | Override config for one command |
| `git --paginate` | 01-setup | Force pager |
| `git --literal-pathspecs` | 01-setup | Treat paths literally (no glob) |
| `git --help` | 01-setup | Open help |

---

## 🧰 GIT CLIENT

| Command | File | What It Does |
|---------|------|-------------|
| `gh pr create` | 11-collaboration | Create PR from CLI |
| `gh pr checkout` | 11-collaboration | Checkout PR locally |
| `gh pr list` | 11-collaboration | List PRs |
| `gh run list` | 11-collaboration | List CI runs |

---

---

## 🚀 ECOSYSTEM TOOLS

| Tool | File | What It Does |
|------|------|-------------|
| `gh api` | 25-workflows | Set branch protection rules via API |
| `gpg --full-generate-key` | 25-workflows | Create GPG key for signed commits |
| `pre-commit install` | 25-workflows | Install pre-commit framework hooks |
| `npx commitlint` | 25-workflows | Enforce conventional commit format |
| `npx semantic-release` | 25-workflows | Auto-version from conventional commits |
| `npx nx affected:test` | 25-workflows | Run tests for changed packages (Nx) |
| `npx turbo run --filter` | 25-workflows | Scoped builds for changed packages (Turborepo) |
| `.github/CODEOWNERS` | 25-workflows | Auto-request reviewers by file pattern |

---

> **Total: ~200 commands across 26 topic files + reference files + ecosystem tools.**
