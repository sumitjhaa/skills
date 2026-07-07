"""Alembic migrations: version tracking, upgrade/downgrade, autogenerate."""
from typing import Any
from datetime import datetime
import json


# ======================== Simulated Alembic ========================

class Migration:
    """Represents a single migration revision."""
    def __init__(self, revision: str, down_revision: str | None, message: str):
        self.revision = revision
        self.down_revision = down_revision
        self.message = message
        self.up_ops: list[dict] = []
        self.down_ops: list[dict] = []

    def add_op(self, direction: str, op_type: str, **kwargs):
        target = self.up_ops if direction == "up" else self.down_ops
        target.append({"type": op_type, **kwargs})


class MigrationEngine:
    """Tracks applied migrations and runs upgrade/downgrade."""
    def __init__(self):
        self.migrations: dict[str, Migration] = {}
        self.applied: list[str] = []
        self.head: str | None = None

    def register(self, migration: Migration):
        self.migrations[migration.revision] = migration
        self.head = migration.revision

    def upgrade(self, target: str | None = None) -> list[str]:
        """Run pending migrations up to target (or head)."""
        if target is None:
            target = self.head
        applied = []
        current = self._current_revision()

        # Build path from current to target
        revisions = self._path_to(current, target)
        for rev in revisions:
            mig = self.migrations[rev]
            self._run_migration(mig, "up")
            self.applied.append(rev)
            applied.append(rev)
        return applied

    def downgrade(self, target: str) -> list[str]:
        """Roll back migrations to target revision."""
        reverted = []
        while self.applied and self.applied[-1] != target:
            rev = self.applied.pop()
            mig = self.migrations[rev]
            self._run_migration(mig, "down")
            reverted.append(rev)
        return reverted

    def _current_revision(self) -> str | None:
        return self.applied[-1] if self.applied else None

    def _path_to(self, current: str | None, target: str | None) -> list[str]:
        """BFS from current to target."""
        path = []
        rev = target
        while rev and rev != current:
            path.insert(0, rev)
            mig = self.migrations.get(rev)
            if mig is None:
                break
            rev = mig.down_revision
        return path

    def _run_migration(self, migration: Migration, direction: str):
        ops = migration.up_ops if direction == "up" else migration.down_ops
        for op in ops:
            pass  # In real Alembic, this executes SQL

    def history(self) -> list[dict]:
        return [
            {"revision": m.revision, "down": m.down_revision, "message": m.message, "applied": m.revision in self.applied}
            for m in self.migrations.values()
        ]

    def show(self, revision: str) -> Migration | None:
        return self.migrations.get(revision)


# ======================== Schema State ========================

class SchemaState:
    """Tracks the current database schema."""
    def __init__(self):
        self.tables: dict[str, list[dict]] = {}
        self.columns: dict[str, dict[str, str]] = {}
        self.indexes: dict[str, list[str]] = {}

    def create_table(self, name: str, columns: dict[str, str]):
        self.tables[name] = []
        self.columns[name] = columns

    def drop_table(self, name: str):
        self.tables.pop(name, None)
        self.columns.pop(name, None)
        self.indexes.pop(name, None)

    def add_column(self, table: str, name: str, col_type: str):
        if table in self.columns:
            self.columns[table][name] = col_type

    def drop_column(self, table: str, name: str):
        if table in self.columns:
            self.columns[table].pop(name, None)

    def add_index(self, table: str, column: str):
        if table not in self.indexes:
            self.indexes[table] = []
        if column not in self.indexes[table]:
            self.indexes[table].append(column)

    def __repr__(self):
        lines = ["SchemaState:"]
        for table, cols in self.columns.items():
            lines.append(f"  {table}:")
            for name, typ in cols.items():
                idx = " [index]" if table in self.indexes and name in self.indexes[table] else ""
                lines.append(f"    - {name}: {typ}{idx}")
        return "\n".join(lines)


# ======================== Define Migrations ========================

engine = MigrationEngine()
schema = SchemaState()

# Migration 1: Initial users table
m1 = Migration("001_initial", None, "Create users table")
m1.add_op("up", "create_table", name="users", columns={"id": "integer", "username": "varchar(50)", "email": "varchar(100)", "password": "varchar(255)"})
m1.add_op("down", "drop_table", name="users")
engine.register(m1)

# Migration 2: Add posts table
m2 = Migration("002_posts", "001_initial", "Create posts table")
m2.add_op("up", "create_table", name="posts", columns={"id": "integer", "title": "varchar(200)", "content": "text", "user_id": "integer", "created_at": "datetime"})
m2.add_op("down", "drop_table", name="posts")
engine.register(m2)

# Migration 3: Add bio column to users
m3 = Migration("003_add_bio", "002_posts", "Add bio column to users")
m3.add_op("up", "add_column", table="users", name="bio", type="text")
m3.add_op("down", "drop_column", table="users", name="bio")
engine.register(m3)

# Migration 4: Add email index
m4 = Migration("004_email_index", "003_add_bio", "Add index on users.email")
m4.add_op("up", "add_index", table="users", column="email")
m4.add_op("down", "drop_index", table="users", column="email")
engine.register(m4)


# ======================== Apply Schema Changes ========================

def apply_up(migration: Migration):
    for op in migration.up_ops:
        if op["type"] == "create_table":
            schema.create_table(op["name"], op["columns"])
        elif op["type"] == "drop_table":
            schema.drop_table(op["name"])
        elif op["type"] == "add_column":
            schema.add_column(op["table"], op["name"], op["type"])
        elif op["type"] == "drop_column":
            schema.drop_column(op["table"], op["name"])
        elif op["type"] == "add_index":
            schema.add_index(op["table"], op["column"])


def apply_down(migration: Migration):
    for op in migration.down_ops:
        if op["type"] == "create_table":
            schema.create_table(op["name"], op["columns"])
        elif op["type"] == "drop_table":
            schema.drop_table(op["name"])
        elif op["type"] == "add_column":
            schema.add_column(op["table"], op["name"], op["type"])
        elif op["type"] == "drop_column":
            schema.drop_column(op["table"], op["name"])
        elif op["type"] == "add_index":
            schema.add_index(op["table"], op["column"])


# ======================== Demo ========================
print("=== Alembic Migrations Demo ===\n")

# Initial state
print("1. Initial schema (empty):")
print(f"   {schema}\n")

# Run all migrations
print("2. Running all migrations (upgrade to head):")
current = engine._current_revision()
for revision in engine._path_to(current, engine.head):
    mig = engine.migrations[revision]
    print(f"   → Applying: {mig.revision} — {mig.message}")
    apply_up(mig)
    engine.applied.append(revision)
print(f"\n   Schema after upgrade:\n{schema}\n")

# Show history
print("3. Migration history:")
for h in engine.history():
    status = "✅" if h["applied"] else "⬜"
    print(f"   {status} {h['revision']:20s} ↓{h['down'] or 'None':15s} {h['message']}")

# Rollback
print("\n4. Rollback one migration (downgrade to 003):")
reverted = []
while engine.applied and engine.applied[-1] != "003_add_bio":
    rev = engine.applied.pop()
    mig = engine.migrations[rev]
    print(f"   → Reverting: {mig.revision} — {mig.message}")
    apply_down(mig)
    reverted.append(rev)

print(f"\n   Schema after rollback:\n{schema}")

# Current state
print(f"\n5. Current revision: {engine._current_revision()}")
print(f"   Applied count: {len(engine.applied)}")
print(f"   Pending: {len(engine.migrations) - len(engine.applied)}")
