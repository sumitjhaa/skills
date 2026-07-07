# 📘 Django Phase 06 — Lesson 02: CI/CD Pipeline

> 🎯 **Goal**: Automate testing, building, and deployment with GitHub Actions — lint, test, build, deploy.

## 📖 Concepts

### CI/CD Flow
```
Push → Lint → Test → Build → Migrate → Deploy → Health Check
  ↑        ↑       ↑        ↑        ↑         ↑       ↑
Commit   ruff   pytest  Docker   python    ansible   curl
         mypy   coverage compose  manage.py          /health/
                        build    migrate
```

### Pipeline Stages

| Stage | Tool | Fails On |
|-------|------|----------|
| Lint | `ruff`, `mypy` | Code style / type errors |
| Test | `pytest`, `coverage` | Failing tests / low coverage |
| Security | `bandit`, `safety` | Vulnerabilities |
| Build | `docker compose build` | Build failure |
| Migrate | `python manage.py migrate` | Migration conflicts |
| Deploy | Ansible / SSH | Connection / script failure |
| Smoke | `curl /health/` | Health check fails |

### GitHub Actions Workflow
```yaml
name: Test & Deploy
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: myapp
          POSTGRES_USER: myapp
          POSTGRES_PASSWORD: myapp
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: ruff check .
      - run: pytest --cov --timeout=30

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying to production..."
```

### Environment Variables in CI
```yaml
- name: Run migrations
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
    SECRET_KEY: ${{ secrets.SECRET_KEY }}
  run: python manage.py migrate
```

### ADHD-Friendly Summary
```
Push → auto test + lint → auto deploy main
GitHub Actions → free CI/CD
Secrets → never hardcode credentials
Needs: [job] → sequential execution
```

## 🛠️ Code

```yaml
# .github/workflows/deploy.yml
name: Deploy Django

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: '3.12'

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: myapp
          POSTGRES_USER: myapp
          POSTGRES_PASSWORD: myapp
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install -r requirements.txt
      - run: ruff check .
      - run: pytest --cov=.

  deploy:
    if: github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to VPS
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /app
            git pull
            docker compose build
            docker compose run --rm web python manage.py migrate
            docker compose up -d --force-recreate
```

## 🧪 Practice

1. Create a GitHub Actions workflow that runs `ruff` and `pytest`
2. Add a PostgreSQL service container for tests
3. Add a `deploy` job that runs only on `main` branch
4. Use secrets for `DATABASE_URL` and `SECRET_KEY`
5. Add a health check step after deployment

## 🧠 Key Takeaways

- CI runs on every push — lint + test + security check
- CD deploys only from main branch after CI passes
- Use GitHub secrets for all sensitive data
- Service containers provide test databases
- Pipeline should fail fast — exit on first error
