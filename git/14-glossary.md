# 📖 Glossary — Git Terms A–Z

> **TL;DR** One line per term. Skim it when you hear a word you don't know.

---

- **Amend** — Fix last commit. Don't do on shared branches.
- **Blame** — `git blame` shows who last changed each line.
- **Blob** — Git's file content storage. Same content = same hash.
- **Branch** — A movable pointer to a commit. Your "alternate reality."
- **Cherry-Pick** — Take a commit from one branch, apply to another.
- **Clone** — Copy a remote repo to your machine (full history).
- **Commit** — A snapshot of staged changes. Like a game save point.
- **Conflict** — When Git can't auto-merge. Fix it manually.
- **Detached HEAD** — Not on any branch, just at a commit. Make a branch to keep work.
- **Diff** — Shows what changed between two states.
- **Fetch** — Download remote commits without merging.
- **Force Push** — Overwrite remote history. Dangerous. Prefer `--force-with-lease`.
- **HEAD** — The commit you're currently on. Usually points to a branch.
- **Index** — Another name for the staging area.
- **Merge** — Combine two branches into one.
- **Origin** — Default name for your remote repo.
- **Pull** — `fetch` + `merge` in one command.
- **Push** — Upload local commits to the remote.
- **Rebase** — Rewrite commit history by replaying commits onto another base.
- **Reflog** — Git's activity log. Recovers "lost" commits.
- **Remote** — A repo hosted elsewhere (GitHub, GitLab, etc.).
- **Repository (repo)** — A folder tracked by Git. Has a `.git` folder inside.
- **Reset** — Move HEAD backward. `--soft` keeps changes, `--hard` destroys them.
- **Restore** — Discard or unstage changes. Modern undo tool.
- **Revert** — Create a new commit that undoes a previous one. Safe for pushed work.
- **SHA/Hash** — A 40-char ID for every commit. Unique fingerprint.
- **Squash** — Combine multiple commits into one during rebase.
- **Staging Area** — Where you prepare files before committing.
- **Stash** — Temporary shelf for uncommitted changes.
- **Switch** — Change branches. Replaces the older `checkout` for branch tasks.
- **Tag** — A named bookmark for a specific commit (usually versions).
- **Tracking** — A local branch linked to a remote branch.
- **Upstream** — The remote branch your local branch pushes/pulls from.
- **Working Directory** — The files you see and edit on your machine.
- **Worktree** — Multiple branches checked out at the same time in different folders.
