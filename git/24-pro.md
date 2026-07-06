# 24️⃣ PRO CONVENTIONS & WORKFLOWS

⏱️ **Time:** ~15 min | 🏁 **TL;DR:** main is always deployable. Commit messages: 50-char subject, blank line, 72-char body — explain WHAT and WHY, not HOW. Use `.gitattributes` for line endings and `includeIf` in gitconfig to auto-switch identity.

## 🔁 LAST TIME...

In [23-maintenance.md](23-maintenance.md), you learned maintenance commands.

---

### Branching Strategies

| Feature | GitHub Flow | Git Flow | Trunk-Based |
|---------|------------|----------|-------------|
| Main branch | Always deployable | Protected release | Always deployable |
| Other branches | Feature branches only | develop, feature, release, hotfix | Almost none |
| Branch lifetime | Hours to days | Days to weeks | Hours |
| Complexity | Low | High | Very low |
| Best for | Web apps, startups | Mobile apps, releases | Microservices, DevOps |

### Commit Message 7 Rules

1. Separate subject from body with blank line
2. Limit subject to **50 characters**
3. Capitalize the subject
4. No period at end of subject
5. **Imperative mood:** "Add" not "Added"
6. Wrap body at **72 characters**
7. Explain **WHAT and WHY**, not HOW

### `.gitattributes`

```
* text=auto                     # Normalize line endings
*.png binary                    # Binary files (never convert)
package-lock.json -merge        # Never auto-merge
.gitattributes export-ignore    # Exclude from git archive
```

### Conditional Config (`includeIf`)

```ini
[includeIf "gitdir:~/work/"]
  path = ~/.gitconfig-work
```

👉 **Mnemonic:** GitHub Flow = main is sacred, branches are cheap, PRs are the gateway. 50/72 = subject/body rule for commit messages.

---

## 🧠 KEY TAKEAWAYS

- **GitHub Flow:** `main` is always deployable, feature branches + PRs
- **Commit messages:** 50-char subject, blank line, 72-char body — explain WHAT and WHY
- **`.gitattributes`** normalizes line endings and sets merge strategies
- **`includeIf`** in `~/.gitconfig` auto-switches identity by directory
- **Pick ONE branching strategy** and stick with it — switching creates chaos

---

**Next: [25-workflows.md](25-workflows.md) — Production-grade workflows combining everything you've learned.**
