# 📘 Django Phase 02 — Lesson 07: Migrations Deep Dive

> 🎯 **Goal**: Understand Django migrations — creating, applying, inspecting, and squashing.

## 📖 Concepts

### Migration Flow
```
Change models.py → python manage.py makemigrations
                  → creates migration file (0002_xxx.py)
                  → python manage.py migrate
                  → executes SQL against DB
                  → updates django_migrations table
```

### Common Migration Commands

| Command | Purpose |
|---------|---------|
| `makemigrations` | Detect model changes, create migration |
| `migrate` | Apply pending migrations |
| `sqlmigrate app 0002` | Show SQL (dry run) |
| `showmigrations` | List all migrations with status |
| `migrate app 0001` | Rollback to specific migration |
| `makemigrations --empty app` | Create empty (data) migration |

### Migration Operations

| Operation | Purpose |
|-----------|---------|
| `CreateModel(name, fields)` | New model |
| `DeleteModel(name)` | Remove model |
| `AddField(model, field)` | New column |
| `RemoveField(model, name)` | Drop column |
| `AlterField(model, field)` | Change column type |
| `RenameField(model, old, new)` | Rename column |
| `RenameModel(old, new)` | Rename table |
| `AlterModelTable(model, table)` | Change table name |
| `AlterModelOptions(model, options)` | Meta/options |
| `AddIndex(model, index)` | Add DB index |
| `RemoveIndex(model, name)` | Drop index |

### Data Migrations
For backfilling data:

```python
# Generated with: makemigrations --empty app
from django.db import migrations

def set_default_slug(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    for post in Post.objects.all():
        post.slug = post.title.lower().replace(' ', '-')
        post.save()

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(set_default_slug),
    ]
```

### Migration Best Practices
1. **Never edit production migrations** — create a new one
2. Test migrations on a copy of prod data
3. Keep migrations **small and focused** (one change per migration)
4. Use `sqlmigrate` to review SQL before running
5. **Squash** old migrations periodically: `makemigrations --squash-name app`

### ADHD-Friendly Summary
```
models.py → makemigrations → migration file → migrate → DB

Commands:
  makemigrations    detect → create
  migrate           apply
  sqlmigrate        show SQL
  showmigrations    list status
  
Always create new migrations (never edit applied ones)
```

## 🛠️ Code

```python
# Creating initial models
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

class Author(models.Model):
    name = models.CharField(max_length=100)

# Running
# python manage.py makemigrations
# python manage.py migrate

# Adding fields later
# Add to models.py: likes = models.IntegerField(default=0)
# python manage.py makemigrations
# python manage.py migrate

# Data migration
def add_initial_data(apps, schema_editor):
    Author = apps.get_model('blog', 'Author')
    Author.objects.create(name='Admin')

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(add_initial_data),
    ]
```

## 🧪 Practice

1. Start with `Post(title, content)`. Create migration.
2. Add `Post.likes` (IntegerField, default=0). Create + apply.
3. Rename `content` to `body`. Create migration, check SQL with `sqlmigrate`.
4. Create a data migration that sets `likes=10` for all existing posts.
5. Squash the first 3 migrations into one.

## 🧠 Key Takeaways

- Migrations are **version control for your database schema**
- `makemigrations` diffs current models vs last migration
- `migrate` replays pending migrations in order
- Data migrations use `apps.get_model()` (not direct import)
- Squash old migrations to keep project clean
- Never delete a migration that's been applied to production
