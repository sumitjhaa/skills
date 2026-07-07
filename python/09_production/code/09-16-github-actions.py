"""GitHub Actions CI/CD — workflow anatomy and local validation."""
import os
import sys

try:
    import yaml
except ImportError:
    print("Install PyYAML: pip install pyyaml")
    sys.exit(1)

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

assert yaml.safe_load(WORKFLOW) is not None
print("\n✅ Workflow YAML is valid")
