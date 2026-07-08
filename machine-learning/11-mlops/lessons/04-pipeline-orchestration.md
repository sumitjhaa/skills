# 11.04 Pipeline Orchestration

## Objective
Schedule, monitor, and retry ML workflows with **Airflow** and **Prefect**.

## Apache Airflow
- DAG-based scheduler (Python).
- Operators: `PythonOperator`, `BashOperator`, `DockerOperator`.
- Sensors: wait for external events (file, API).

```python
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG("ml_pipeline", schedule_interval="@daily") as dag:
    task_extract = PythonOperator(task_id="extract", python_callable=extract)
    task_train = PythonOperator(task_id="train", python_callable=train)
    task_extract >> task_train
```

## Prefect
- Async, imperative flow orchestration.
- Automatic retries, caching, state persistence.
- Prefect Cloud / Server UI.

```python
from prefect import flow, task

@task(retries=2)
def train_model(data):
    ...

@flow
def ml_workflow():
    data = extract()
    model = train_model(data)
    deploy(model)
```

## Comparison
| Feature | Airflow | Prefect |
|---------|---------|---------|
| Scheduling | Cron-based | Event + cron |
| Backfill | Native | `run` with params |
| Caching | XCom | `task_cache` |
| Deployment | `airflow deploy` | `prefect deploy` |

## Best Practices
1. Keep tasks idempotent.
2. Use `short_circuit` / conditional branching for data checks.
3. Set SLA alerts on critical production DAGs.
4. Pin container images for reproducible runs.
