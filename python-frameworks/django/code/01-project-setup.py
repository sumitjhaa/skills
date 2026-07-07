"""Verify Django installation and project setup."""
import django
import sys

print(f"Django version: {django.get_version()}")
print(f"Python version: {sys.version}")
print("\n✅ Django is ready.")

print("\nNext steps:")
print("  django-admin startproject myproject")
print("  cd myproject")
print("  python manage.py startapp myapp")
print("  python manage.py runserver")
