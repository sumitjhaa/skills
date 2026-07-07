"""Migrations with Alembic — schema versioning concepts (simulated)."""
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean, Text

engine = create_engine("sqlite:///:memory:", echo=False)
metadata = MetaData()

schema_state = [
    ("id", "INTEGER", True),
    ("username", "VARCHAR(50)", False),
    ("email", "VARCHAR(100)", False),
]

print("=== Alembic Migrations ===\n")

class Migration:
    def __init__(self, rev: str, down_rev: str, description: str):
        self.rev = rev
        self.down_rev = down_rev
        self.description = description

    def upgrade(self, cols): pass
    def downgrade(self, cols): pass

class AddBioColumn(Migration):
    def __init__(self):
        super().__init__("abc123", None, "Add bio column to users")
    def upgrade(self, cols):
        cols.append(("bio", "TEXT", False))
    def downgrade(self, cols):
        cols.pop()

class AddAgeDefault(Migration):
    def __init__(self):
        super().__init__("def456", "abc123", "Add age column with default")
    def upgrade(self, cols):
        cols.append(("age", "INTEGER", False))
    def downgrade(self, cols):
        cols.pop()

class RenameUsername(Migration):
    def __init__(self):
        super().__init__("ghi789", "def456", "Rename username to full_name")
    def upgrade(self, cols):
        for i, (name, typ, pk) in enumerate(cols):
            if name == "username":
                cols[i] = ("full_name", typ, pk)
                break
    def downgrade(self, cols):
        for i, (name, typ, pk) in enumerate(cols):
            if name == "full_name":
                cols[i] = ("username", typ, pk)
                break

migrations = [AddBioColumn(), AddAgeDefault(), RenameUsername()]

print("Migration history:")
for m in migrations:
    print(f"  {m.rev} <- {m.down_rev or 'init'} : {m.description}")

print(f"\nApplying all migrations...")
for m in migrations:
    m.upgrade(schema_state)
    print(f"  ✅ {m.rev}: {m.description}")

print(f"\nSchema after migrations:")
for name, typ, pk in schema_state:
    pk_mark = " PK" if pk else ""
    print(f"  {name:15s} {typ:20s}{pk_mark}")

print(f"\nRolling back {migrations[2].rev}...")
migrations[2].downgrade(schema_state)
print(f"Schema after rollback:")
for name, typ, pk in schema_state:
    pk_mark = " PK" if pk else ""
    print(f"  {name:15s} {typ:20s}{pk_mark}")

print(f"\nTypical Alembic commands:")
print("  alembic init alembic")
print("  alembic revision --autogenerate -m 'add bio'")
print("  alembic upgrade head")
print("  alembic downgrade -1")
print("  alembic history")
