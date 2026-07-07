# 📘 Django Phase 05 — Lesson 05: Custom Management Commands

> 🎯 **Goal**: Build CLI tools for your Django project — data cleanup, fixtures, backups, maintenance.

## 📖 Concepts

### What Are Management Commands?
Python scripts that run via `python manage.py <command>`. They have access to Django's ORM, settings, and environment.

### Basic Structure
```
myapp/
  management/
    __init__.py
    commands/
      __init__.py
      cleanup_sessions.py
      generate_fixtures.py
```

### Command Components

| Component | Description |
|-----------|-------------|
| `BaseCommand` | Base class for all commands |
| `help` | Short description shown in `--help` |
| `add_arguments(parser)` | Define CLI arguments |
| `handle(*args, **options)` | Main logic — return `None` or a string |
| `self.stdout.write()` | Print to stdout (respects `--verbosity`) |
| `self.stderr.write()` | Print to stderr |

### Argument Types

| Parser Method | CLI Flag | Example |
|---------------|----------|---------|
| `add_argument('--days', type=int)` | `--days=30` | Optional int |
| `add_argument('--dry-run', action='store_true')` | `--dry-run` | Boolean flag |
| `add_argument('name', type=str)` | (positional) | Required arg |
| `add_argument('--file', type=argparse.FileType('r'))` | `--file=data.json` | File input |

### Best Practices
- Always support `--dry-run` for destructive operations
- Use `--verbosity` to control output level
- Handle errors gracefully with `CommandError`
- Return meaningful exit codes (0 = success)

### ADHD-Friendly Summary
```
class Command(BaseCommand):
    help = "description"
    def add_arguments(self, parser): ...
    def handle(self, **options): ...
python manage.py my_command --dry-run --days=30
```

## 🛠️ Code

```python
# myapp/management/commands/cleanup_sessions.py
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.contrib.sessions.models import Session

class Command(BaseCommand):
    help = 'Cleans up expired sessions'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=30)
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **options):
        cutoff = timezone.now() - timezone.timedelta(days=options['days'])
        expired = Session.objects.filter(expire_date__lt=cutoff)
        count = expired.count()

        if options['dry_run']:
            self.stdout.write(f'Would delete {count} expired sessions')
            return

        expired.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} sessions'))

# Usage: python manage.py cleanup_sessions --days=60 --dry-run
```

## 🧪 Practice

1. Create a `generate_fixtures` command with `--users=10 --posts=50`
2. Create a `backup_db` command that dumps data to a JSON file
3. Add `--compress` flag that gzips the backup
4. Create a `send_test_email` command that takes an email address
5. Add `--dry-run` support to a destructive command

## 🧠 Key Takeaways

- Commands live in `myapp/management/commands/`
- Use `self.stdout.write()` for output (not `print()`)
- Always support `--dry-run` for destructive operations
- `BaseCommand` handles `--help`, `--verbosity`, `--skip-checks` automatically
- Commands have full access to Django ORM and settings
