# Pools

Pools limit the concurrency of tasks across the entire Airflow installation. They are useful when an external resource (e.g., a database connection pool, an API rate limit) must not be overwhelmed, even when many DAGs or DAG runs run simultaneously.

## Key Concepts
- **`pool`** — a named slot quota; tasks that belong to a pool can only run while slots are available
- **`pool_slots`** — how many slots a single task consumes (default 1)
- **`default_pool`** — a built-in pool with 128 slots; tasks without an explicit `pool` use it
- **Priority weights** — within a pool, tasks with higher `priority_weight` run first
- **CLI management** — create, list, and delete pools without the UI

## Code Example

References `../code/14-pools.py`.

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def _api_call(task_id: str) -> None:
    print(f"Executing {task_id}")


with DAG(
    dag_id="pool_demo",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
):
    task_a = PythonOperator(
        task_id="api_call_a",
        python_callable=_api_call,
        op_kwargs={"task_id": "api_call_a"},
        pool="external_api",
        pool_slots=1,
    )

    task_b = PythonOperator(
        task_id="api_call_b",
        python_callable=_api_call,
        op_kwargs={"task_id": "api_call_b"},
        pool="external_api",
        pool_slots=1,
    )
```

Manage the pool from the CLI:

```bash
airflow pools set external_api 5 "Limits concurrent calls to the external API"
airflow pools list
airflow pools get external_api
```

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/14-pools.py /tmp/airflow_test/dags/
airflow pools set external_api 5 "Limit external API calls"
airflow dags test pool_demo 2024-01-01
```

## Key Takeaways
- Pools cap concurrent task execution for shared, rate-limited resources
- Create pools before they are referenced by a DAG to avoid scheduler warnings
- Tasks without an explicit `pool` default to `default_pool` (128 slots)
- Use `priority_weight` and `pool_slots` together to control execution order within a pool
- Monitor pool usage in the Airflow UI under **Browse → Pools**
