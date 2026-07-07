# 🎯 Pre-commit & Makefile
<!-- ⏱️ 14 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Set up pre-commit hooks (ruff, mypy, black, isort) and a Makefile for standardized development workflows.

> 💡 **TL;DR — The whole point:** Pre-commit automatically checks your code before every git commit. Makefile provides standardized commands so every dev runs the same lint/test/typecheck workflow.

## 🔗 Why This Matters
Without automation, code reviews get bogged down with style nitpicks. Pre-commit catches formatting issues before they reach the PR. Makefile ensures "it worked on my machine" is replaced by "it passed the CI checks."

## The Concept
- **Pre-commit:** runs hooks on staged files before each commit
- **Hooks:** ruff (lint + format), mypy (type check), black (auto-format), isort (import sort)
- **Makefile:** defines `lint`, `typecheck`, `test`, `clean`, `docker-build` targets

## Code Example
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        args: [--strict, --ignore-missing-imports]
        additional_dependencies: [pydantic, types-requests]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.7
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]
        additional_dependencies: ["bandit[toml]"]
```

```makefile
# Makefile
.PHONY: install lint typecheck test clean docker-build help

.DEFAULT_GOAL := help

install:                           ## Install dev dependencies
	pip install -e ".[dev]"
	pre-commit install

lint:                              ## Run ruff linter and formatter
	ruff check src/
	ruff format --check src/

typecheck:                         ## Run mypy type checker
	mypy src/

test:                              ## Run tests
	python -m pytest tests/ -v --cov=src

test-fast:                         ## Run tests without coverage
	python -m pytest tests/ -v -x

clean:                             ## Clean build artifacts
	rm -rf dist/ build/ *.egg-info __pycache__ .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

docker-build:                      ## Build Docker image
	docker build -t my-app:latest .

docker-run:                        ## Run Docker container
	docker run -p 8000:8000 my-app:latest

help:                              ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
```

```python
"""src/app.py — Example file that pre-commit checks."""
from typing import Final

TAX_RATE: Final[float] = 0.08


def calculate_total(items: list[float], discount: float = 0.0) -> float:
    subtotal = sum(items)
    discounted = subtotal * (1 - discount)
    return round(discounted * (1 + TAX_RATE), 2)
```

## 🔍 How It Works
- Install: `pip install pre-commit && pre-commit install`
- On `git commit`, pre-commit runs all hooks on staged files
- Ruff auto-fixes many issues; if it can't, the commit is blocked
- Makefile targets: `make lint`, `make test`, `make typecheck`
- `make lint` runs ruff; `make typecheck` runs mypy; `make test` runs pytest
- `make clean` removes `__pycache__`, `dist/`, etc.
- `make help` prints all targets with descriptions

## ⚠️ Common Pitfall
Committing pre-commit configuration changes without running `pre-commit install` first. The hooks won't run. Always run `pre-commit install` after cloning or changing `.pre-commit-config.yaml`.

## 🧠 Memory Aid
"Pre-commit = 'check my code before git commit.' Makefile = 'standard commands everyone runs.' `make lint` + `make test` + `make typecheck` = the golden trio."

## 🏃 Try It
Create a `.pre-commit-config.yaml` with just `ruff` and `trailing-whitespace` hooks. Write a Python file with trailing whitespace and a lint error. Run `pre-commit run --all-files` and see it caught.

## 🔗 Related
- [PEP 8 & Code Style](02-pep8-style.md) — what ruff enforces
- [Type Checking](07-type-checking.md) — what mypy checks
- [Docker for Python](11-docker-python.md) — `make docker-build`

## ➡️ Next
[Pydantic & Settings](13-pydantic-settings.md)
