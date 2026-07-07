"""Custom management commands: BaseCommand, arguments, stdout/stderr."""
from typing import Any, Optional
from argparse import ArgumentParser
import sys
import time
import random


# ======================== Management Command Framework ========================

class CommandError(Exception):
    """Exception for management command errors."""
    pass


class BaseCommand:
    """Simulates Django's BaseCommand for management commands."""
    help = ""
    requires_system_checks = True

    def __init__(self):
        self.parser = ArgumentParser(prog=self.__class__.__name__)
        self.add_arguments(self.parser)
        self.stdout = []
        self.stderr = []

    def add_arguments(self, parser: ArgumentParser):
        """Override to add command arguments."""
        pass

    def handle(self, *args, **options) -> str | None:
        """Override with command logic. Return a string or None."""
        raise NotImplementedError("Subclasses must implement handle()")

    def print(self, msg: str, style: str = "default"):
        """Simulate self.stdout.write()."""
        self.stdout.append(msg)

    def error(self, msg: str):
        """Simulate self.stderr.write()."""
        self.stderr.append(msg)

    def run_from_argv(self, argv: list[str]) -> str:
        """Parse args and execute the command."""
        try:
            parsed = self.parser.parse_args(argv[2:])  # skip script + command name
            options = vars(parsed)
            result = self.handle(**options)
            return "\n".join(self.stdout) + (f"\n{result}" if result else "")
        except CommandError as e:
            self.error(str(e))
            return f"Error: {e}"
        except Exception as e:
            self.error(f"Unexpected error: {e}")
            return f"Error: {e}"


# ======================== Concrete Commands ========================

class CleanupExpiredSessions(BaseCommand):
    help = "Cleans up expired sessions from the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="Delete sessions older than this many days (default: 30)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be deleted without deleting",
        )

    def handle(self, days: int, dry_run: bool, **options):
        expired_count = random.randint(10, 100)
        if dry_run:
            self.print(f"[DRY RUN] Would delete {expired_count} sessions older than {days} days")
        else:
            self.print(f"Deleted {expired_count} sessions older than {days} days")
        return f"Done (dry_run={dry_run}, days={days})"


class GenerateFixtures(BaseCommand):
    help = "Generate sample data for development/testing."

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            default=10,
            help="Number of users to create (default: 10)",
        )
        parser.add_argument(
            "--posts",
            type=int,
            default=50,
            help="Number of posts to create (default: 50)",
        )
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing data before generating",
        )

    def handle(self, users: int, posts: int, flush: bool, **options):
        if flush:
            self.print("Flushing existing data...")
        self.print(f"Generating {users} users...")
        time.sleep(0.05)
        self.print(f"Generating {posts} posts...")
        time.sleep(0.1)
        return f"Created {users} users and {posts} posts"


class BackupDatabase(BaseCommand):
    help = "Creates a database backup dump."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            type=str,
            default="backup.json",
            help="Output file path (default: backup.json)",
        )
        parser.add_argument(
            "--compress",
            action="store_true",
            help="Compress the backup with gzip",
        )

    def handle(self, output: str, compress: bool, **options):
        self.print(f"Backing up database to {output}...")
        time.sleep(0.2)
        size = random.randint(1, 100)
        self.print(f"Backup complete: {size}MB")
        if compress:
            self.print(f"Compressed: {size // 2}MB")
        return f"Backup saved to {output}"


# ======================== Demo ========================
print("=== Management Commands Demo ===\n")

commands = {
    "cleanup_sessions": CleanupExpiredSessions(),
    "generate_fixtures": GenerateFixtures(),
    "backup_db": BackupDatabase(),
}

# --- Cleanup sessions (dry-run) ---
print("1. python manage.py cleanup_sessions --days=60 --dry-run")
cmd = commands["cleanup_sessions"]
output = cmd.run_from_argv(["manage.py", "cleanup_sessions", "--days=60", "--dry-run"])
print(f"   {output}")

# --- Cleanup sessions (actual) ---
print("\n2. python manage.py cleanup_sessions --days=7")
cmd = commands["cleanup_sessions"]
output = cmd.run_from_argv(["manage.py", "cleanup_sessions", "--days=7"])
print(f"   {output}")

# --- Generate fixtures ---
print("\n3. python manage.py generate_fixtures --users=5 --posts=20 --flush")
cmd = commands["generate_fixtures"]
output = cmd.run_from_argv(["manage.py", "generate_fixtures", "--users=5", "--posts=20", "--flush"])
print(f"   {output}")

# --- Backup database ---
print("\n4. python manage.py backup_db --output=prod_backup.json --compress")
cmd = commands["backup_db"]
output = cmd.run_from_argv(["manage.py", "backup_db", "--output=prod_backup.json", "--compress"])
print(f"   {output}")

# --- Help text check ---
print("\n5. Command help texts:")
for name, cmd in commands.items():
    print(f"   {name}: {cmd.help}")
