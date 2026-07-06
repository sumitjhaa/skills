# 0️⃣ WHAT IS GIT?

---

⏱️ **Time:** ~3 min | 🏁 **TL;DR:** Git is a time machine for your code. Every commit is a photograph of your entire project you can revisit forever.

---

## 🎯 THE BIG IDEA

**Git tracks file changes with snapshots (commits), not file copies.**

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   WORKING    │ ──→ │   STAGING    │ ──→ │  REPOSITORY  │
│  DIRECTORY   │     │  AREA (Index)│     │   (.git/)    │
│  (Your files)│     │  (Next commit)│     │  (All history)│
└──────────────┘     └──────────────┘     └──────────────┘
```

- **Working Directory** — the files you see and edit on disk
- **Staging Area** — files you've marked for the next snapshot
- **Repository** — all snapshots (commits) ever saved, stored in `.git/`

---

## 🕰️ TIME TRAVEL ANALOGY

- Every `git commit` = a photograph of your entire project
- You can jump to ANY photograph, anytime
- Branches = "what if" timelines that don't affect the main story

👉 **Mnemonic:** Git = **G**reat **I**nstant **T**ime-machine

---

## 🧠 KEY TAKEAWAYS

- Git stores **snapshots** (full-project copies), not file diffs
- The **three states** are Working → Staging → Repository
- Every commit is **permanent** and retrievable
- `.git/` IS the repository — delete it, lose all history
- Branches let you experiment without breaking the main timeline

---

> **Next: [01-setup.md](01-setup.md) — Install and configure git**
