"""Docker + Docker Compose: multi-stage builds, services, volumes, networking."""
from typing import Any
import json


# ======================== Dockerfile Generator ========================

class Dockerfile:
    """Generates Dockerfile content."""
    def __init__(self, base_image: str = "python:3.11-slim"):
        self.base = base_image
        self.stages: list[str] = []
        self._current_stage = 0

    def from_(self, image: str, as_name: str | None = None):
        line = f"FROM {image}"
        if as_name:
            line += f" AS {as_name}"
        self.stages.append(line)
        return self

    def workdir(self, path: str):
        self.stages.append(f"WORKDIR {path}")
        return self

    def copy(self, src: str, dst: str, from_stage: str | None = None):
        line = f"COPY "
        if from_stage:
            line += f"--from={from_stage} "
        line += f"{src} {dst}"
        self.stages.append(line)
        return self

    def run(self, command: str):
        self.stages.append(f"RUN {command}")
        return self

    def env(self, key: str, value: str):
        self.stages.append(f"ENV {key}={value}")
        return self

    def expose(self, port: int):
        self.stages.append(f"EXPOSE {port}")
        return self

    def cmd(self, command: list[str]):
        cmd_str = json.dumps(command)
        self.stages.append(f"CMD {cmd_str}")
        return self

    def entrypoint(self, command: list[str]):
        cmd_str = json.dumps(command)
        self.stages.append(f"ENTRYPOINT {cmd_str}")
        return self

    def install_packages(self, packages: list[str]):
        self.stages.append(f"RUN pip install --no-cache-dir {' '.join(packages)}")
        return self

    def generate(self) -> str:
        return "\n".join(self.stages)


class ComposeService:
    """A single service in docker-compose.yml."""
    def __init__(self, name: str, image: str = "", build: str | None = None):
        self.name = name
        self.image = image
        self.build = build
        self.ports: list[str] = []
        self.environment: dict[str, str] = {}
        self.volumes: list[str] = []
        self.depends_on: list[str] = []
        self.command: list[str] | None = None
        self.restart: str = "unless-stopped"
        self.healthcheck: dict | None = None

    def add_port(self, host_port: int, container_port: int, protocol: str = "tcp"):
        self.ports.append(f"{host_port}:{container_port}/{protocol}")
        return self

    def add_env(self, key: str, value: str):
        self.environment[key] = value
        return self

    def add_volume(self, host_path: str, container_path: str, mode: str = "rw"):
        self.volumes.append(f"{host_path}:{container_path}:{mode}")
        return self

    def depends(self, *services: str):
        self.depends_on.extend(services)
        return self

    def set_healthcheck(self, test: list[str], interval: str = "30s", timeout: str = "10s", retries: int = 3):
        self.healthcheck = {"test": test, "interval": interval, "timeout": timeout, "retries": retries}
        return self

    def to_dict(self) -> dict:
        service = {}
        if self.build:
            service["build"] = self.build
        if self.image:
            service["image"] = self.image
        if self.ports:
            service["ports"] = self.ports
        if self.environment:
            service["environment"] = self.environment
        if self.volumes:
            service["volumes"] = self.volumes
        if self.depends_on:
            service["depends_on"] = self.depends_on
        if self.command:
            service["command"] = self.command
        service["restart"] = self.restart
        if self.healthcheck:
            service["healthcheck"] = self.healthcheck
        return service


class ComposeFile:
    """Docker Compose file generator."""
    def __init__(self, version: str = "3.9"):
        self.version = version
        self.services: dict[str, ComposeService] = {}
        self.volumes: dict[str, dict] = {}
        self.networks: dict[str, dict] = {}

    def add_service(self, service: ComposeService):
        self.services[service.name] = service
        return self

    def add_volume(self, name: str, driver: str = "local"):
        self.volumes[name] = {"driver": driver}
        return self

    def add_network(self, name: str, driver: str = "bridge"):
        self.networks[name] = {"driver": driver}
        return self

    def generate(self) -> dict:
        result = {"version": self.version, "services": {}}
        for name, svc in self.services.items():
            result["services"][name] = svc.to_dict()
        if self.volumes:
            result["volumes"] = self.volumes
        if self.networks:
            result["networks"] = self.networks
        return result


# ======================== Generate Infrastructure ========================

# ---- Multi-stage Dockerfile ----
dockerfile = Dockerfile()
dockerfile.from_("python:3.11-slim", "builder")
dockerfile.workdir("/app")
dockerfile.install_packages(["poetry"])
dockerfile.copy("pyproject.toml", ".")
dockerfile.copy("poetry.lock", ".")
dockerfile.run("poetry export -f requirements.txt --output requirements.txt")
dockerfile.run("pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt")

dockerfile.from_("python:3.11-slim", "runner")
dockerfile.workdir("/app")
dockerfile.copy("/app/wheels", "/app/wheels", from_stage="builder")
dockerfile.copy("requirements.txt", ".")
dockerfile.run("pip install --no-cache-dir --no-index --find-links=/app/wheels -r requirements.txt")
dockerfile.env("PYTHONPATH", "/app")
dockerfile.copy("app", ".")
dockerfile.copy("migrations", "migrations", from_stage="builder")
dockerfile.expose(8000)
dockerfile.cmd(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])


# ---- Docker Compose ----
compose = ComposeFile()

# API service
api = ComposeService("api", build=".")
api.add_port(8000, 8000)
api.add_env("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/app")
api.add_env("REDIS_URL", "redis://redis:6379/0")
api.add_env("SECRET_KEY", "change-me-in-production")
api.add_env("ENVIRONMENT", "production")
api.add_volume("./app", "/app/app")
api.depends("db", "redis")
api.set_healthcheck(["CMD", "curl", "-f", "http://localhost:8000/health"])
compose.add_service(api)

# Database service
db = ComposeService("db", image="postgres:15-alpine")
db.add_port(5432, 5432)
db.add_env("POSTGRES_USER", "postgres")
db.add_env("POSTGRES_PASSWORD", "postgres")
db.add_env("POSTGRES_DB", "app")
db.add_volume("postgres_data", "/var/lib/postgresql/data")
db.set_healthcheck(["CMD-SHELL", "pg_isready -U postgres"])
compose.add_service(db)
compose.add_volume("postgres_data")

# Redis service
redis = ComposeService("redis", image="redis:7-alpine")
redis.add_port(6379, 6379)
redis.add_volume("redis_data", "/data")
redis.set_healthcheck(["CMD", "redis-cli", "ping"])
compose.add_service(redis)
compose.add_volume("redis_data")

# Nginx reverse proxy
nginx = ComposeService("nginx", image="nginx:alpine")
nginx.add_port(80, 80)
nginx.add_port(443, 443)
nginx.add_volume("./nginx.conf", "/etc/nginx/nginx.conf", mode="ro")
nginx.add_volume("./ssl", "/etc/nginx/ssl", mode="ro")
nginx.depends("api")
compose.add_service(nginx)

# Add network
compose.add_network("app_network")


# ======================== Demo ========================
print("=== Docker + Docker Compose Demo ===\n")

print("1. Generated Dockerfile (multi-stage):")
print("-" * 50)
print(dockerfile.generate())
print("-" * 50)

print("\n2. Generated docker-compose.yml:")
compose_dict = compose.generate()
print(json.dumps(compose_dict, indent=2))

print("\n3. Service summary:")
for name, svc in compose_dict["services"].items():
    image = svc.get("image", svc.get("build", "custom"))
    ports = ", ".join(svc.get("ports", ["none"]))
    deps = ", ".join(svc.get("depends_on", ["none"]))
    print(f"   {name:10s} image={image:25s} ports={ports:20s} depends={deps}")

print("\n4. Volumes:")
for vol in compose_dict.get("volumes", {}):
    print(f"   - {vol}")

print("\n5. Networks:")
for net in compose_dict.get("networks", {}):
    print(f"   - {net}")

print("\n6. Health checks:")
for name, svc in compose_dict["services"].items():
    if "healthcheck" in svc:
        hc = svc["healthcheck"]
        print(f"   {name}: {' '.join(hc['test'])} (interval={hc['interval']})")
