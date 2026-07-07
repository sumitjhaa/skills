# 🔄 CI/CD for APIs
<!-- ⏱️ 15 min | 🟢 Core -->

**What You'll Learn:** Pipeline stages, GitHub Actions, testing in CI, deployment strategies.

## Pipeline Stages

```
Lint → Type Check → Unit Tests → Integration Tests → Build → Deploy
```

| Stage | Tools | Fast |
|-------|-------|------|
| Lint | ruff, flake8 | ✅ |
| Type Check | mypy, pyright | ✅ |
| Unit Tests | pytest | ✅ |
| Integration | pytest + TestClient | ⚠️ |
| Build | docker build | ❌ |
| Deploy | docker push + ssh/ecs | ❌ |

## GitHub Actions Workflow

```yaml
name: FastAPI CI/CD

on:
  push: [main]
  pull_request: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt
      - run: ruff check .
      - run: pytest tests/ -x -v

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - run: echo "Deploying..."
```

## Environment Strategy

| Environment | Auto-Deploy | Tests | Approval |
|-------------|-------------|-------|----------|
| Development | On push | Unit | None |
| Staging | On PR merge | All | None |
| Production | Manual | All + smoke | Required |

## Run the Code

```bash
python code/27-cicd.py
```
