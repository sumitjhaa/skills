"""Database migrations & backups: migration operations, data migrations, backup strategies."""
import json
import time
import random
from datetime import datetime
from collections import defaultdict


# ======================== Migration Simulation ========================

class MigrationOperation:
    """Represents a single migration operation."""
    def __init__(self, name: str, sql: str, reverse_sql: str = ""):
        self.name = name
        self.sql = sql
        self.reverse_sql = reverse_sql
        self.duration = 0.0

    def run(self, direction: str = "forward") -> bool:
        t0 = time.time()
        time.sleep(random.uniform(0.05, 0.2))
        self.duration = time.time() - t0
        return True

    def to_dict(self) -> dict:
        return {"name": self.name, "sql": self.sql[:40] + "...", "duration": round(self.duration, 3)}


class Migration:
    """Represents a Django migration file."""
    def __init__(self, name: str, app_label: str, dependencies: list[str] = None):
        self.name = name
        self.app_label = app_label
        self.dependencies = dependencies or []
        self.operations: list[MigrationOperation] = []
        self.applied = False
        self.applied_at: str = ""

    def add_operation(self, op: MigrationOperation):
        self.operations.append(op)

    def apply(self) -> bool:
        for op in self.operations:
            if not op.run("forward"):
                return False
        self.applied = True
        self.applied_at = datetime.now().isoformat()
        return True

    def rollback(self) -> bool:
        for op in reversed(self.operations):
            if op.reverse_sql:
                time.sleep(0.05)
        self.applied = False
        self.applied_at = ""
        return True

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "app": self.app_label,
            "operations": [op.to_dict() for op in self.operations],
            "applied": self.applied,
        }


class MigrationTracker:
    """Tracks all migrations like django_migrations table."""
    def __init__(self):
        self.migrations: dict[str, Migration] = {}
        self.history: list[str] = []

    def register(self, migration: Migration):
        self.migrations[migration.name] = migration

    def migrate(self, target: str = None) -> list[str]:
        results = []
        for name, migration in sorted(self.migrations.items()):
            if target and name > target:
                break
            if not migration.applied:
                success = migration.apply()
                status = "✅" if success else "❌"
                results.append(f"  {status} {migration.app_label}.{migration.name}")
                self.history.append(f"{datetime.now().isoformat()} - Applied {migration.name}")
        return results

    def show_migrations(self) -> list[dict]:
        return [m.to_dict() for m in self.migrations.values()]


# ======================== Data Migration ========================

class DataMigration:
    """Simulates a data migration (RunPython)."""
    @staticmethod
    def populate_slugs(apps, schema_editor):
        """Forward: fill empty slug fields."""
        time.sleep(0.1)
        return {"updated": 42}

    @staticmethod
    def reverse_populate_slugs(apps, schema_editor):
        """Reverse: clear slug fields."""
        time.sleep(0.05)
        return {"cleared": 42}


# ======================== Backup Strategy ========================

class Backup:
    """Represents a database backup."""
    def __init__(self, name: str, backup_type: str = "full"):
        self.name = name
        self.backup_type = backup_type
        self.size_mb = random.randint(50, 500)
        self.created_at = datetime.now().isoformat()
        self.duration = 0.0
        self.location = f"s3://backups/{name}.sql.gz"

    def create(self) -> dict:
        t0 = time.time()
        time.sleep(random.uniform(0.3, 0.8))
        self.duration = time.time() - t0
        return {
            "name": self.name,
            "type": self.backup_type,
            "size_mb": self.size_mb,
            "duration_s": round(self.duration, 2),
            "location": self.location,
            "success": True,
        }

    def restore(self) -> bool:
        time.sleep(random.uniform(0.5, 1.0))
        return True


class BackupSchedule:
    """Backup schedule configuration."""
    def __init__(self):
        self.schedules = {
            "full": {"frequency": "daily", "time": "03:00 UTC", "retention": 30},
            "incremental": {"frequency": "hourly", "retention": 7},
            "weekly": {"frequency": "weekly", "day": "Sunday", "time": "04:00 UTC", "retention": 12},
            "monthly": {"frequency": "monthly", "day": 1, "time": "05:00 UTC", "retention": 12},
        }

    def get(self, backup_type: str) -> dict:
        return self.schedules.get(backup_type, {})


# ======================== Demo ========================
print("=== Database Migrations & Backups Demo ===\n")

# --- Create migrations ---
print("1. Migration operations:")

migration_001 = Migration("0001_initial", "blog")
migration_001.add_operation(MigrationOperation(
    "CreatePostModel",
    "CREATE TABLE blog_post (id SERIAL, title VARCHAR(200), content TEXT);",
    "DROP TABLE blog_post;",
))
migration_001.add_operation(MigrationOperation(
    "CreateCommentModel",
    "CREATE TABLE blog_comment (id SERIAL, post_id INT, text TEXT);",
    "DROP TABLE blog_comment;",
))

migration_002 = Migration("0002_add_slug", "blog", dependencies=["0001_initial"])
migration_002.add_operation(MigrationOperation(
    "AddFieldSlug",
    "ALTER TABLE blog_post ADD COLUMN slug VARCHAR(200) UNIQUE;",
    "ALTER TABLE blog_post DROP COLUMN slug;",
))
migration_002.add_operation(MigrationOperation(
    "PopulateSlugs",
    "UPDATE blog_post SET slug = lower(title);",
    "",
))

migration_003 = Migration("0003_add_indexes", "blog", dependencies=["0002_add_slug"])
migration_003.add_operation(MigrationOperation(
    "AddIndex",
    "CREATE INDEX idx_post_created ON blog_post(created_at);",
    "DROP INDEX idx_post_created;",
))

# --- Show and run migrations ---
print("   Registered migrations:")
for m in [migration_001, migration_002, migration_003]:
    print(f"     {m.app_label}.{m.name} ({len(m.operations)} ops)")

print("\n2. Applying migrations:")
tracker = MigrationTracker()
tracker.register(migration_001)
tracker.register(migration_002)
tracker.register(migration_003)

results = tracker.migrate()
for r in results:
    print(r)

print("\n3. Migration status:")
for m in tracker.show_migrations():
    status = "✅ Applied" if m["applied"] else "☐ Pending"
    print(f"   {m['app']}.{m['name']}: {status}")

# --- Rollback ---
print("\n4. Rollback last migration:")
migration_003.rollback()
print(f"   {migration_003.name}: rolled back, applied={migration_003.applied}")

# --- Backups ---
print("\n5. Database backups:")
schedule = BackupSchedule()
print("   Backup schedule:")
for bt, cfg in schedule.schedules.items():
    freq = cfg.get("frequency", "")
    retention = cfg.get("retention", "N/A")
    print(f"     • {bt:15s} every {freq:10s} retention: {retention}d")

backup = Backup("prod-blog-2024-01-15-full", "full")
result = backup.create()
print(f"\n   Creating backup: {result['name']}")
print(f"     Size: {result['size_mb']}MB, Duration: {result['duration_s']}s")
print(f"     Location: {result['location']}")

# --- Migration best practices ---
print("\n6. Migration best practices:")
practices = [
    ("Test locally first", "Run migrate on a copy of prod DB"),
    ("One operation per migration", "Easier to rollback"),
    ("Add indexes in separate migration", "Can take long on large tables"),
    ("Data migrations use RunPython", "Must be reversible"),
    ("Avoid default on large tables", "ALTER TABLE ... ADD COLUMN with DEFAULT locks table"),
    ("Use --fake-initial", "Skip initial migration if table already exists"),
    ("Rollback before deploy", "Always have a reverse migration"),
    ("Backup before migrating", "In case something goes wrong"),
]
for practice, detail in practices:
    print(f"   • {practice}: {detail}")
