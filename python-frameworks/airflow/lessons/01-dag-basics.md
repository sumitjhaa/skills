# DAG Basics

A DAG (Directed Acyclic Graph) is the core concept of Airflow — it defines a collection of tasks with dependencies that run on a schedule. Every DAG is a Python script that declares the graph structure.

## Key Concepts
- **DAG definition** — instantiate `DAG()` with a `dag_id`, `start_date`, `schedule`, and `catchup`
- **start_date** — the date from which the DAG's schedule begins (in UTC); Airflow will create DAG Runs from this date onward
- **schedule** — defines how often the DAG runs; can be a cron string or one of the `@` presets
- **catchup** — when `True`, Airflow creates DAG Runs for every interval between `start_date` and now that hasn't been run yet
- **PythonOperator** — the simplest operator; executes any Python callable as a task

## Code Example

References `../code/01-dag-basics.py`.

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def _print_hello() -> None:
    print("Hello from Airflow!")


with DAG(
    dag_id="dag_basics",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    description="A minimal DAG demonstrating core concepts.",
):
    hello_task = PythonOperator(
        task_id="print_hello",
        python_callable=_print_hello,
    )
```

The DAG is created using a context manager (`with DAG(...):`). Everything indented inside it belongs to that DAG. The `PythonOperator` wraps `_print_hello` so Airflow can execute it as a task.

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/01-dag-basics.py /tmp/airflow_test/dags/
airflow dags list
airflow dags test dag_basics 2024-01-01
```

## Key Takeaways
- Every DAG needs a unique `dag_id`, a `start_date`, and a `schedule`
- The `with DAG(...)` context manager is the idiomatic way to define a DAG
- `catchup=False` prevents backfilling past intervals automatically
- `PythonOperator` is the most common operator for arbitrary Python logic
