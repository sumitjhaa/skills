"""Settings management: env vars, multiple settings files, 12-factor app."""
import os
import json
from pathlib import Path


# ======================== 12-Factor App ========================

class TwelveFactorConfig:
    """Implements 12-factor app config via environment variables."""

    @staticmethod
    def str_env(key: str, default: str = "") -> str:
        return os.environ.get(key, default)

    @staticmethod
    def bool_env(key: str, default: bool = False) -> bool:
        val = os.environ.get(key, str(default)).lower()
        return val in ("true", "1", "yes", "y")

    @staticmethod
    def int_env(key: str, default: int = 0) -> int:
        try:
            return int(os.environ.get(key, default))
        except (ValueError, TypeError):
            return default

    @staticmethod
    def list_env(key: str, default: list = None, separator: str = ",") -> list:
        val = os.environ.get(key, "")
        if not val:
            return default or []
        return [v.strip() for v in val.split(separator) if v.strip()]

    @staticmethod
    def dict_env(key: str, default: dict = None) -> dict:
        val = os.environ.get(key, "{}")
        try:
            return json.loads(val)
        except json.JSONDecodeError:
            return default or {}

    @staticmethod
    def path_env(key: str, default: str = "") -> Path:
        return Path(os.environ.get(key, default))


# ======================== Settings Module ========================

class BaseSettings:
    """Base settings shared by all environments."""
    DEBUG = False
    SECRET_KEY = "change-me-in-production"
    ALLOWED_HOSTS: list[str] = []
    INSTALLED_APPS: list[str] = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # Third-party
        "rest_framework",
        "corsheaders",
        # Local
        "blog",
        "accounts",
    ]
    MIDDLEWARE: list[str] = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "myapp",
            "USER": "myapp",
            "PASSWORD": "",
            "HOST": "localhost",
            "PORT": 5432,
        }
    }
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
        }
    }


class DevelopmentSettings(BaseSettings):
    DEBUG = True
    SECRET_KEY = "dev-secret-key-not-for-production"
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "*"]
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db.sqlite3",
        }
    }
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


class StagingSettings(BaseSettings):
    DEBUG = False
    ALLOWED_HOSTS = ["staging.myapp.com"]
    DATABASES = {
        "default": {
            **BaseSettings.DATABASES["default"],
            "PASSWORD": TwelveFactorConfig.str_env("DB_PASSWORD", ""),
            "HOST": TwelveFactorConfig.str_env("DB_HOST", "staging-db"),
        }
    }


class ProductionSettings(BaseSettings):
    DEBUG = False
    SECRET_KEY = TwelveFactorConfig.str_env("SECRET_KEY", "")
    ALLOWED_HOSTS = TwelveFactorConfig.list_env("ALLOWED_HOSTS", ["myapp.com"])
    DATABASES = {
        "default": {
            **BaseSettings.DATABASES["default"],
            "PASSWORD": TwelveFactorConfig.str_env("DB_PASSWORD", ""),
            "HOST": TwelveFactorConfig.str_env("DB_HOST", "prod-db"),
        }
    }
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": TwelveFactorConfig.str_env("REDIS_URL", "redis://redis:6379/1"),
        }
    }
    STATIC_ROOT = "/var/www/static"
    MEDIA_ROOT = "/var/www/media"


# ======================== Settings Factory ========================

class SettingsFactory:
    @staticmethod
    def get_settings(env: str = None):
        env = env or TwelveFactorConfig.str_env("DJANGO_ENV", "development")
        mapping = {
            "development": DevelopmentSettings,
            "staging": StagingSettings,
            "production": ProductionSettings,
        }
        cls = mapping.get(env, DevelopmentSettings)
        instance = cls()
        # Validate
        issues = SettingsFactory.validate(instance)
        return instance, issues

    @staticmethod
    def validate(settings) -> list[str]:
        issues = []
        if settings.DEBUG and settings.SECRET_KEY == "dev-secret-key-not-for-production":
            pass  # OK for dev
        if not settings.DEBUG and settings.SECRET_KEY in ("", "change-me-in-production"):
            issues.append("SECRET_KEY is not set for non-debug environment!")
        if not settings.DEBUG and not settings.ALLOWED_HOSTS:
            issues.append("ALLOWED_HOSTS is empty!")
        return issues


# ======================== .env file parser ========================

class DotEnvParser:
    """Parse .env files."""
    @staticmethod
    def parse(content: str) -> dict:
        env_vars = {}
        for line in content.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, val = line.partition("=")
                key = key.strip()
                val = val.strip().strip("'").strip('"')
                env_vars[key] = val
        return env_vars

    @staticmethod
    def generate(env_vars: dict) -> str:
        lines = []
        for k, v in env_vars.items():
            if " " in v or "#" in v:
                v = f'"{v}"'
            lines.append(f"{k}={v}")
        return "\n".join(lines)


# ======================== Demo ========================
print("=== Settings Management Demo ===\n")

# --- 12-factor helpers ---
os.environ["DATABASE_URL"] = "postgres://user:pass@prod:5432/myapp"
os.environ["ALLOWED_HOSTS"] = "myapp.com,www.myapp.com"
os.environ["SECRET_KEY"] = "prod-secret-12345"

print("1. 12-factor config helpers:")
print(f"   ALLOWED_HOSTS: {TwelveFactorConfig.list_env('ALLOWED_HOSTS')}")
print(f"   DB_URL: {TwelveFactorConfig.str_env('DATABASE_URL', 'not-set')[:40]}...")

# --- Different environments ---
print("\n2. Environment settings:")
for env in ["development", "staging", "production"]:
    settings, issues = SettingsFactory.get_settings(env)
    print(f"\n   {env}:")
    print(f"     DEBUG={settings.DEBUG}, ALLOWED_HOSTS={settings.ALLOWED_HOSTS[:2]}")
    if issues:
        for issue in issues:
            print(f"     ⚠ {issue}")

# --- .env file ---
print("\n3. .env file generation:")
env_vars = {
    "SECRET_KEY": "my-secret-key-12345",
    "DEBUG": "False",
    "ALLOWED_HOSTS": "myapp.com,www.myapp.com",
    "DB_NAME": "myapp",
    "DB_USER": "myapp",
    "DB_PASSWORD": "secure-password-here",
    "DB_HOST": "localhost",
    "DB_PORT": "5432",
    "REDIS_URL": "redis://localhost:6379/1",
    "EMAIL_HOST": "smtp.sendgrid.net",
    "EMAIL_PORT": "587",
    "EMAIL_HOST_USER": "apikey",
    "EMAIL_HOST_PASSWORD": "sendgrid-api-key",
}
env_content = DotEnvParser.generate(env_vars)
print(env_content[:400] + "...")

# --- Settings structure ---
print("\n4. Recommended settings structure:")
structure = """
myapp/
  settings/
    __init__.py          # → from .production import *  (or dev)
    base.py              # Base settings (shared)
    development.py       # Dev overrides
    staging.py           # Staging overrides
    production.py        # Production overrides
.env                    # Local env vars (gitignored)
.env.example            # Template (committed)
"""
print(structure)

# --- Validation ---
print("5. Common misconfigurations:")
misconfigs = [
    ("DEBUG=True in production", "High"),
    ("SECRET_KEY hardcoded in settings", "Critical"),
    ("ALLOWED_HOSTS = ['*']", "Medium"),
    ("SQLite in production", "High"),
    ("CORS_ORIGIN_ALLOW_ALL = True", "Medium"),
    ("No HTTPS redirect", "High"),
]
for issue, severity in misconfigs:
    print(f"   [{severity}] {issue}")
