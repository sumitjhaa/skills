# Dynamic DAGs

Airflow DAGs are just Python objects, so you can generate them programmatically using loops, functions, and factories. Dynamic DAG generation lets you create many similar DAGs from a single template — ideal for multi-tenant pipelines, per-client workflows, or data-source-specific processing.

## Key Concepts
- **DAG factory** — a function that accepts parameters and returns a `DAG` object
- **`globals()` registration** — assigning a DAG to a module-level variable (or `globals()`) so Airflow's `DagBag` discovers it
- **Parameterised DAGs** — using `schedule`, `start_date`, or task configuration as function arguments
- **Loop-driven tasks** — building task sets by iterating over a list of configs

## Code Example

References `../code/11-dynamic-dags.py`.

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

CUSTOMERS = ["acme", "globex", "initech"]


def _process_customer(customer: str) -> None:
    print(f"Processing {customer}")


def build_dag(customer: str) -> DAG:
    with DAG(
        dag_id=f"process_{customer}",
        start_date=datetime(2024, 1, 1),
        schedule="@daily",
        catchup=False,
        description=f"Pipeline for customer {customer}",
    ) as dag:
        PythonOperator(
            task_id=f"process_{customer}",
            python_callable=_process_customer,
            op_kwargs={"customer": customer},
        )
    return dag


for customer in CUSTOMERS:
    globals()[f"dag_process_{customer}"] = build_dag(customer)
```

The loop iterates over `CUSTOMERS` and injects each generated DAG into `globals()`. Airflow's `DagBag` scanner picks up any module-level variable that is a `DAG` instance.

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/11-dynamic-dags.py /tmp/airflow_test/dags/
airflow dags list
airflow dags test process_acme 2024-01-01
airflow dags test process_globex 2024-01-01
```

## Key Takeaways
- Assigning a DAG to `globals()` is the standard way to register dynamically generated DAGs
- Keep factory functions in a separate module and import them to keep the DAG file clean
- Each dynamic DAG needs a unique `dag_id` — use string formatting with the differentiating parameter
- Dynamic DAGs are parsed on every `dagbag` refresh; avoid expensive I/O inside the factory function
