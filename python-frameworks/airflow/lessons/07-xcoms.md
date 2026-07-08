# XComs

XComs (short for "cross-communications") let tasks share small amounts of data. A task pushes a value to XCom, and another task pulls it — either by key or automatically from the return value.

## Key Concepts
- **Push** — a task sends data to XCom with `ti.xcom_push(key="my_key", value=...)` or by simply returning a value
- **Pull** — a receiving task calls `ti.xcom_pull(task_ids="sender_id", key="my_key")` to retrieve the data
- **Return values** — any value returned by a `python_callable` is automatically pushed to XCom under the key `"return_value"`
- **XCom key conventions** — use descriptive keys like `"user_ids"`, `"api_response"`, `"file_path"` instead of the default `"return_value"` when a task produces multiple pieces of data

## Code Example

References `../code/07-xcoms.py`.

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def _generate_user_ids(**context) -> list[int]:
    """Return value is auto-pushed to XCom under 'return_value'."""
    return [101, 102, 103]


def _process_user(ti, **context) -> None:
    # Pull the return_value from the upstream task
    user_ids = ti.xcom_pull(task_ids="generate_user_ids", key="return_value")
    print(f"Processing users: {user_ids}")

    # Also push additional data manually
    ti.xcom_push(key="processed_count", value=len(user_ids))


def _report(ti, **context) -> None:
    processed = ti.xcom_pull(task_ids="process_user", key="processed_count")
    print(f"Processed {processed} users total.")


with DAG(
    dag_id="xcom_demo",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
):
    generate_user_ids = PythonOperator(
        task_id="generate_user_ids",
        python_callable=_generate_user_ids,
    )

    process_user = PythonOperator(
        task_id="process_user",
        python_callable=_process_user,
    )

    report = PythonOperator(
        task_id="report",
        python_callable=_report,
    )

    generate_user_ids >> process_user >> report
```

When `generate_user_ids` runs, its return value `[101, 102, 103]` is automatically pushed to XCom under the key `"return_value"`. The `process_user` task pulls that value and then pushes its own custom key `"processed_count"`. The `report` task pulls that custom key downstream.

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/07-xcoms.py /tmp/airflow_test/dags/
airflow dags list
airflow dags test xcom_demo 2024-01-01
```

## Key Takeaways
- Return values are automatically pushed to XCom under the `"return_value"` key
- Use `ti.xcom_push(key, value)` for custom keys; use `ti.xcom_pull(task_ids, key)` to retrieve them
- XComs are stored in the Airflow metadata database; they are **not** designed for large data (keep values under a few MB)
- For large data, push a file path or object storage key instead of the data itself
