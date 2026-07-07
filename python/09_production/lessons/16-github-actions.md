# 🚀 GitHub Actions CI/CD
<!-- ⏱️ 16 min | 🔴 Advanced | 🧠 Production -->

**What You'll Learn:** Automate testing, linting, and deployment with GitHub Actions — the industry-standard CI/CD platform for Python projects.

> 💡 **TL;DR — The whole point:** A `.github/workflows/ci.yml` file can run your tests on every push, lint your code, type-check with mypy, and deploy to production — all automatically, on every commit.

## 🔗 Why This Matters
Manual testing is fragile and doesn't scale. CI/CD pipelines catch bugs before they reach production, enforce code quality automatically, and make deployment a one-click (or zero-click) operation. Every professional Python project uses some form of CI/CD.

## The Concept

| Concept | Purpose |
|---------|---------|
| **Workflow** | A single automation pipeline (`.yml` file) |
| **Event** | What triggers the workflow (push, PR, schedule) |
| **Job** | A unit of work running on a runner |
| **Step** | A single command or action within a job |
| **Runner** | The VM/container that executes jobs |
| **Action** | Reusable unit (checkout, setup-python, etc.) |
| **Matrix** | Run the same job across multiple versions/configs |

## Code Example

```python
"""GitHub Actions CI/CD — workflow anatomy and local validation."""
import os
import sys
import yaml

WORKFLOW = """
name: CI

"on":
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ruff mypy pytest
          pip install -e .
      - name: Lint with ruff
        run: ruff check .
      - name: Type-check with mypy
        run: mypy src/
      - name: Test with pytest
        run: pytest tests/ --cov=src/ --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  deploy:
    needs: [test]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: echo "Deploying... (add your deploy step here)"
"""

print("=== Workflow YAML (validated) ===")
parsed = yaml.safe_load(WORKFLOW)
print(f"Workflow name: {parsed['name']}")
print(f"Events: {list(parsed['on'].keys())}")
print(f"Jobs: {list(parsed['jobs'].keys())}")
matrix = parsed['jobs']['test']['strategy']['matrix']
print(f"Python matrix: {matrix['python-version']}")
print(f"Deploy depends on: {parsed['jobs']['deploy']['needs']}")

print("\n=== Matrix test simulation ===")
for py_ver in matrix['python-version']:
    print(f"  Would test on Python {py_ver}")
    print(f"    Steps: checkout → setup-python({py_ver}) → install deps → ruff → mypy → pytest")

print("\n=== Badge generator ===")
repo = "owner/my-python-project"
badge = f"[![CI](https://github.com/{repo}/actions/workflows/ci.yml/badge.svg)](https://github.com/{repo}/actions/workflows/ci.yml)"
print(f"  Add to README.md:\n  {badge}")

# Verify workflow parses as valid YAML
assert yaml.safe_load(WORKFLOW) is not None
print("\n✅ Workflow YAML is valid")
```

## 🔍 How It Works
- **Events** trigger workflows: `push`, `pull_request`, `schedule` (cron), `workflow_dispatch` (manual)
- **Matrix strategy** runs the same job with different Python versions, OSes, or dependency sets
- **Actions** (`actions/checkout`, `actions/setup-python`) are pre-built steps from the GitHub Marketplace
- **`needs`** creates job dependencies — `deploy` waits for `test` to pass
- **Conditional execution** with `if` — only deploy on `main` branch
- **Secrets** (like `PYPI_TOKEN`) are stored in GitHub repo settings, never in the workflow file

## ⚠️ Common Pitfall
- Forgetting to `pip install -e .` (or your package) before testing — tests can't import your code
- Hardcoding secrets in the workflow file — use `${{ secrets.MY_SECRET }}` instead
- Not pinning action versions — `actions/checkout@v4` is stable; `@main` or `@v1.2.3` can break
- Matrix explosion — testing 3 Python versions × 3 OSes = 9 jobs; keep it focused

## 🧠 Memory Aid
"Event triggers → Jobs run in parallel → Steps execute sequentially → Matrix multiplies versions → Needs creates chains."

## 🏃 Try It
Create a `.github/workflows/ci.yml` for a Python project that runs `ruff check .`, `pytest`, and deploys to PyPI on tagged releases.

## 🔗 Related
- [Pre-commit & Makefile](12-precommit-makefile.md) — local quality gates that run before CI
- [Testing with Pytest](04-testing-pytest.md) — the tests your CI pipeline runs
- [Packaging](10-packaging.md) — building the package that CI deploys
- [Docker Python](11-docker-python.md) — containerized CI/CD

## ➡️ Next
[17 — Profiling & Optimization](17-profiling-cprofile.md)
