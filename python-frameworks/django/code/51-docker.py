"""Docker for Django: Dockerfile, docker-compose, multi-stage builds."""
import os
import subprocess
import sys


# ======================== Simulation of Docker Build ========================

class Dockerfile:
    """Simulates generating/validating a Dockerfile."""
    @staticmethod
    def generate_python_version() -> str:
        return f"{sys.version_info.major}.{sys.version_info.minor}"

    @staticmethod
    def validate(lines: list[str]) -> list[str]:
        errors = []
        if not any(l.startswith("FROM") for l in lines):
            errors.append("Missing FROM instruction")
        if not any("EXPOSE" in l for l in lines):
            errors.append("Missing EXPOSE instruction")
        if not any("CMD" in l or "ENTRYPOINT" in l for l in lines):
            errors.append("Missing CMD or ENTRYPOINT")
        if not any("COPY" in l for l in lines):
            errors.append("Missing COPY instruction")
        return errors


class DockerComposeService:
    """Represents a service in docker-compose.yml."""
    def __init__(self, name: str, image: str = None, build: str = None):
        self.name = name
        self.image = image
        self.build = build
        self.ports: list[str] = []
        self.environment: dict[str, str] = {}
        self.env_file: str = ""
        self.volumes: list[str] = []
        self.depends_on: list[str] = []
        self.command: str = ""
        self.restart: str = "unless-stopped"
        self.healthcheck: dict = {}

    def yaml_lines(self, indent: int = 2) -> list[str]:
        pad = " " * indent
        lines = [f"{pad}{self.name}:"]
        if self.build:
            lines.append(f"{pad}  build: {self.build}")
        if self.image:
            lines.append(f"{pad}  image: {self.image}")
        if self.command:
            lines.append(f"{pad}  command: {self.command}")
        if self.ports:
            lines.append(f"{pad}  ports:")
            for p in self.ports:
                lines.append(f"{pad}    - '{p}'")
        if self.environment:
            lines.append(f"{pad}  environment:")
            for k, v in self.environment.items():
                lines.append(f"{pad}    {k}={v}")
        if self.env_file:
            lines.append(f"{pad}  env_file: {self.env_file}")
        if self.volumes:
            lines.append(f"{pad}  volumes:")
            for v in self.volumes:
                lines.append(f"{pad}    - {v}")
        if self.depends_on:
            lines.append(f"{pad}  depends_on:")
            for d in self.depends_on:
                lines.append(f"{pad}    - {d}")
        if self.restart:
            lines.append(f"{pad}  restart: {self.restart}")
        return lines


# ======================== Multi-stage Build ========================

class MultiStageBuild:
    """Represents a multi-stage Docker build."""
    def __init__(self):
        self.stages: list[dict] = []

    def add_stage(self, name: str, base: str, commands: list[str]):
        self.stages.append({"name": name, "base": base, "commands": commands})

    def generate(self) -> str:
        lines = []
        for stage in self.stages:
            lines.append(f"# Stage: {stage['name']}")
            lines.append(f"FROM {stage['base']} AS {stage['name']}")
            for cmd in stage['commands']:
                lines.append(f"RUN {cmd}")
            lines.append("")
        return "\n".join(lines)


# ======================== Demo ========================
print("=== Docker for Django Demo ===\n")

# --- Dockerfile validation ---
print("1. Dockerfile validation:")
good_dockerfile = [
    "FROM python:3.12-slim",
    "WORKDIR /app",
    "COPY requirements.txt .",
    "RUN pip install --no-cache-dir -r requirements.txt",
    "COPY . .",
    "EXPOSE 8000",
    "CMD ['gunicorn', 'myproject.wsgi:application', '--bind', '0.0.0.0:8000']",
]
bad_dockerfile = [
    "FROM python:3.12-slim",
    "RUN pip install django",
]

errors = Dockerfile.validate(good_dockerfile)
print(f"   Good Dockerfile errors: {errors}")
errors = Dockerfile.validate(bad_dockerfile)
print(f"   Bad Dockerfile errors: {errors}")

# --- Multi-stage build ---
print("\n2. Multi-stage build:")
build = MultiStageBuild()
build.add_stage("builder", "python:3.12-slim", [
    "pip install --no-cache-dir poetry",
    "poetry export -f requirements.txt --output requirements.txt",
])
build.add_stage("runtime", "python:3.12-slim", [
    "apt-get update && apt-get install -y --no-install-recommends libpq-dev",
    "pip install --no-cache-dir -r requirements.txt",
])
print(f"   Generated {len(build.stages)} stages")

# --- Docker Compose ---
print("\n3. Docker Compose services:")
web = DockerComposeService("web", build=".")
web.ports = ["8000:8000"]
web.environment = {"DJANGO_SETTINGS_MODULE": "myproject.settings.production"}
web.env_file = ".env"
web.volumes = [".:/app", "static_volume:/app/static"]
web.depends_on = ["db", "redis", "celery"]
web.command = "gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --workers=4"

db = DockerComposeService("db", image="postgres:16-alpine")
db.environment = {"POSTGRES_DB": "myapp", "POSTGRES_USER": "myapp", "POSTGRES_PASSWORD": "${DB_PASSWORD}"}
db.volumes = ["postgres_data:/var/lib/postgresql/data"]
db.healthcheck = {"test": "pg_isready -U myapp", "interval": "10s"}

redis = DockerComposeService("redis", image="redis:7-alpine")
redis.ports = ["6379:6379"]

celery = DockerComposeService("celery", build=".")
celery.command = "celery -A myproject worker -l info"
celery.depends_on = ["redis", "db"]

for service in [web, db, redis, celery]:
    print(f"\n   {service.name}:")
    for line in service.yaml_lines():
        print(f"      {line}")

# --- Build context ---
print("\n4. .dockerignore patterns:")
ignore_patterns = [
    "*.pyc", "__pycache__/", ".git", ".env", ".venv",
    "media/", "staticfiles/", "*.sqlite3", "Dockerfile",
]
for p in ignore_patterns:
    print(f"   - {p}")

print("\n5. Common Docker commands:")
commands = [
    "docker compose build",
    "docker compose up -d",
    "docker compose exec web python manage.py migrate",
    "docker compose exec web python manage.py collectstatic --noinput",
    "docker compose logs -f web",
    "docker compose down",
]
for cmd in commands:
    print(f"   $ {cmd}")
