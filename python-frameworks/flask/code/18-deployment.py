"""Deployment: Gunicorn, Nginx, environment config, production settings."""
from typing import Any, Optional
from datetime import datetime
import json
import os


# ======================== Configuration System ========================

class Config:
    """Environment-based configuration."""
    SECRET_KEY: str = "dev-secret-key"
    DATABASE_URL: str = "sqlite:///dev.db"
    DEBUG: bool = True
    TESTING: bool = False
    SERVER_NAME: str = "localhost:5000"

    @classmethod
    def from_env(cls):
        cls.SECRET_KEY = os.environ.get("SECRET_KEY", cls.SECRET_KEY)
        cls.DATABASE_URL = os.environ.get("DATABASE_URL", cls.DATABASE_URL)
        cls.DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"
        cls.SERVER_NAME = os.environ.get("SERVER_NAME", cls.SERVER_NAME)
        return cls


class ProductionConfig(Config):
    SECRET_KEY: str = "change-this-in-production"
    DATABASE_URL: str = "postgresql://user:pass@localhost/prod"
    DEBUG: bool = False
    SERVER_NAME: str = "api.example.com"


class StagingConfig(Config):
    SECRET_KEY: str = "staging-secret"
    DATABASE_URL: str = "postgresql://user:pass@staging-db/prod"
    DEBUG: bool = False
    SERVER_NAME: str = "staging.example.com"


class DevelopmentConfig(Config):
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///dev.db"


configs = {
    "development": DevelopmentConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
}


# ======================== Gunicorn Simulation ========================

class GunicornWorker:
    """Simulates Gunicorn worker behavior."""
    def __init__(self, name: str = "gunicorn", workers: int = 4, worker_class: str = "sync",
                 bind: str = "0.0.0.0:8000", timeout: int = 30):
        self.name = name
        self.workers = workers
        self.worker_class = worker_class
        self.bind = bind
        self.timeout = timeout
        self.pid = os.getpid()
        self.started_at = datetime.now()
        self.requests_served = 0

    def serve_request(self):
        self.requests_served += 1

    def status(self) -> dict:
        return {
            "server": self.name,
            "workers": self.workers,
            "worker_class": self.worker_class,
            "bind": self.bind,
            "timeout": self.timeout,
            "pid": self.pid,
            "uptime": (datetime.now() - self.started_at).total_seconds(),
            "requests_served": self.requests_served,
        }


class NginxConfig:
    """Nginx reverse proxy configuration generator."""
    def __init__(self, domain: str = "api.example.com", upstream_port: int = 8000):
        self.domain = domain
        self.upstream_port = upstream_port
        self.ssl_cert: Optional[str] = None
        self.ssl_key: Optional[str] = None
        self.rate_limit: Optional[int] = None
        self.allowed_ips: list[str] = []
        self.static_path: Optional[str] = None

    def enable_ssl(self, cert: str, key: str):
        self.ssl_cert = cert
        self.ssl_key = key

    def enable_rate_limit(self, req_per_min: int = 100):
        self.rate_limit = req_per_min

    def generate(self) -> str:
        lines = [f"server {{", f"    listen 80;", f"    server_name {self.domain};"]

        if self.ssl_cert:
            lines.extend([
                f"    listen 443 ssl;",
                f"    ssl_certificate {self.ssl_cert};",
                f"    ssl_certificate_key {self.ssl_key};",
            ])

        if self.rate_limit:
            lines.append(f"    limit_req zone=api burst={self.rate_limit};")

        if self.static_path:
            lines.extend([
                f"    location /static/ {{",
                f"        alias {self.static_path};",
                f"        expires 30d;",
                f"    }}",
            ])

        lines.extend([
            f"    location / {{",
            f"        proxy_pass http://127.0.0.1:{self.upstream_port};",
            f"        proxy_set_header Host $host;",
            f"        proxy_set_header X-Real-IP $remote_addr;",
            f"        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;",
            f"        proxy_set_header X-Forwarded-Proto $scheme;",
            f"    }}",
            f"}}",
        ])
        return "\n".join(lines)


# ======================== Flask App ========================

class Flask:
    def __init__(self):
        self.routes: list[dict] = []
        self.config = DevelopmentConfig()
        self.gunicorn = GunicornWorker()
        self.nginx = NginxConfig()

    def route(self, path, methods=None):
        methods = methods or ["GET"]
        def deco(f):
            self.routes.append({"path": path, "methods": methods, "handler": f}); return f
        return deco

    def __call__(self, method, path, **kw):
        self.gunicorn.serve_request()
        for r in self.routes:
            if method in r["methods"] and r["path"] == path:
                result = r["handler"](**kw)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"error": "Not Found"}}

app = Flask()


# ======================== Routes ========================

@app.route("/")
def home():
    env = os.environ.get("FLASK_ENV", "development")
    return {
        "app": "Flask Production App",
        "environment": env,
        "config": {
            "debug": app.config.DEBUG,
            "database": app.config.DATABASE_URL.split("://")[0] + "://...",
            "server": app.config.SERVER_NAME,
        },
    }

@app.route("/config")
def show_config():
    return {
        "environment": os.environ.get("FLASK_ENV", "development"),
        "debug": app.config.DEBUG,
        "database_url": app.config.DATABASE_URL,
        "secret_key_set": app.config.SECRET_KEY != "",
    }

@app.route("/server/status")
def server_status():
    return app.gunicorn.status()

@app.route("/server/nginx-config")
def nginx_config():
    return {"nginx_config": app.nginx.generate()}


# ======================== Demo ========================
print("=== Deployment Demo ===\n")

print("1. Environment configs:")
for name, cfg_cls in configs.items():
    cfg = cfg_cls()
    print(f"   {name:12s} debug={cfg.DEBUG} db={cfg.DATABASE_URL[:20]}...")

print(f"\n2. Current config:")
os.environ["FLASK_ENV"] = "production"
app.config = ProductionConfig()
r = app("GET", "/")
print(f"   {json.dumps(r['data'], indent=2)}")

print(f"\n3. Gunicorn server status:")
r = app("GET", "/server/status")
print(f"   {json.dumps(r['data'], indent=2)}")

print(f"\n4. Nginx configuration generated:")
app.nginx = NginxConfig(domain="api.example.com", upstream_port=8000)
app.nginx.enable_ssl("/etc/ssl/certs/cert.pem", "/etc/ssl/private/key.pem")
app.nginx.enable_rate_limit(100)
app.nginx.static_path = "/var/www/app/static"
print(app.nginx.generate())

print(f"\n5. Server handling requests:")
for i in range(5):
    app("GET", "/")
r = app("GET", "/server/status")
print(f"   Requests served: {r['data']['requests_served']}")

print(f"\n6. Deploy commands:")
print("   # Development:")
print("   flask run --port 5000 --debug")
print("   # Production:")
print("   gunicorn -w 4 -b 0.0.0.0:8000 app:app")
print("   # With config:")
print("   FLASK_ENV=production SECRET_KEY=... gunicorn -w 4 app:app")
