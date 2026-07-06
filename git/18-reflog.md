# 18️⃣ REFLOG — TIME MACHINE

⏱️ **Time:** ~10 min | 🏁 **TL;DR:** `git reflog` = your LOCAL activity diary. Every checkout, commit, reset, merge — even on deleted branches. Recover anything within 90 days.

## 🔁 LAST TIME...

In [17-internals.md](17-internals.md), you learned about git objects and plumbing.

---

### `git reflog` — See Everything You Did

```bash
git reflog
# → abc123 HEAD@{0}: commit: feat: critical feature
# → def456 HEAD@{1}: checkout: moving from main to feat/old
# → ghi789 HEAD@{3}: commit: feat: lost feature work  ← FOUND IT!
```

### Recover Deleted Branches / Lost Commits

```bash
# Find the lost commit hash with git reflog, then:
git checkout -b rescued-feature ghi789

# Or reset directly using the reference:
git reset --hard HEAD@{3}
```

### Branch-Specific Reflog & `git log --reflog`

```bash
git reflog feat/deleted-branch         # Reflog for a specific branch
git log --reflog --oneline             # Reflog as proper git log
git log --reflog --grep="reset"        # Search reflog for "reset"
```

💡 **Reflog is LOCAL only — never pushed to remote.** Entries expire after ~90 days. `HEAD@{n}` references are local to YOUR machine.

👉 **Mnemonic:** Reflog = "Git's memory. It forgets nothing." `HEAD@{3}` = "What was HEAD 3 moves ago."

---

## 🧠 KEY TAKEAWAYS

- **`git reflog` = personal time machine** — shows every git command you ran
- **Recover deleted branches** by finding the commit hash in reflog and branching from it
- **`HEAD@{n}` notation** references your local history (`HEAD@{1}` = previous state)
- **Reflog is NOT shared** — it's your local safety net, not a remote feature
- **`git log --reflog`** combines reflog entries with all `git log` formatting options

---

**Next: [19-bisect.md](19-bisect.md)**
