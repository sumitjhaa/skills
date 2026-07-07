# 📘 Django Phase 03 — Lesson 04: Groups & Custom Permissions

> 🎯 **Goal**: Organize users into groups and define custom permissions.

## 📖 Concepts

### Groups
Groups are collections of users with shared permissions. A user can belong to multiple groups.

```python
from django.contrib.auth.models import Group, Permission

# Create
editors = Group.objects.create(name='Editors')
admins = Group.objects.create(name='Admins')

# Add permissions
perm = Permission.objects.get(codename='add_post')
editors.permissions.add(perm)

# Assign user
user.groups.add(editors)

# Check
user.has_perm('blog.add_post')  # True (inherited from group)
```

### Permission Inheritance
```
User's permissions = own permissions + all group permissions
Superuser          = all permissions (bypasses checks)
```

### Custom Permissions (on the Model)
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    # ...

    class Meta:
        permissions = [
            ("can_publish", "Can publish posts"),
            ("can_feature", "Can feature posts"),
            ("can_archive", "Can archive posts"),
        ]
```

After adding custom permissions:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Managing Groups in Admin
```python
# admin.py
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

# Groups are already registered by default
# Add/remove users and permissions via admin UI
```

### Programmatic Group Management
```python
def assign_role(user, role):
    """Assign a predefined role to a user."""
    roles = {
        'editor': ['blog.add_post', 'blog.change_post', 'blog.can_publish'],
        'moderator': ['blog.can_feature', 'blog.can_archive'],
        'admin': ['blog.add_post', 'blog.change_post', 'blog.delete_post',
                   'blog.can_publish', 'blog.can_feature', 'blog.can_archive'],
    }
    group, _ = Group.objects.get_or_create(name=role.title())
    group.permissions.set(
        Permission.objects.filter(codename__in=roles[role])
    )
    user.groups.add(group)
```

### ADHD-Friendly Summary
```
Groups = permission bundles
User in multiple groups → union of all their permissions

Custom permissions: Meta.permissions = [...]
Then: makemigrations → migrate

Prefer groups over assigning perms to individual users!
```

## 🛠️ Code

```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Custom permission on model
class Article(models.Model):
    title = models.CharField(max_length=200)
    class Meta:
        permissions = [
            ("can_publish", "Can publish"),
            ("can_feature", "Can feature"),
        ]

# Assign to group
ct = ContentType.objects.get_for_model(Article)
perm = Permission.objects.get(content_type=ct, codename='can_publish')
editors = Group.objects.get(name='Editors')
editors.permissions.add(perm)

# Check
user.has_perm('myapp.can_publish')
```

## 🧪 Practice

1. Create groups: Editors, Writers, Moderators, Admins
2. Give each group different custom permissions
3. Create 4 users, assign each to a different group
4. Verify permission checks work per group
5. Write a test that group permissions are inherited correctly

## 🧠 Key Takeaways

- Groups = permission bundles for role-based access control (RBAC)
- Custom permissions in `Meta.permissions` require a migration
- One user can be in many groups (union of permissions)
- Use `user.get_group_permissions()` to see effective permissions
- Always use groups over assigning perms per-user (maintainable)
