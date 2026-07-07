# 🔄 Alembic Migrations
<!-- ⏱️ 20 min | 🟡 Intermediate -->

**What You'll Learn:** Schema versioning, migration chains, upgrade/downgrade, Alembic workflow.

## What is Alembic?

Alembic is a lightweight database migration tool for SQLAlchemy. It tracks schema changes as a chain of versioned migration scripts.

## Migration Structure

Each migration has:
- `revision` — unique ID (hash)
- `down_revision` — parent revision ID (or `None` for first)
- `upgrade()` — apply the changes
- `downgrade()` — roll back the changes

## Common Operations

```python
# Add column
def upgrade():
    op.add_column("users", Column("bio", Text))

def downgrade():
    op.drop_column("users", "bio")

# Rename column
def upgrade():
    op.alter_column("users", "username", new_column_name="full_name")

# Create/drop table
def upgrade():
    op.create_table("posts", Column("id", Integer, primary_key=True), ...)
def downgrade():
    op.drop_table("posts")
```

## Typical Workflow

```bash
alembic init alembic               # Create migration directory
alembic revision --autogenerate -m "add bio"  # Auto-detect changes
alembic upgrade head               # Apply all pending
alembic downgrade -1               # Rollback one step
```

<!-- 🤔 Autogenerate compares your model metadata with the actual DB schema. -->

## Run the Code

```bash
python code/11-alembic-migrations.py
```
