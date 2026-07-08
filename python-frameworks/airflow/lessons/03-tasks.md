# Tasks

A task is an instance of an operator that runs within a DAG. When a DAG Run is created, Airflow instantiates each operator into a Task Instance — the runtime representation of a single task execution.

## Key Concepts
- **Task Instance** — an object that tracks the state (queued, running, success, failed, etc.) of a single task execution for a specific DAG Run
- **Execution** — Airflow's scheduler picks up queued Task Instances and hands them to workers; each task is retried on failure based on `retries` configuration
- **task_id conventions** — `task_id` values must be unique **within** a DAG; convention uses `snake_case` (e.g., `load_data`, `validate_schema`); task_ids appear in the UI logs, XCom keys, and stack traces, so descriptive names matter

## Code Example

References `../code/03-tasks.py`.

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def _fetch_data() -> None:
    print("Fetching data from API ...")
    # simulate work
    import time
    time.sleep(2)


def _validate() -> None:
    print("Validating fetched data ...")


def _store() -> None:
    print("Storing data to database ...")


with DAG(
    dag_id="task_concepts",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"retries": 2},
):
    fetch_data = PythonOperator(
        task_id="fetch_data",
        python_callable=_fetch_data,
    )

    validate = PythonOperator(
        task_id="validate",
        python_callable=_validate,
    )

    store = PythonOperator(
        task_id="store",
        python_callable=_store,
    )

    fetch_data >> validate >> store
```

Each `PythonOperator` creates a distinct task in the DAG. When the DAG triggers, Airflow creates a Task Instance per task per DAG Run. The `task_id` (`fetch_data`, `validate`, `store`) is how you identify the task in logs, metrics, and the UI.

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/03-tasks.py /tmp/airflow_test/dags/
airflow dags list
airflow dags test task_concepts 2024-01-01
```

## Key Takeaways
- A Task Instance is the runtime record of a task; its state lifecycle is: `scheduled` → `queued` → `running` → `success` (or `failed` → up for retry)
- `task_id` must be unique per DAG; use descriptive `snake_case` names
- `default_args` propagates to every task in the DAG, saving repetitive configuration
