# CI/CD for Airflow

Airflow DAGs need the same rigour as application code: linting, type checking, unit tests, and automated deployment. A CI/CD pipeline catches broken imports, syntax errors, and structural problems before they reach production. Deployment strategies range from simple file sync (rsync) to Git-sync sidecars and image-based deployments.

## Key Concepts
- **DAG validation** — run `DagBag(dag_folder=...)` and assert zero `import_errors` in CI
- **Linting** — use `ruff`, `pylint`, or `mypy` to enforce code quality on DAG files and plugins
- **Import tests** — verify that every module in the `dags/` directory can be imported without an Airflow instance
- **Git-sync** — a sidecar container that syncs DAGs from a Git repo into the DAG folder on a schedule; native support via `airflow.kubernetes` executor
- **Rsync / CI push** — build step copies DAG files to the Airflow server (simple but less traceable)
- **Image-based** — bake DAGs into a custom Docker image; promotes immutable deployments

## Code Example

References `../code/19-cicd-airflow.py`.

```python
"""CI validation script — run in your CI pipeline."""

import sys
from pathlib import Path

from airflow.models import DagBag


def main() -> None:
    dag_folder = Path(__file__).parent / "dags"
    dagbag = DagBag(dag_folder=str(dag_folder), include_examples=False)

    errors = dagbag.import_errors
    if errors:
        print("DAG import errors found:")
        for filepath, error in errors.items():
            print(f"  {filepath}: {error}")
        sys.exit(1)

    print(f"Successfully loaded {len(dagbag.dags)} DAG(s)")


if __name__ == "__main__":
    main()
```

Example CI workflow (GitHub Actions):

```yaml
name: Validate DAGs
on: [push]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install apache-airflow
      - run: python ci/validate_dags.py
```

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/19-cicd-airflow.py /tmp/airflow_test/dags/
airflow dags test cicd_demo 2024-01-01
```

## Key Takeaways
- The most valuable CI check is `DagBag(...).import_errors == 0` — it catches missing imports, syntax errors, and configuration typos
- Add linting (`ruff`) and type checking (`mypy`) to maintain code quality across the team
- For deployment, prefer Git-sync or image-based deployments for traceability and rollback support
- Pin Airflow and provider versions in CI to avoid surprises when new releases arrive
- Test DAGs against a lightweight SQLite database in CI (set `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` to `sqlite:////tmp/ci.db`)
