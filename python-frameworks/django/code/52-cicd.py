"""CI/CD pipeline simulation: testing, linting, building, deploying."""
import json
import time
import random
from enum import Enum


# ======================== CI/CD Pipeline ========================

class StageStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class PipelineStage:
    """Represents a single stage in CI/CD pipeline."""
    def __init__(self, name: str, command: str, timeout: int = 300):
        self.name = name
        self.command = command
        self.timeout = timeout
        self.status = StageStatus.PENDING
        self.duration = 0.0
        self.output: list[str] = []
        self.errors: list[str] = []

    def run(self) -> StageStatus:
        self.status = StageStatus.RUNNING
        t0 = time.time()
        try:
            success = self.execute()
            self.duration = time.time() - t0
            self.status = StageStatus.PASSED if success else StageStatus.FAILED
            return self.status
        except Exception as e:
            self.duration = time.time() - t0
            self.errors.append(str(e))
            self.status = StageStatus.FAILED
            return self.status

    def execute(self) -> bool:
        """Simulate command execution."""
        time.sleep(random.uniform(0.3, 1.5))
        if "FAIL" in self.command:
            self.errors.append("Simulated failure")
            return False
        self.output.append(f"✓ {self.command}")
        return True

    def summary(self) -> dict:
        return {
            "name": self.name,
            "status": self.status.value,
            "duration": round(self.duration, 2),
            "errors": self.errors,
        }


class Pipeline:
    """A complete CI/CD pipeline."""
    def __init__(self, name: str):
        self.name = name
        self.stages: list[PipelineStage] = []
        self.branch = "main"
        self.commit_hash = ""
        self.status = StageStatus.PENDING

    def add_stage(self, stage: PipelineStage):
        self.stages.append(stage)

    def run(self) -> StageStatus:
        print(f"\n=== Pipeline: {self.name} ===")
        print(f"   Branch: {self.branch}")
        print(f"   Commit: {self.commit_hash[:8] if self.commit_hash else 'N/A'}")
        print()

        all_passed = True
        for stage in self.stages:
            print(f"   ▶ {stage.name} ({stage.command})")
            result = stage.run()
            status_icon = "✅" if result == StageStatus.PASSED else "❌" if result == StageStatus.FAILED else "⏳"
            print(f"     {status_icon} {result.value} in {stage.duration:.2f}s")
            if stage.errors:
                for err in stage.errors:
                    print(f"     ! {err}")
            if result == StageStatus.FAILED:
                all_passed = False
                break
            print()

        self.status = StageStatus.PASSED if all_passed else StageStatus.FAILED
        return self.status

    def report(self) -> dict:
        return {
            "pipeline": self.name,
            "status": self.status.value,
            "branch": self.branch,
            "stages": [s.summary() for s in self.stages],
            "total_duration": round(sum(s.duration for s in self.stages), 2),
        }


# ======================== GitHub Actions Workflow ========================

class GitHubAction:
    """Represents a GitHub Actions workflow step."""
    def __init__(self, name: str, uses: str = "", run: str = ""):
        self.name = name
        self.uses = uses
        self.run = run

    def yaml(self, indent: int = 4) -> str:
        pad = " " * indent
        lines = [f"{pad}- name: {self.name}"]
        if self.uses:
            lines.append(f"{pad}  uses: {self.uses}")
        if self.run:
            lines.append(f"{pad}  run: {self.run}")
        return "\n".join(lines)


class Workflow:
    """Simulates a GitHub Actions workflow."""
    def __init__(self, name: str, on: list[str]):
        self.name = name
        self.on = on
        self.jobs: dict[str, list[GitHubAction]] = {}

    def add_job(self, name: str, actions: list[GitHubAction]):
        self.jobs[name] = actions

    def generate_yaml(self) -> str:
        lines = [f"name: {self.name}"]
        lines.append(f"on: {self.on}")
        lines.append("jobs:")
        for job_name, actions in self.jobs.items():
            lines.append(f"  {job_name}:")
            lines.append("    runs-on: ubuntu-latest")
            lines.append("    steps:")
            for action in actions:
                lines.append(action.yaml(6))
        return "\n".join(lines)


# ======================== Demo ========================
print("=== CI/CD Pipeline Demo ===\n")

# --- Build a deployment pipeline ---
pipeline = Pipeline("Deploy Blog")
pipeline.branch = "main"
pipeline.commit_hash = "a1b2c3d4e5f6"

pipeline.add_stage(PipelineStage("Lint", "ruff check ."))
pipeline.add_stage(PipelineStage("Type Check", "mypy ."))
pipeline.add_stage(PipelineStage("Test", "pytest --cov -x --timeout=30"))
pipeline.add_stage(PipelineStage("Build", "docker compose build"))
pipeline.add_stage(PipelineStage("Migrate", "python manage.py migrate --fake-initial"))
pipeline.add_stage(PipelineStage("Deploy", "ansible-playbook deploy.yml"))

result = pipeline.run()
report = pipeline.report()

print(f"\nPipeline status: {report['status']}")
print(f"Total duration: {report['total_duration']}s")

# --- GitHub Actions workflow ---
print("\n--- GitHub Actions Workflow ---")

workflow = Workflow("Test & Deploy", ["push", "pull_request"])

workflow.add_job("test", [
    GitHubAction("Checkout", uses="actions/checkout@v4"),
    GitHubAction("Setup Python", uses="actions/setup-python@v5", run=""),
    GitHubAction("Install deps", run="pip install -r requirements.txt"),
    GitHubAction("Run tests", run="pytest --cov --timeout=30"),
    GitHubAction("Run linter", run="ruff check ."),
])

workflow.add_job("deploy", [
    GitHubAction("Checkout", uses="actions/checkout@v4"),
    GitHubAction("Deploy to production", run="ansible-playbook deploy.yml -i production"),
])

print(workflow.generate_yaml())

# --- Deployment summary ---
print("\n--- Deployment Summary ---")
deploy_steps = [
    ("Pull latest", "git pull origin main"),
    ("Build images", "docker compose build --no-cache"),
    ("Run migrations", "docker compose run --rm web python manage.py migrate"),
    ("Collect static", "docker compose run --rm web python manage.py collectstatic --noinput"),
    ("Restart services", "docker compose up -d --force-recreate"),
    ("Health check", "curl -f http://localhost:8000/health/"),
    ("Rollback if failed", "docker compose up -d web_previous"),
]
for i, (step, cmd) in enumerate(deploy_steps, 1):
    print(f"   {i}. {step}: {cmd}")
