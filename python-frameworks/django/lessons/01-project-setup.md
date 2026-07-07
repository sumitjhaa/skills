# 🏗️ Project Setup & Structure
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Create a Django project, understand the file structure, configure settings, and run the dev server.

## Create Project

```bash
# Install Django
pip install django

# Create project
django-admin startproject myproject

# File structure
myproject/
├── manage.py          # CLI tool for Django commands
├── myproject/
│   ├── __init__.py    # Makes this a Python package
│   ├── settings.py    # Configuration (DB, apps, middleware, etc.)
│   ├── urls.py        # Top-level URL routing
│   ├── asgi.py        # ASGI entry point (async)
│   └── wsgi.py        # WSGI entry point (sync/production)

# Create an app (a module within your project)
python manage.py startapp blog

# New structure
blog/
├── __init__.py
├── admin.py           # Register models for admin panel
├── apps.py            # App configuration
├── migrations/        # Database migration files
├── models.py          # Data models (database tables)
├── tests.py           # Tests
└── views.py           # Request handlers
```

## Run the Server

```bash
python manage.py runserver  # http://127.0.0.1:8000
```

## Settings Basics

```python
# myproject/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # Add your app here
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
```

## Code Example

```python
"""Project setup verification script."""
import django
import sys

print(f"Django version: {django.get_version()}")
print(f"Python version: {sys.version}")

# Verify Django can create a project
from django.core.management import call_command
from django.conf import settings

# This simulates what happens when you run startproject
print("\n✅ Django is ready. Create your project with:")
print("  django-admin startproject myproject")
print("  cd myproject")
print("  python manage.py startapp myapp")
print("  python manage.py runserver")
```

## Key Points
- `startproject` creates the outer project (settings, urls, WSGI)
- `startapp` creates an inner app (models, views, admin)
- Always add your app to `INSTALLED_APPS` in settings
- `manage.py` is your Swiss Army knife — run, migrate, shell, test
