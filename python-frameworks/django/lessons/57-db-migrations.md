# 📘 Django Phase 06 — Lesson 07: Database Migrations & Backups

> 🎯 **Goal**: Manage schema changes safely, write data migrations, and implement backup/restore strategies.

## 📖 Concepts

### Migration Operations

| Operation | SQL | Use Case |
|-----------|-----|----------|
| `migrations.CreateModel` | `CREATE TABLE` | New model |
| `migrations.AddField` | `ALTER TABLE ADD COLUMN` | New field |
| `migrations.RemoveField` | `ALTER TABLE DROP COLUMN` | Remove field |
| `migrations.AlterField` | `ALTER TABLE ALTER COLUMN` | Change field type |
| `migrations.AddIndex` | `CREATE INDEX` | Add database index |
| `migrations.RunSQL` | Custom SQL | Raw SQL operations |
| `migrations.RunPython` | Python function | Data migration |

### Data Migrations
```python
# Generated with: python manage.py makemigrations --empty myapp --name populate_slugs

from django.db import migrations

def populate_slugs(apps, schema_editor):
    Post = apps.get_model('myapp', 'Post')
    for post in Post.objects.all():
        post.slug = post.title.lower().replace(' ', '-')
        post.save(update_fields=['slug'])

def reverse(apps, schema_editor):
    pass  # No reverse — irreversible migration

class Migration(migrations.Migration):
    dependencies = [('myapp', '0002_add_slug_field')]
    operations = [
        migrations.RunPython(populate_slugs, reverse),
    ]
```

### Safe Migration Practices

| Practice | Why |
|----------|-----|
| One logical change per migration | Easier to rollback |
| Add nullable columns first | Avoid locking large tables |
| Use `--fake-initial` | Skip if table already exists |
| Backup before migrating | Rollback if migration fails |
| Test on staging first | Catch issues before prod |
| Avoid `RunSQL` if possible | ORM handles DB differences |

### Backup Strategies

| Type | Frequency | Retention | Tool |
|------|-----------|-----------|------|
| Full DB dump | Daily | 30 days | `pg_dump` |
| WAL archiving | Continuous | 7 days | PostgreSQL |
| Incremental | Hourly | 7 days | `pg_dump --format=custom` |
| Monthly archive | Monthly | 12 months | `pg_dump` + S3 |

### Backup & Restore
```bash
# Backup
pg_dump -h localhost -U myapp myapp_db > backup_$(date +%Y%m%d).sql
gzip backup_*.sql
aws s3 cp backup_*.sql.gz s3://backups/

# Restore
gunzip -c backup_20240115.sql.gz | psql -h localhost -U myapp myapp_db
```

### ADHD-Friendly Summary
```
makemigrations → detect changes
migrate → apply changes
RunPython → data migrations
pg_dump → backup
Backup before every deploy!
```

## 🛠️ Code

```bash
# backup.sh — automated backup script
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="myapp"
DB_USER="myapp"

# Create backup
pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/${DB_NAME}_$TIMESTAMP.sql.gz

# Upload to S3
aws s3 cp $BACKUP_DIR/${DB_NAME}_$TIMESTAMP.sql.gz s3://myapp-backups/daily/

# Cleanup old backups (older than 30 days)
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

# Notify
echo "Backup complete: ${DB_NAME}_$TIMESTAMP.sql.gz"
```

## 🧪 Practice

1. Create a migration that adds a `slug` field to Post
2. Write a data migration (RunPython) to populate slugs
3. Create a reversible migration
4. Write a backup script with pg_dump + S3 upload
5. Restore from a backup and verify data integrity

## 🧠 Key Takeaways

- One migration per logical change — easier to rollback
- Data migrations use `apps.get_model()`, not direct imports
- Always test migrations on staging first
- Backup before every deployment
- Monitor migration time — large tables need special handling
- Use `--fake` sparingly — it marks migration as applied without running it
