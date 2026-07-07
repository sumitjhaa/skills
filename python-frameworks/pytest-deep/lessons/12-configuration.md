# ⚙️ Configuration
<!-- ⏱️ 10 min | 🟡 Intermediate -->

**What You'll Learn:** pytest.ini, pyproject.toml settings, CLI flags, profiles.

## Config Files

```ini
# pytest.ini
[pytest]
minversion = 7.0
testpaths = tests
python_files = test_*.py
markers =
    slow: marks tests as slow
    api: marks API tests
addopts = -v --tb=short
```

## pyproject.toml

```toml
[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py"]
markers = { slow = "marks tests as slow", api = "marks API tests" }
addopts = "-v --tb=short"
```

## Useful CLI Flags

```bash
pytest -v                      # Verbose
pytest -s                      # Show print statements
pytest -x                      # Stop on first failure
pytest --tb=long               # Full traceback
pytest --tb=short              # Short traceback
pytest --tb=line               # One line per failure
pytest -lf                     # Run last failed first
pytest --ff                    # Run failed first, then rest
pytest --co                    # Show conftest import order
```

## Test Filtering

```bash
pytest -k "test_login"         # Keyword match
pytest -k "not slow"           # Exclusion
pytest -m "api"                # Mark match
pytest --ignore=tests/legacy   # Skip directory
```

## Profile with --durations

```bash
pytest --durations=5           # Show 5 slowest tests
pytest --durations=0           # Show all durations
```

<!-- 🤔 Put settings in `pyproject.toml` (modern) or `pytest.ini` (compatible). -->

## Run the Code

```bash
pytest code/12-configuration.py -v
```
