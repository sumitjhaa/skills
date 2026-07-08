# ⚡ Celery — Distributed Task Queue

15 lessons covering Celery for async task processing, from basics to production workflows.

All code runs in eager mode — no broker required.

## Structure

| Phase | Focus | Lessons | Practice |
|-------|-------|---------|----------|
| 01 | Core & Production | 01–15 | ✅ |

## How to Use

```bash
# Run a lesson's code
python code/01-celery-basics.py

# Read the corresponding lesson
lessons/01-celery-basics.md

# Do the practice exercises
practice/phase01-exercises.md
```

## Topics

Celery basics, task configuration, running workers, result backend, calling tasks (delay/apply_async/signatures), task routing, task binding & inheritance, periodic tasks (Celery beat), workflows (chains/groups/chords), error handling & retries, task signals, monitoring (Flower), Django integration, FastAPI integration, full async pipeline.

Requires Celery (`pip install celery`). All code files run standalone with eager mode.
