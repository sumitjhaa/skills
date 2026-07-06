# 17️⃣ INTERNALS — UNDER THE HOOD

⏱️ **Time:** ~15 min | 🏁 **TL;DR:** Git has 4 objects: blob (file), tree (folder), commit (snapshot), tag (bookmark). Every object gets a unique SHA-1 hash. Same content = same hash = automatic dedup.

## 🔁 LAST TIME...

In [16-tag.md](16-tag.md), you learned about lightweight vs annotated tags.

---

### The `.git` Directory

```
.git/objects/       ← All data, stored by SHA-1 prefix
.git/refs/heads/    ← Local branch pointers
.git/refs/tags/     ← Tag references
.git/HEAD           ← Current branch
.git/index          ← Staging area
```

### 4 Object Types

| Object | Purpose | Example |
|--------|---------|--------|
| Blob | File content | `echo "hi" | git hash-object --stdin` |
| Tree | Directory listing | `git ls-tree HEAD` |
| Commit | Snapshot + metadata | `git cat-file -p HEAD` |
| Tag | Named bookmark | `git cat-file -p v1.0` |

### Plumbing Commands

```bash
git hash-object -w file    # Store a blob
git cat-file -p <hash>     # View any object
git ls-tree HEAD           # List tree contents
git ls-files --stage       # List staged files
git rev-parse HEAD         # Resolve to hash
git rev-list HEAD          # List commits
git show-ref HEAD          # Show the SHA-1 of any ref
git for-each-ref           # Iterate over all refs (branches/tags)
```

### Manual Commit (what `git commit` does internally)

```bash
TREE=$(git write-tree)
COMMIT=$(echo "msg" | git commit-tree $TREE -p HEAD)
git update-ref refs/heads/main $COMMIT
```

### Plumbing vs Porcelain

| Porcelain | Plumbing |
|-----------|----------|
| `git add` | `git hash-object` |
| `git commit` | `git write-tree` + `git commit-tree` |
| `git log` | `git rev-list` |
| `git branch` | `git update-ref` |

### Advanced Specifiers

```bash
git show :/fix                        # Last commit with "fix" in message
git log @{u}..                        # Unpushed commits
git show HEAD^{tree}                  # Tree of HEAD
git rev-parse HEAD@{"1 week ago"}     # Reflog time travel
```

👉 **Mnemonic:** BLOB = file content / TREE = directory / COMMIT = snapshot / TAG = bookmark. Plumbing = engine / Porcelain = dashboard.

---

## 🧠 KEY TAKEAWAYS

- **4 git objects:** Blob (file), Tree (folder), Commit (snapshot), Tag (bookmark)
- **Same content = same SHA-1 hash** — automatic deduplication
- **Plumbing = engine parts, Porcelain = driving controls**
- **`@{u}`** = upstream tracking branch (e.g., `origin/main`)
- **You can manually create a commit** with `write-tree` + `commit-tree` + `update-ref`

---

**Next: [18-reflog.md](18-reflog.md)**
