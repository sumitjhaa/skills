"""Docker: Dockerfile, docker-compose, multi-stage builds, volumes."""
from typing import Any, Optional
import json


# ======================== Dockerfile Generator ========================

class Dockerfile:
    def __init__(self, base: str = "python:3.11-slim"):
        self.base = base
        self.lines: list[str] = []
        self._multi_stage = False

    def from_(self, image: str, as_name: str | None = None):
        line = f"FROM {image}"
        if as_name:
            line += f" AS {as_name}"
        self.lines.append(line)
        return self

    def workdir(self, path: str):
        self.lines.append(f"WORKDIR {path}")
        return self

    def copy(self, src: str, dst: str, from_stage: str | None = None):
        line = "COPY "
        if from_stage:
            line += f"--from={from_stage} "
        line += f"{src} {dst}"
        self.lines.append(line)
        return self

    def run(self, cmd: str):
        self.lines.append(f"RUN {cmd}")
        return self

    def env(self, key: str, value: str):
        self.lines.append(f"ENV {key}={value}")
        return self

    def expose(self, port: int):
        self.lines.append(f"EXPOSE {port}")
        return self

    def cmd(self, cmd: list[str]):
        self.lines.append(f"CMD {json.dumps(cmd)}")
        return self

    def pip_install(self, *packages):
        self.lines.append(f"RUN pip install --no-cache-dir {' '.join(packages)}")
        return self

    def generate(self) -> str:
        return "\n".join(self.lines)


class ComposeService:
    def __init__(self, name: str, build: str | None = None, image: str | None = None):
        self.name = name
        self.build = build
        self.image = image
        self.ports: list[str] = []
        self.env: dict[str, str] = {}
        self.volumes: list[str] = []
        self.depends: list[str] = []
        self.command: list[str] | None = None
        self.restart = "unless-stopped"
        self.healthcheck: dict | None = None

    def add_port(self, host: int, container: int):
        self.ports.append(f"{host}:{container}")
        return self

    def add_env(self, key: str, value: str):
        self.env[key] = value
        return self

    def add_volume(self, host: str, container: str):
        self.volumes.append(f"{host}:{container}")
        return self

    def depends_on(self, *services: str):
        self.depends.extend(services)
        return self

    def to_dict(self) -> dict:
        svc = {"restart": self.restart}
        if self.build: svc["build"] = self.build
        if self.image: svc["image"] = self.image
        if self.ports: svc["ports"] = self.ports
        if self.env: svc["environment"] = self.env
        if self.volumes: svc["volumes"] = self.volumes
        if self.depends: svc["depends_on"] = self.depends
        if self.command: svc["command"] = self.command
        if self.healthcheck: svc["healthcheck"] = self.healthcheck
        return svc


class Compose:
    def __init__(self, version: str = "3.9"):
        self.version = version
        self.services: dict[str, ComposeService] = {}
        self.volumes: dict[str, dict] = {}
        self.networks: dict[str, dict] = {}

    def add_service(self, svc: ComposeService):
        self.services[svc.name] = svc
        return self

    def add_volume(self, name: str):
        self.volumes[name] = {"driver": "local"}
        return self

    def add_network(self, name: str, driver: str = "bridge"):
        self.networks[name] = {"driver": driver}
        return self

    def generate(self) -> dict:
        result = {"version": self.version, "services": {name: s.to_dict() for name, s in self.services.items()}}
        if self.volumes: result["volumes"] = self.volumes
        if self.networks: result["networks"] = self.networks
        return result


# ======================== Generate ========================

# Multi-stage Dockerfile
df = Dockerfile()
df.from_("python:3.11-slim", "builder")
df.workdir("/app")
df.copy("requirements.txt", ".")
df.run("pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt")
df.from_("python:3.11-slim", "runner")
df.workdir("/app")
df.copy("/app/wheels", "/app/wheels", from_stage="builder")
df.copy("requirements.txt", ".")
df.run("pip install --no-cache-dir --no-index --find-links=/app/wheels -r requirements.txt")
df.env("FLASK_ENV", "production")
df.copy("app", ".")
df.expose(5000)
df.cmd(["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"])

# Docker Compose
compose = Compose()

flask_svc = ComposeService("web", build=".")
flask_svc.add_port(80, 5000)
flask_svc.add_env("FLASK_ENV", "production")
flask_svc.add_env("SECRET_KEY", "${SECRET_KEY}")
flask_svc.add_env("DATABASE_URL", "postgresql://postgres:postgres@db:5432/flaskapp")
flask_svc.add_volume("./app", "/app/app")
flask_svc.depends_on("db", "redis")
compose.add_service(flask_svc)

db_svc = ComposeService("db", image="postgres:15-alpine")
db_svc.add_port(5432, 5432)
db_svc.add_env("POSTGRES_USER", "postgres")
db_svc.add_env("POSTGRES_PASSWORD", "postgres")
db_svc.add_env("POSTGRES_DB", "flaskapp")
db_svc.add_volume("postgres_data", "/var/lib/postgresql/data")
compose.add_service(db_svc)
compose.add_volume("postgres_data")

redis_svc = ComposeService("redis", image="redis:7-alpine")
redis_svc.add_port(6379, 6379)
redis_svc.add_volume("redis_data", "/data")
compose.add_service(redis_svc)
compose.add_volume("redis_data")

nginx_svc = ComposeService("nginx", image="nginx:alpine")
nginx_svc.add_port(443, 443)
nginx_svc.add_volume("./nginx.conf", "/etc/nginx/nginx.conf")
nginx_svc.depends_on("web")
compose.add_service(nginx_svc)

compose.add_network("app_network")


# ======================== Flask App ========================

class Flask:
    def __init__(self):
        self.routes: list[dict] = []

    def route(self, path, methods=None):
        methods = methods or ["GET"]
        def deco(f):
            self.routes.append({"path": path, "methods": methods, "handler": f}); return f
        return deco

    def __call__(self, method, path, **kw):
        for r in self.routes:
            if method in r["methods"] and r["path"] == path:
                result = r["handler"](**kw)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"error": "Not Found"}}

app = Flask()

@app.route("/")
def home():
    return {
        "message": "Dockerized Flask App",
        "services": ["web (Flask + Gunicorn)", "db (PostgreSQL)", "redis", "nginx"],
    }

@app.route("/dockerfile")
def dockerfile():
    return {"dockerfile": df.generate()}

@app.route("/compose")
def compose_config():
    return compose.generate()


# ======================== Demo ========================
print("=== Docker Demo ===\n")

print("1. Multi-stage Dockerfile:")
print("-" * 50)
print(df.generate())
print("-" * 50)

print("\n2. Docker Compose services:")
cfg = compose.generate()
for name, svc in cfg["services"].items():
    image = svc.get("image", svc.get("build", "custom"))
    ports = ", ".join(svc.get("ports", ["none"]))
    deps = ", ".join(svc.get("depends_on", ["none"]))
    print(f"   {name:8s} image={image:30s} ports={ports:20s} depends={deps}")

print("\n3. Volumes:")
for vol in cfg.get("volumes", {}):
    print(f"   - {vol}")

print("\n4. Networks:")
for net in cfg.get("networks", {}):
    print(f"   - {net}")

print("\n5. Build and run commands:")
print("   docker compose build")
print("   docker compose up -d")
print("   docker compose logs -f")
print("   docker compose down")

print("\n6. Environment variables for secrets:")
print("   export SECRET_KEY=your-secret-key-here")
print("   docker compose up")
