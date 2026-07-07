"""Integration: Full production deployment — combines all Phase 06 concepts."""
import json
import time
import random
import os
from datetime import datetime
from collections import defaultdict


# ======================== Core ========================
class HttpRequest:
    def __init__(self, method="GET", path="/", user=None):
        self.method = method
        self.path = path
        self.user = user or "anonymous"


class HttpResponse:
    def __init__(self, content="", status=200, headers=None):
        self.content = content
        self.status = status
        self.headers = headers or {}


# ======================== Settings Manager ========================
class Settings:
    def __init__(self, env: str = "production"):
        self.ENV = env
        self.DEBUG = self._bool("DEBUG", False)
        self.SECRET_KEY = os.environ.get("SECRET_KEY", "")
        self.ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "example.com").split(",")
        self.DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://user:pass@localhost:5432/db")
        self.REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/1")
        self.SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
        self.EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.example.com")
        self.STORAGE_BACKEND = os.environ.get("STORAGE_BACKEND", "s3")
        self.validate()

    def _bool(self, key: str, default: bool) -> bool:
        val = os.environ.get(key, str(default)).lower()
        return val in ("true", "1", "yes")

    def validate(self) -> list[str]:
        issues = []
        if not self.DEBUG and not self.SECRET_KEY:
            issues.append("CRITICAL: SECRET_KEY not set")
        if not self.DEBUG and not self.ALLOWED_HOSTS:
            issues.append("CRITICAL: ALLOWED_HOSTS empty")
        if not self.DATABASE_URL.startswith("postgres"):
            issues.append("WARNING: Using non-PostgreSQL database in production")
        return issues


# ======================== Deployment Pipeline ========================
class DeployStage:
    def __init__(self, name: str, duration: float = 0.0):
        self.name = name
        self.duration = duration
        self.status = "pending"
        self.output: list[str] = []

    def run(self) -> bool:
        self.status = "running"
        t0 = time.time()
        time.sleep(random.uniform(0.1, 0.3))
        self.duration = time.time() - t0
        success = random.random() > 0.05  # 95% success
        self.status = "passed" if success else "failed"
        return success


class DeployPipeline:
    def __init__(self, version: str):
        self.version = version
        self.stages: list[DeployStage] = []
        self.started_at = datetime.now().isoformat()
        self.completed_at = ""

    def add_stage(self, stage: DeployStage):
        self.stages.append(stage)

    def run(self) -> dict:
        results = []
        all_passed = True
        for stage in self.stages:
            success = stage.run()
            icon = "✅" if success else "❌"
            results.append(f"   {icon} {stage.name} ({stage.duration:.2f}s)")
            if not success:
                all_passed = False
                break
        self.completed_at = datetime.now().isoformat()
        return {
            "version": self.version,
            "success": all_passed,
            "stages": results,
            "duration": sum(s.duration for s in self.stages),
        }


# ======================== Health Check ========================
class HealthChecker:
    def __init__(self):
        self.services: dict[str, bool] = {}

    def check_all(self) -> dict:
        self.services = {
            "database": self._check_db(),
            "redis": self._check_redis(),
            "celery": self._check_celery(),
            "disk": self._check_disk(),
            "memory": self._check_memory(),
        }
        return self.services

    def _check_db(self) -> bool:
        time.sleep(0.02)
        return True
    def _check_redis(self) -> bool:
        time.sleep(0.02)
        return True
    def _check_celery(self) -> bool:
        time.sleep(0.02)
        return random.random() > 0.1
    def _check_disk(self) -> bool:
        return True
    def _check_memory(self) -> bool:
        return True


# ======================== Logging ========================
class ProductionLogger:
    def __init__(self):
        self.logs: list[dict] = []

    def log(self, level: str, message: str, **extra):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            **extra,
        }
        self.logs.append(entry)
        if level in ("ERROR", "CRITICAL"):
            print(f"   [{level}] {message}")

    def error_count(self) -> int:
        return len([l for l in self.logs if l["level"] in ("ERROR", "CRITICAL")])


# ======================== Deploy Simulation ========================
print("=" * 60)
print("🚀 PRODUCTION DEPLOYMENT — FULL INTEGRATION DEMO")
print("=" * 60)

# --- Settings validation ---
print("\n1. Production settings validation:")
os.environ["SECRET_KEY"] = "prod-secret-abc123"
os.environ["ALLOWED_HOSTS"] = "example.com,www.example.com"
os.environ["DATABASE_URL"] = "postgres://user:pass@prod-db:5432/blog"
os.environ["REDIS_URL"] = "redis://redis:6379/1"
os.environ["SENTRY_DSN"] = "https://key@sentry.io/project"

settings = Settings("production")
issues = settings.validate()
print(f"   Environment: {settings.ENV}")
print(f"   DEBUG: {settings.DEBUG}")
print(f"   DB: {settings.DATABASE_URL[:30]}...")
if issues:
    for issue in issues:
        print(f"   ⚠ {issue}")
else:
    print("   ✅ All settings valid")

# --- Deployment pipeline ---
print("\n2. Deployment pipeline:")
pipeline = DeployPipeline("v2.5.0")
pipeline.add_stage(DeployStage("Pull images"))
pipeline.add_stage(DeployStage("Run migrations"))
pipeline.add_stage(DeployStage("Collect static"))
pipeline.add_stage(DeployStage("Restart web servers"))
pipeline.add_stage(DeployStage("Restart Celery workers"))
pipeline.add_stage(DeployStage("Health check"))

result = pipeline.run()
print(f"\n   Version: {result['version']}")
for stage_result in result['stages']:
    print(stage_result)
print(f"\n   Total duration: {result['duration']:.2f}s")
print(f"   {'✅ DEPLOY SUCCESS' if result['success'] else '❌ DEPLOY FAILED'}")

# --- Health check ---
print("\n3. Health checks:")
checker = HealthChecker()
health = checker.check_all()
for service, healthy in health.items():
    icon = "✅" if healthy else "❌"
    print(f"   {icon} {service}: {'healthy' if healthy else 'unhealthy'}")

# --- Load balancing ---
print("\n4. Load balancing (3 instances):")
instances = ["web-01", "web-02", "web-03"]
for inst in instances:
    cpu = random.uniform(20, 80)
    mem = random.uniform(30, 70)
    reqs = random.randint(100, 500)
    print(f"   {inst}: CPU={cpu:.1f}%, MEM={mem:.1f}%, Requests={reqs}/min")

# --- Logging ---
print("\n5. Production logging:")
logger = ProductionLogger()
logger.log("INFO", "Server started", port=8000, workers=4)
logger.log("INFO", "Request completed", method="GET", path="/posts/", status=200, duration_ms=45)
logger.log("WARNING", "Slow query detected", query_time=0.32, table="posts")
logger.log("ERROR", "Database connection timeout", retry=1, max_retries=3)

# --- Monitoring dashboard ---
print("\n6. Production monitoring dashboard:")
dashboard = {
    "requests_per_minute": "1,234",
    "avg_response_time": "42ms",
    "p95_response_time": "120ms",
    "error_rate": "0.02%",
    "active_users": "342",
    "db_connections": "8/20",
    "celery_queue_size": "15",
    "cache_hit_rate": "94.5%",
    "disk_usage": "65%",
    "uptime": "14d 6h 32m",
}
for metric, value in dashboard.items():
    print(f"   {metric:25s}: {value}")

# --- Runbook ---
print("\n7. Production runbook:")
runbook = [
    ("Deploy", "docker compose up -d --build"),
    ("Rollback", "docker compose up -d web_previous"),
    ("Scale up", "docker compose up -d --scale web=5"),
    ("Migrate DB", "docker compose run --rm web python manage.py migrate"),
    ("Backup DB", "pg_dump -h localhost blog > backup.sql"),
    ("Restore DB", "psql blog < backup.sql"),
    ("Check logs", "docker compose logs -f --tail=100 web"),
    ("Restart Celery", "docker compose restart celery"),
    ("Health check", "curl -f http://localhost:8000/health/"),
    ("SSL renew", "certbot renew"),
]
for step, cmd in runbook:
    print(f"   {step:15s}: {cmd}")

print("\n✅ Production Deployment Integration Complete")
print(f"\n{'='*60}")
print("DEPLOYMENT SUMMARY")
print(f"{'='*60}")
print(f"  Environment:    {settings.ENV}")
print(f"  Version:        {result['version']}")
print(f"  Status:         {'PASSED' if result['success'] else 'FAILED'}")
print(f"  Duration:       {result['duration']:.2f}s")
print(f"  Services:       {sum(1 for v in health.values() if v)}/5 healthy")
print(f"  Log errors:     {logger.error_count()}")
print(f"  Settings:       {0 if not issues else len(issues)} issues")
