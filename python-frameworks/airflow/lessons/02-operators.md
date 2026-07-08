# Operators

Operators are the building blocks of an Airflow DAG. Each operator defines a single unit of work and knows how to execute it. Airflow ships with a wide set of built-in operators for common tasks.

## Key Concepts
- **PythonOperator** — executes any Python callable; the most flexible operator
- **BashOperator** — runs an arbitrary bash command in a temporary shell
- **EmptyOperator** — a no-op placeholder; useful for grouping or structuring a DAG
- **Built-in operators** — Airflow includes operators for SQL (e.g., `PostgresOperator`, `SnowflakeOperator`), file transfer (`S3FileTransformOperator`), cloud services (`GCSObjectExistenceSensor`), and many more

## Code Example

References `../code/02-operators.py`.

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


def _extract() -> dict:
    return {"data": [1, 2, 3]}

def _transform(ti) -> None:
    payload = ti.xcom_pull(task_ids="extract")
    print(f"Transformed {payload}")

with DAG(
    dag_id="operator_examples",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
):
    start = EmptyOperator(task_id="start")

    extract = PythonOperator(
        task_id="extract",
        python_callable=_extract,
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=_transform,
    )

    cleanup = BashOperator(
        task_id="cleanup",
        bash_command="echo 'Cleaning up...' && rm -f /tmp/extract_output",
    )

    end = EmptyOperator(task_id="end")
```

Each operator is instantiated with a unique `task_id` and the configuration it needs. `BashOperator` accepts a `bash_command` string; `PythonOperator` takes a `python_callable`.

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/02-operators.py /tmp/airflow_test/dags/
airflow dags list
airflow dags test operator_examples 2024-01-01
```

## Key Takeaways
- Operators are instantiated tasks; a DAG is a set of operator instances wired together
- `PythonOperator` is the go-to for custom logic; `BashOperator` is ideal for shell commands or scripts
- `EmptyOperator` acts as a marker — useful for `start` / `end` sentinels in a pipeline
- When a built-in operator fits (e.g., `PostgresOperator`), prefer it over manual scripting
