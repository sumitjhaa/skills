# 🧪 Real-World Scenarios — Fixes with Before & After

> **TL;DR** 5 common messes and how to get out of them.

---

## Scenario 1: I Committed to Main by Accident

**Situation:** You were on `main` and made a commit that belongs on a feature branch.

**Before:**
```
main  ●──●──●──●  (bad commit here)
```

**Fix:**
```
git branch feat
git reset --hard HEAD~1
git switch feat
```

**After:**
```
main  ●──●──●
feat  └──●
```

---

## Scenario 2: My Feature Branch Is Behind Main

**Situation:** `main` has moved ahead and your feature branch is outdated.

**Before:**
```
main     ●──●──●──●
feat     └──●──●
```

**Fix:**
```
git switch feat
git rebase main
```

**After:**
```
main     ●──●──●──●
feat                 └──●──●
```

---

## Scenario 3: I Need to Undo a Pushed Bug

**Situation:** You pushed a buggy commit to the shared branch and need to undo it safely.

**Before:**
```
origin/main  ●──●──●──●  (buggy)
```

**Fix:**
```
git revert <buggy-hash>
git push
```

**After:**
```
origin/main  ●──●──●──●──●  (revert commit undoes bug, history intact)
```

---

## Scenario 4: 5 Messy Commits Should Be 1 Clean One

**Situation:** You made 5 tiny "WIP", "oops", "fix" commits and want one clean commit.

**Before:**
```
feat  ●──●──●──●──●  (wip, oops, fix, fix2, done)
```

**Fix:**
```
git rebase -i HEAD~5
# Change "pick" to "squash" for commits 2–5
```

**After:**
```
feat  ●  (one clean commit with everything)
```

---

## Scenario 5: I Accidentally Deleted My Branch

**Situation:** You deleted a branch with `git branch -D` and panicked.

**Before:**
```
main  ●──●──●
                    feat was here — gone!
```

**Fix:**
```
git reflog
# find the last commit hash from the deleted branch
git branch rescue <hash>
```

**After:**
```
main   ●──●──●
rescue └──●──●  (branch restored from reflog)
```
