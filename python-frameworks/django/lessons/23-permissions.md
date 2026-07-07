# 📘 Django Phase 03 — Lesson 03: Permissions & Authorization

> 🎯 **Goal**: Control access with `login_required`, `permission_required`, and object-level checks.

## 📖 Concepts

### Three Levels of Authorization

| Level | Mechanism | Use Case |
|-------|-----------|----------|
| View | `@login_required` | Any authenticated user |
| View + Permission | `@permission_required('app.action')` | Specific permission check |
| Object-level | Custom check | User owns the object |

### Login Required
```python
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def dashboard(request):
    ...
```

**CBV equivalent**: `LoginRequiredMixin`

### Permission Required
```python
from django.contrib.auth.decorators import permission_required

@permission_required('blog.add_post')
def create_post(request):
    ...
```

**CBV**: `PermissionRequiredMixin` with `permission_required = 'blog.add_post'`

### Permission Names
Format: `app_label.codename`

Default codenames per model: `add_modelname`, `change_modelname`, `delete_modelname`, `view_modelname`

```python
# Check in template
{% if perms.blog.add_post %}
    <a href="{% url 'create_post' %}">New Post</a>
{% endif %}
```

### Staff & Superuser
```python
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_panel(request):
    ...

# Superuser-only
@user_passes_test(lambda u: u.is_superuser)
def superadmin(request):
    ...
```

### Object-Level Permissions
```python
# In the model
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def can_edit(self, user):
        return user == self.author or user.has_perm('blog.change_post')

# In the view
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post.can_edit(request.user):
        raise PermissionDenied
    ...
```

### User.has_perm() checks
```python
user.has_perm('blog.add_post')          # single
user.has_perms(['blog.add_post', ...])   # multiple (AND)
```

### ADHD-Friendly Summary
```
@login_required              → any auth user
@permission_required('perm') → specific permission
@staff_member_required       → is_staff=True
object.can_edit(user)        → per-object check
```

## 🛠️ Code

```python
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@permission_required('blog.add_post')
def create_post(request):
    ...

@permission_required('blog.change_post')
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        raise PermissionDenied
    ...
```

## 🧪 Practice

1. Protect a view with `@login_required`
2. Protect a view with `@permission_required`
3. Create an object-level permission check (only author can edit)
4. Show/hide UI based on `perms` in templates
5. Test: anonymous user → 302, wrong permission → 403, ok → 200

## 🧠 Key Takeaways

- `login_required` checks `is_authenticated` — simple gate
- `permission_required` checks specific permission — fine-grained
- Object-level checks require custom logic (Django doesn't provide by default)
- Superuser bypasses all permission checks
- Always check permissions in views, not just in templates
