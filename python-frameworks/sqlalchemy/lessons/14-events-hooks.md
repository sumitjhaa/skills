# 🔔 Events & Hooks
<!-- ⏱️ 20 min | 🔴 Advanced -->

**What You'll Learn:** Mapper events, session events, connection events, event-based auditing.

## Mapper Events

```python
from sqlalchemy import event

@event.listens_for(User, "before_insert")
def set_created_at(mapper, connection, target):
    target.created_at = datetime.utcnow()
```

## Session Events

```python
@event.listens_for(Session, "before_commit")
def validate_before_commit(session):
    for obj in session.new:
        if isinstance(obj, User) and not obj.email:
            raise ValueError("Email required")
```

## Connection Events

```python
@event.listens_for(engine, "before_execute")
def log_queries(conn, clause, multiparams, params):
    print(f"SQL: {clause}")
```

## Common Use Cases

- **Audit logs** — `before_update` / `before_insert` to track changes
- **Validation** — `before_commit` to enforce business rules
- **Timestamps** — auto-set `created_at` / `updated_at`
- **Caching** — `after_load` to populate calculated fields

## Registering Events

```python
@event.listens_for(Model, "event_name")
def handler(mapper, connection, target):
    ...

# For session events:
@event.listens_for(Session, "event_name")
def handler(session):
    ...
```

<!-- 🧠 Events are synchronous — keep handlers fast to avoid slowing down operations. -->

## Run the Code

```bash
python code/14-events-hooks.py
```
