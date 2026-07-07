# 📦 Alembic Migrations
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Schema versioning, migration files, upgrade/downgrade, autogenerate.

## Install & Init

```bash
pip install alembic
alembic init alembic
```

Configure `alembic.ini`:

```ini
sqlalchemy.url = sqlite:///./app.db
```

In `alembic/env.py`:

```python
from app.models import Base
target_metadata = Base.metadata
```

<!-- 🔧 Alembic compares your SQLAlchemy models against the current DB and generates migration scripts. -->

## Create a Migration

```bash
alembic revision --autogenerate -m "Create users table"
```

Generated file:
```python
def upgrade():
    op.create_table("users", Column("id", Integer, primary_key=True), ...)

def downgrade():
    op.drop_table("users")
```

## Run Migrations

```bash
alembic upgrade head   # Apply all pending
alembic downgrade -1   # Roll back one step
alembic history        # Show migration history
alembic current        # Show current revision
```

## Key Commands

| Command | Effect |
|---------|--------|
| `alembic upgrade head` | Apply all pending |
| `alembic downgrade -1` | Roll back one |
| `alembic downgrade revision_id` | Roll back to specific |
| `alembic history` | List all revisions |
| `alembic current` | Show current |

## Common Operations

```python
# Add column
op.add_column("users", Column("bio", Text))

# Drop column
op.drop_column("users", "bio")

# Add index
op.create_index("ix_users_email", "users", ["email"])

# Rename table
op.rename_table("old_name", "new_name")
```

## Run the Code

```bash
python code/12-alembic-migrations.py
```
