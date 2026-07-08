# Branching

Branching allows a DAG to dynamically choose which path to follow at runtime based on a condition. `BranchPythonOperator` returns the `task_id` (or list of `task_id`s) of the next task to run.

## Key Concepts
- **BranchPythonOperator** — a PythonOperator whose callable returns the `task_id` (or a list of `task_id`s) of the downstream task(s) to execute; all other downstream branches are skipped
- **Trigger rules** — define when a task should run; `all_success` (default), `all_failed`, `one_success`, `one_failed`, `all_done`, `none_failed`, `none_skipped`, `dummy`
- **Merge pattern** — after a branch, a downstream task with `trigger_rule="none_failed"` or `"all_done"` runs regardless of which branch was taken, allowing the pipeline to rejoin

## Code Example

References `../code/08-branching.py`.

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator


def _choose_branch(**context) -> str:
    # Logic to decide which branch to take
    day_of_week = context["logical_date"].isoweekday()
    if day_of_week <= 5:
        return "weekday_process"
    return "weekend_process"


with DAG(
    dag_id="branching_demo",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
):
    start = EmptyOperator(task_id="start")

    choose_branch = BranchPythonOperator(
        task_id="choose_branch",
        python_callable=_choose_branch,
    )

    weekday_process = EmptyOperator(task_id="weekday_process")
    weekend_process = EmptyOperator(task_id="weekend_process")

    # Merge point — runs no matter which branch was taken
    merge = EmptyOperator(
        task_id="merge",
        trigger_rule="none_failed",
    )

    end = EmptyOperator(task_id="end")

    start >> choose_branch
    choose_branch >> weekday_process >> merge
    choose_branch >> weekend_process >> merge
    merge >> end
```

When `choose_branch` executes, it returns either `"weekday_process"` or `"weekend_process"`. Airflow skips the unchosen branch entirely. The merge task uses `trigger_rule="none_failed"` so it runs as long as the chosen branch succeeded — it is not blocked by the skipped branch.

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/08-branching.py /tmp/airflow_test/dags/
airflow dags list
airflow dags test branching_demo 2024-01-01
```

## Key Takeaways
- `BranchPythonOperator` returns the `task_id` of the branch(es) to execute; everything else is skipped
- Use `trigger_rule="none_failed"` or `"all_done"` at merge points so the DAG rejoins cleanly
- The default trigger rule is `all_success` — this will cause a merge task to wait **forever** if a branch is skipped
- You can return a **list** of `task_id`s to take multiple branches simultaneously
