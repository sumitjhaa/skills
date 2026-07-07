"""Deployment strategies: VPS, PaaS, environment configs, health checks."""
import json
import time
import random
import os


# ======================== Environment Manager ========================

class EnvManager:
    """Manages environment-specific settings."""
    ENVIRONMENTS = {
        "development": {
            "DEBUG": True,
            "ALLOWED_HOSTS": ["localhost", "127.0.0.1"],
            "DATABASE_URL": "sqlite:///db.sqlite3",
            "CACHE_BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "EMAIL_BACKEND": "django.core.mail.backends.console.EmailBackend",
        },
        "staging": {
            "DEBUG": False,
            "ALLOWED_HOSTS": ["staging.myapp.com"],
            "DATABASE_URL": "postgres://user:pass@staging-db:5432/myapp",
            "CACHE_BACKEND": "django.core.cache.backends.redis.RedisCache",
            "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        },
        "production": {
            "DEBUG": False,
            "ALLOWED_HOSTS": ["myapp.com", "www.myapp.com"],
            "DATABASE_URL": "postgres://user:pass@prod-db:5432/myapp",
            "CACHE_BACKEND": "django.core.cache.backends.redis.RedisCache",
            "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
            "SECRET_KEY": "${SECRET_KEY}",  # from env variable
        },
    }

    @staticmethod
    def get_config(env: str) -> dict:
        return EnvManager.ENVIRONMENTS.get(env, EnvManager.ENVIRONMENTS["development"])

    @staticmethod
    def validate_env(env: str) -> list[str]:
        warnings = []
        config = EnvManager.get_config(env)
        if env == "production":
            if config["DEBUG"]:
                warnings.append("DEBUG must be False in production")
            if "${" in str(config):
                warnings.append("Use environment variables for secrets, not hardcoded values")
            if "localhost" in config["ALLOWED_HOSTS"]:
                warnings.append("Remove localhost from production ALLOWED_HOSTS")
        return warnings


# ======================== Deployment Platform ========================

class DeploymentTarget:
    """Represents a deployment platform."""
    def __init__(self, name: str, platform_type: str):
        self.name = name
        self.platform_type = platform_type
        self.config: dict = {}

    def deploy(self, version: str) -> dict:
        """Simulate deployment to this target."""
        t0 = time.time()
        steps = self._deploy_steps()
        time.sleep(random.uniform(0.5, 1.5))
        duration = time.time() - t0
        return {
            "target": self.name,
            "version": version,
            "duration": round(duration, 2),
            "steps": steps,
            "success": True,
        }

    def _deploy_steps(self) -> list[str]:
        steps = {
            "VPS": [
                "git pull origin main",
                "pip install -r requirements.txt",
                "python manage.py migrate",
                "python manage.py collectstatic --noinput",
                "systemctl restart gunicorn",
                "systemctl restart celery",
                "nginx -t && systemctl reload nginx",
            ],
            "Heroku": [
                "git push heroku main",
                "heroku run python manage.py migrate",
                "heroku run python manage.py collectstatic",
            ],
            "Railway": [
                "Push to GitHub → auto-deploy",
                "Run migrations via deploy hook",
            ],
        }
        return steps.get(self.platform_type, ["Deploy application"])


# ======================== Health Check ========================

class HealthCheck:
    """Simulates a health check endpoint."""
    def __init__(self):
        self.checks: dict[str, bool] = {}

    def add_check(self, name: str, check_fn):
        self.checks[name] = check_fn

    def run_all(self) -> dict:
        results = {}
        all_healthy = True
        for name, check_fn in self.checks.items():
            try:
                healthy = check_fn()
                results[name] = {"healthy": healthy}
                if not healthy:
                    all_healthy = False
            except Exception as e:
                results[name] = {"healthy": False, "error": str(e)}
                all_healthy = False
        return {
            "status": "healthy" if all_healthy else "degraded",
            "checks": results,
        }


# ======================== WSGI Server Config ========================

class GunicornConfig:
    """Gunicorn configuration generator."""
    @staticmethod
    def generate(workers: int = 4, bind: str = "0.0.0.0:8000") -> dict:
        return {
            "bind": bind,
            "workers": workers,
            "worker_class": "sync",
            "timeout": 120,
            "keepalive": 5,
            "max_requests": 1000,
            "max_requests_jitter": 50,
            "accesslog": "/var/log/gunicorn/access.log",
            "errorlog": "/var/log/gunicorn/error.log",
            "loglevel": "info",
        }


class NginxConfig:
    """Nginx reverse proxy config generator."""
    @staticmethod
    def generate(domain: str, static_dir: str, media_dir: str) -> list[str]:
        return [
            f"server {{",
            f"    listen 80;",
            f"    server_name {domain};",
            f"    return 301 https://$server_name$request_uri;",
            f"}}",
            f"",
            f"server {{",
            f"    listen 443 ssl;",
            f"    server_name {domain};",
            f"",
            f"    ssl_certificate /etc/ssl/certs/{domain}.pem;",
            f"    ssl_certificate_key /etc/ssl/private/{domain}.key;",
            f"",
            f"    location /static/ {{",
            f"        alias {static_dir};",
            f"    }}",
            f"",
            f"    location /media/ {{",
            f"        alias {media_dir};",
            f"    }}",
            f"",
            f"    location / {{",
            f"        proxy_pass http://127.0.0.1:8000;",
            f"        proxy_set_header Host $host;",
            f"        proxy_set_header X-Real-IP $remote_addr;",
            f"        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;",
            f"        proxy_set_header X-Forwarded-Proto $scheme;",
            f"    }}",
            f"}}",
        ]


# ======================== Demo ========================
print("=== Deployment Strategies Demo ===\n")

# --- Environment configs ---
print("1. Environment configurations:")
for env_name in ["development", "staging", "production"]:
    config = EnvManager.get_config(env_name)
    warnings = EnvManager.validate_env(env_name)
    print(f"\n   {env_name}:")
    print(f"     DEBUG={config['DEBUG']}, DB={config['DATABASE_URL'][:15]}...")
    if warnings:
        for w in warnings:
            print(f"     ⚠ {w}")

# --- Deploy to different targets ---
print("\n2. Deployment targets:")
for name, ptype in [("My VPS", "VPS"), ("Heroku", "Heroku"), ("Railway", "Railway")]:
    target = DeploymentTarget(name, ptype)
    result = target.deploy("v2.1.0")
    print(f"\n   {name} ({ptype}):")
    print(f"     Duration: {result['duration']}s")
    for step in result['steps'][:3]:
        print(f"     • {step}")
    if len(result['steps']) > 3:
        print(f"     ... and {len(result['steps']) - 3} more steps")

# --- Gunicorn config ---
print("\n3. Gunicorn configuration:")
gunicorn = GunicornConfig.generate(workers=8, bind="0.0.0.0:8000")
for k, v in gunicorn.items():
    print(f"   {k}: {v}")

# --- Nginx config ---
print("\n4. Nginx configuration:")
nginx_lines = NginxConfig.generate("myapp.com", "/var/www/static", "/var/www/media")
for line in nginx_lines:
    print(f"   {line}")

# --- Health check ---
print("\n5. Health check:")
hc = HealthCheck()
hc.add_check("database", lambda: True)
hc.add_check("redis", lambda: True)
hc.add_check("celery", lambda: False)  # Simulated failure
hc.add_check("disk_space", lambda: True)

result = hc.run_all()
print(f"   Status: {result['status']}")
for name, check in result['checks'].items():
    icon = "✅" if check['healthy'] else "❌"
    print(f"     {icon} {name}")

print("\n6. Deployment checklist:")
checklist = [
    "DEBUG=False",
    "SECRET_KEY from env variable",
    "ALLOWED_HOSTS configured",
    "Database migrated",
    "Static files collected",
    "CORS configured",
    "HTTPS enabled",
    "Health check endpoint",
    "Logging configured",
    "Backup strategy in place",
]
for i, item in enumerate(checklist, 1):
    print(f"   {i:2d}. {'✅' if i <= 8 else '☐'} {item}")
