# 📘 Django Phase 03 — Lesson 07: Custom User Models

> 🎯 **Goal**: Replace the built-in User model with a custom one using `AbstractUser` or `AbstractBaseUser`.

## 📖 Concepts

### Three Approaches

| Approach | When to Use |
|----------|-------------|
| Profile model (OneToOne) | Existing project, don't want to change User |
| `AbstractUser` | New project, need extra fields + all built-in auth |
| `AbstractBaseUser` | Need different auth (email login, phone login) |

### AbstractUser (Recommended for 90% of projects)
**Extends** the built-in User with your own fields.

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
```

Must set **before first migration**:
```python
# settings.py
AUTH_USER_MODEL = 'myapp.User'
```

### AbstractBaseUser (Full Control)
Start from scratch. Define only what you need.

```python
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError('Email required')
        user = self.model(email=self.normalize_email(email), **extra)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # login field (not username)
    REQUIRED_FIELDS = ['display_name']
```

### When to Customize
You should customize if:
- You want users to **login with email** (no username)
- You need **extra required fields** during registration
- You want a **different unique identifier** (phone number, etc.)

Do NOT customize if:
- You already have production data with the default User model
- You only need a bio/avatar (use Profile instead)

### Migration Considerations
If changing `AUTH_USER_MODEL` after any migration:
- **Cannot** use a simple migration
- Requires a **database reset** or complex multi-step migration
- **Always** set `AUTH_USER_MODEL` before the first migration

### Referencing the User Model
Always use `get_user_model()` or `settings.AUTH_USER_MODEL`:

```python
from django.contrib.auth import get_user_model

User = get_user_model()

# For ForeignKey
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
```

### ADHD-Friendly Summary
```
AbstractUser (90%):    extend built-in + add fields
AbstractBaseUser:      from scratch, define everything

Set BEFORE first migrate: AUTH_USER_MODEL = 'app.User'
Reference: get_user_model() or settings.AUTH_USER_MODEL
```

## 🛠️ Code

```python
# AbstractUser approach
class User(AbstractUser):
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)

# Admin
from django.contrib import admin
from .models import User

admin.site.register(User)  # works with AbstractUser too
```

## 🧪 Practice

1. Create a custom User with `AbstractUser` (bio, phone, location)
2. Set `AUTH_USER_MODEL` in settings.py
3. Create a superuser and verify login works
4. Reference the User model in a Post model using `settings.AUTH_USER_MODEL`
5. Bonus: Create an email-login User with `AbstractBaseUser`

## 🧠 Key Takeaways

- `AbstractUser` → extend built-in (add fields). 90% of projects.
- `AbstractBaseUser` → rewrite auth from scratch (email login, custom identifiers)
- **Must** set `AUTH_USER_MODEL` before first migration
- Always reference via `get_user_model()` or `settings.AUTH_USER_MODEL`
- If project is already live → use Profile model instead of custom User
