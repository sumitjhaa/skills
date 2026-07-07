"""CI/CD pipeline: lint, test, build, deploy stages; GitHub Actions simulation."""
from typing import Any, Optional
from datetime import datetime
import json
import time


# ======================== CI Pipeline ========================

class Stage:
    """A single CI/CD stage."""
    def __init__(self, name: str, commands: list[str]):
        self.name = name
        self.commands = commands
        self.status: str = "pending"
        self.output: list[str] = []
        self.duration: float = 0.0
        self.error: str | None = None

    def run(self, env: dict | None = None) -> bool:
        self.status = "running"
        self.output.append(f"▶️  Starting stage: {self.name}")
        start = time.time()

        try:
            for cmd in self.commands:
                self.output.append(f"   $ {cmd}")
                # Simulate command execution
                time.sleep(0.05)
                if "fail" in cmd.lower() or "error" in cmd.lower():
                    raise RuntimeError(f"Command failed: {cmd}")

            self.status = "passed"
            self.output.append(f"✅ {self.name} passed")
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            self.output.append(f"❌ {self.name} failed: {e}")

        self.duration = time.time() - start
        return self.status == "passed"


class Pipeline:
    """A complete CI/CD pipeline with stages."""
    def __init__(self, name: str, branch: str = "main"):
        self.name = name
        self.branch = branch
        self.stages: list[Stage] = []
        self.status: str = "pending"
        self.run_id: str = f"run_{int(time.time())}"
        self.start_time: float = 0.0
        self.end_time: float = 0.0

    def add_stage(self, name: str, commands: list[str]):
        self.stages.append(Stage(name, commands))
        return self

    def run(self, env: dict | None = None) -> dict:
        self.status = "running"
        self.start_time = time.time()
        results = []

        print(f"\n{'='*60}")
        print(f"  PIPELINE: {self.name} (branch: {self.branch})")
        print(f"  Run ID: {self.run_id}")
        print(f"{'='*60}\n")

        for stage in self.stages:
            success = stage.run(env)
            results.append({"name": stage.name, "status": stage.status, "duration": round(stage.duration, 2)})

            # Print output
            for line in stage.output:
                print(f"  {line}")

            print(f"  Duration: {stage.duration:.2f}s\n")

            if not success:
                self.status = "failed"
                self.end_time = time.time()
                return {"status": "failed", "failed_stage": stage.name, "results": results}

        self.status = "passed"
        self.end_time = time.time()
        total_duration = round(self.end_time - self.start_time, 2)
        print(f"{'='*60}")
        print(f"  ✅ Pipeline passed! Total: {total_duration}s")
        print(f"{'='*60}\n")

        return {"status": "passed", "results": results, "total_duration": total_duration}


class GitHubActionsWorkflow:
    """Generates GitHub Actions workflow YAML (simulated)."""
    def __init__(self, name: str):
        self.name = name
        self.triggers: list[str] = []
        self.jobs: dict[str, dict] = {}

    def on_push(self, branches: list[str] | None = None):
        self.triggers.append(f"push: {branches or ['main']}")
        return self

    def on_pull_request(self, branches: list[str] | None = None):
        self.triggers.append(f"pull_request: {branches or ['main']}")
        return self

    def add_job(self, name: str, runs_on: str = "ubuntu-latest", steps: list[dict] | None = None):
        self.jobs[name] = {"runs-on": runs_on, "steps": steps or []}
        return self

    def generate(self) -> str:
        lines = [f"name: {self.name}", ""]
        for trigger in self.triggers:
            lines.append(f"on:")
            event, branches = trigger.split(": ", 1)
            lines.append(f"  {event}:")
            for b in eval(branches):
                lines.append(f"    - {b}")
        lines.append("")
        lines.append("jobs:")
        for job_name, job in self.jobs.items():
            lines.append(f"  {job_name}:")
            lines.append(f"    runs-on: {job['runs-on']}")
            lines.append("    steps:")
            for step in job["steps"]:
                if "name" in step:
                    lines.append(f"      - name: {step['name']}")
                if "run" in step:
                    lines.append(f"        run: {step['run']}")
                if "uses" in step:
                    lines.append(f"        uses: {step['uses']}")
        return "\n".join(lines)


# ======================== Demo ========================
print("=" * 60)
print("  CI/CD PIPELINE DEMO")
print("=" * 60)

# 1. Build pipeline
print("\n1. Building pipeline: FastAPI CI/CD")
pipeline = Pipeline("FastAPI CI/CD", branch="main")

pipeline.add_stage("Lint", [
    "ruff check .",
    "mypy src/",
])
pipeline.add_stage("Type Check", [
    "pyright src/",
])
pipeline.add_stage("Unit Tests", [
    "pytest tests/ -x -v --cov=src --cov-report=term",
])
pipeline.add_stage("Integration Tests", [
    "pytest tests/integration/ -x -v",
])
pipeline.add_stage("Build", [
    "docker build -t fastapi-app:latest .",
])
pipeline.add_stage("Push", [
    "docker tag fastapi-app:latest registry.example.com/fastapi-app:latest",
    "docker push registry.example.com/fastapi-app:latest",
])

result = pipeline.run()

# 2. Generate GitHub Actions workflow
print("\n2. Generating GitHub Actions workflow:")
workflow = GitHubActionsWorkflow("FastAPI Deploy")
workflow.on_push(["main"]).on_pull_request(["main"])

workflow.add_job("test", "ubuntu-latest", steps=[
    {"name": "Checkout code", "uses": "actions/checkout@v4"},
    {"name": "Set up Python", "uses": "actions/setup-python@v5", "run": "python-version: '3.11'"},
    {"name": "Install dependencies", "run": "pip install -r requirements.txt"},
    {"name": "Run linting", "run": "ruff check ."},
    {"name": "Run tests", "run": "pytest tests/ -x -v"},
])

workflow.add_job("deploy", "ubuntu-latest", steps=[
    {"name": "Checkout code", "uses": "actions/checkout@v4"},
    {"name": "Configure AWS credentials", "uses": "aws-actions/configure-aws-credentials@v4"},
    {"name": "Build and push Docker image", "run": "docker build -t app . && docker push"},
    {"name": "Deploy to ECS", "run": "aws ecs update-service --cluster prod --service api --force-new-deployment"},
])

print("-" * 60)
print(workflow.generate())
print("-" * 60)

# 3. Deployment environments
print("\n3. Deployment environments:")
environments = [
    {"name": "Development", "url": "dev.api.example.com", "auto_deploy": True, "tests": "unit"},
    {"name": "Staging", "url": "staging.api.example.com", "auto_deploy": True, "tests": "all"},
    {"name": "Production", "url": "api.example.com", "auto_deploy": False, "tests": "all + manual approval"},
]
for env in environments:
    print(f"   🌐 {env['name']:15s} {env['url']:30s} auto={env['auto_deploy']} tests={env['tests']}")

# 4. Pipeline summary
print(f"\n4. Pipeline result: {result['status'].upper()}")
print(f"   Run ID: {pipeline.run_id}")
for r in result.get("results", []):
    icon = "✅" if r["status"] == "passed" else "❌"
    print(f"   {icon} {r['name']:20s} {r['status']:8s} {r['duration']:.2f}s")
