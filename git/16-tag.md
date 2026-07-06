# 16️⃣ TAG — PERMANENT BOOKMARKS

⏱️ **Time:** ~10 min | 🏁 **TL;DR:** Tags are permanent labels on commits. Use `git tag -a v1.0 -m "msg"` for releases (annotated). Lightweight tags are for personal bookmarks. Unlike branches, tags never move.

## 🔁 LAST TIME...

In [15-cherry-pick.md](15-cherry-pick.md), you learned cherry-pick, range-diff, shortlog, and merge-base.

---

### Lightweight vs Annotated

```bash
git tag v1.0.0                           # Lightweight (no metadata)
git tag -a v1.0.0 -m "Release v1.0.0"    # Annotated (author, date, message)
```

### Listing & Comparing

```bash
git tag                                  # List all
git tag -l "v2.*"                        # Pattern match
git tag -n                               # With messages
git show v1.0.0                          # View tag + commit
git diff v1.0.0 v2.0.0                   # Compare tagged versions
```

### Pushing & Deleting

```bash
git push origin v1.0.0                   # Push one tag
git push --follow-tags                   # Push annotated only (safe)
git tag -d v1.0.0                        # Delete local
git push origin --delete v1.0.0          # Delete remote
```

### Signed Tags & Checkout

```bash
git tag -s v1.0.0 -m "Release"           # GPG-signed
git tag -v v1.0.0                        # Verify signature
git checkout v1.0.0                      # Detached HEAD!
git switch -c hotfix/v1.0.1 v1.0.0       # Branch from tag
```

👉 **Mnemonic:** "Tag = museum plaque. Branch = construction sign. Both point, but tags never move."

---

## 🧠 KEY TAKEAWAYS

- **Annotated tags** (`-a`) store author, date, message — always use for releases
- **Tags are permanent** — they never move like branches do
- **Checking out a tag puts you in detached HEAD** — create a branch to make changes
- **Push with `--follow-tags`** to send only annotated tags (safer than `--tags`)

---

**Next: [17-internals.md](17-internals.md)**
