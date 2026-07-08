# SLAs & Timeouts

Service-Level Agreements (SLAs) and timeouts let you enforce pipeline reliability. A timeout kills a task or DAG run that exceeds its duration bound. An SLA miss callback fires when a task takes longer than its SLA window — without killing it — so you can alert, log, or trigger remediation.

## Key Concepts
- **`execution_timeout`** — maximum runtime for a single task; raises `AirflowTaskTimeout` if exceeded
- **`dagrun_timeout`** — maximum runtime for an entire DAG run; if exceeded the run is marked as `failed`
- **`sla`** — a `timedelta` set on a task; when a task's duration exceeds this, Airflow fires `sla_miss_callback`
- **`sla_miss_callback`** — a callable invoked with details about the missed SLA
- **Difference** — timeouts **kill**, SLAs **notify**

## Code Example

References `../code/15-slas-timeouts.py`.

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def _sla_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    print(f"SLA missed on DAG {dag.dag_id}")
    for sla in slas:
        print(f"Task {sla.task_id} expected by {sla.end_date}")


def _slow_task() -> None:
    import time
    time.sleep(20)


with DAG(
    dag_id="sla_timeout_demo",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    dagrun_timeout=timedelta(minutes=30),
    sla_miss_callback=_sla_callback,
):
    critical = PythonOperator(
        task_id="critical_etl",
        python_callable=_slow_task,
        execution_timeout=timedelta(minutes=5),
        sla=timedelta(minutes=2),
    )
```

If `critical_etl` runs for more than 2 minutes, the SLA callback fires. If it exceeds 5 minutes, the task is killed. If the entire DAG run exceeds 30 minutes, it is marked failed.

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/15-slas-timeouts.py /tmp/airflow_test/dags/
airflow dags test sla_timeout_demo 2024-01-01
```

## Key Takeaways
- `execution_timeout` is per-task; `dagrun_timeout` is per-DAG-run — use both for defence in depth
- SLA miss callbacks are a monitoring tool, not a kill switch — the task continues running
- SLAs are checked by the `SlaMissTimer` scheduler loop, which runs every minute by default
- Set SLAs only on meaningful tasks (e.g., critical ETL steps) to avoid notification spam
