# Production Patterns

Running Airflow in production requires deliberate configuration around reliability, observability, and governance. This lesson covers the essential patterns: automatic retries with exponential backoff, email/Slack alerts on failures, DAG metadata for discoverability, and concurrency controls to prevent resource starvation.

## Key Concepts
- **`retries` & `retry_delay`** — automatic task retry on failure; configure at DAG level (default) or per-task
- **Email alerts** — `email_on_failure`, `email_on_retry`, `email` list; triggers an email when a task fails
- **`max_active_runs`** — caps the number of concurrent DAG runs for the same DAG; prevents overlapping runs
- **Tags** — filterable labels in the Airflow UI for organising DAGs by domain, team, or environment
- **`description`** — a human-readable summary shown in the DAG list view

## Code Example

References `../code/18-production-patterns.py`.

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "data_engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email_on_retry": False,
    "email": ["alerts@example.com"],
}

with DAG(
    dag_id="production_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["production", "etl"],
    description="Main production ETL pipeline — do not modify without code review.",
    default_args=default_args,
):
    extract = BashOperator(
        task_id="extract",
        bash_command="python /scripts/extract.py",
    )

    load = BashOperator(
        task_id="load",
        bash_command="python /scripts/load.py",
        retries=3,  # overrides DAG-level default
    )

    extract >> load
```

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/18-production-patterns.py /tmp/airflow_test/dags/
airflow dags test production_pipeline 2024-01-01
```

## Key Takeaways
- Set `default_args` to propagate `retries`, `retry_delay`, and alert settings to all tasks; override per-task where needed
- `max_active_runs=1` prevents concurrent runs for pipelines that must not overlap (e.g., sequential loads)
- Use tags (`["production", "etl"]`) for filtering; combine with `description` for discoverability
- Configure `email_on_failure` with a team distribution list so failures are visible immediately
- For Slack/PagerDuty alerts, use a custom `on_failure_callback` instead of email
