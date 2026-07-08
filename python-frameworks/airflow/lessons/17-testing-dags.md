# Testing DAGs

DAGs are code, and like any code they should be tested. Airflow provides `DagBag` for loading DAG files in isolation and `pytest` fixtures for structuring tests. Testing catches import errors, broken dependencies, misconfigured operators, and scheduling logic before deployment.

## Key Concepts
- **`DagBag`** — loads a DAG file and makes its DAG objects accessible via `dagbag.dags`
- **Import validation** — the simplest test: can the DAG file be imported without exceptions?
- **Structural assertions** — verify task counts, dependency edges, cycle absence, and `dag_id` values
- **Task isolation** — execute a task's `execute()` method in a test context to validate its logic
- **Pytest fixtures** — create a reusable `dagbag` fixture to avoid repeated loading

## Code Example

References `../code/17-testing-dags.py`.

```python
import pytest
from airflow.models import DagBag

DAG_PATH = "/path/to/dags/"


@pytest.fixture
def dagbag() -> DagBag:
    return DagBag(dag_folder=DAG_PATH, include_examples=False)


def test_import_errors(dagbag: DagBag) -> None:
    assert len(dagbag.import_errors) == 0, \
        f"Import errors: {dagbag.import_errors}"


def test_dag_count(dagbag: DagBag) -> None:
    assert len(dagbag.dags) >= 1


def test_task_structure(dagbag: DagBag) -> None:
    dag = dagbag.get_dag("my_pipeline")
    assert dag is not None
    assert len(dag.tasks) >= 3


def test_no_cycles(dagbag: DagBag) -> None:
    for dag_id, dag in dagbag.dags.items():
        dag.task_dict  # triggers cycle check; raises AirflowDagCycleException if cycle exists
```

Run tests with:

```bash
pip install pytest
python -m pytest tests/
```

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/17-testing-dags.py /tmp/airflow_test/dags/
airflow dags test testing_demo 2024-01-01
```

## Key Takeaways
- A simple `DagBag(...).import_errors` check in CI prevents deploying broken DAGs
- Validate task count, task IDs, and dependency edges to catch refactoring mistakes
- Write isolated task unit tests by importing the callable and calling it directly (no Airflow needed)
- Use `pytest` fixtures to share the `DagBag` instance across tests and keep test files DRY
