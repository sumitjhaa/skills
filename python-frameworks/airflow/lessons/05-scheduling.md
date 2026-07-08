# Scheduling

Scheduling is what makes Airflow a batch workflow platform rather than just a task runner. The scheduler continuously evaluates DAGs and creates DAG Runs based on the schedule defined, skipping future intervals and backfilling past ones as needed.

## Key Concepts
- **Cron expressions** — standard five-field cron syntax: `minute hour day month day_of_week` (e.g., `0 9 * * 1` = every Monday at 09:00 UTC)
- **@presets** — shorthand strings: `@daily` (midnight), `@hourly`, `@weekly`, `@monthly`, `@yearly`, and `@once`
- **Data interval** — the time range a DAG Run covers (e.g., for a `@daily` schedule, the data interval for the run at 2024-01-02 is `[2024-01-01, 2024-01-02)`)
- **Schedule vs logical date** — the `logical_date` (previously `execution_date`) marks the **start** of the data interval; the DAG Run is created **after** the interval ends. For a `@daily` DAG starting at 2024-01-01, the run covering Jan 1 data has a `logical_date` of 2024-01-01 but actually executes shortly after 2024-01-02 00:00:00

## Code Example

References `../code/05-scheduling.py`.

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def _show_schedule_info(logical_date: str, dag_run=None) -> None:
    print(f"Logical date (start of data interval): {logical_date}")
    print(f"DAG Run scheduled execution: {dag_run.execution_date if dag_run else 'N/A'}")
    data_interval_start = dag_run.data_interval_start if dag_run else "N/A"
    data_interval_end = dag_run.data_interval_end if dag_run else "N/A"
    print(f"Data interval: [{data_interval_start}, {data_interval_end})")


with DAG(
    dag_id="scheduling_examples",
    start_date=datetime(2024, 1, 1),
    # Runs at 09:00 UTC every Monday
    schedule="0 9 * * 1",
    catchup=False,
    max_active_runs=1,
):
    show_schedule = PythonOperator(
        task_id="show_schedule_info",
        python_callable=_show_schedule_info,
        op_args=["{{ logical_date }}"],
    )
```

The `logical_date` Jinja template variable gives you the start of the data interval. The `schedule` determines the cadence; a run for Monday's data interval starts at 09:00 on the following Monday, not Monday midnight.

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/05-scheduling.py /tmp/airflow_test/dags/
airflow dags list
airflow dags test scheduling_examples 2024-01-01
```

## Key Takeaways
- Cron strings give full control; `@presets` are convenient for common cadences
- The `logical_date` (formerly `execution_date`) is the start of the data interval, not when the run executes
- DAG Runs are created after the data interval completes — Airflow guarantees the data is ready before the run starts
- `catchup=True` creates DAG Runs for every missed interval since `start_date`; use with caution on long-running pipelines
