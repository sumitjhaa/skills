# SubDAGs vs TaskGroups

Before TaskGroups, Airflow users grouped tasks using SubDAGs — separate DAG objects embedded inside a parent DAG. While SubDAGs still work, they come with significant drawbacks that make TaskGroups the preferred approach in modern Airflow.

## Key Concepts
- **SubDAG** — a full `DAG` object instantiated inside another DAG via `SubDagOperator`; runs in its own scope with its own scheduler and its own sequence numbers
- **TaskGroup** — a lightweight, purely-UI grouping mechanism introduced in Airflow 2.0; no separate DAG object, no extra scheduler overhead
- **Why TaskGroups are preferred** — no performance penalty, no cross-DAG scheduling issues, simpler code, better UI rendering, and full support for modern features like `trigger_rules`

## SubDAG Drawbacks

| Concern | SubDAG | TaskGroup |
|---|---|---|
| **Scheduler overhead** | Each SubDAG is a separate DAG; the scheduler treats it independently, increasing load | No extra overhead; all tasks belong to the same DAG |
| **Concurrency limits** | SubDAGs respect parent pool limits but have their own scheduler slots; easily leads to deadlocks | Parent DAG concurrency applies globally with no sub-scheduling |
| **Cross-DAG limits** | You cannot set dependencies between tasks inside and outside a SubDAG without `ExternalTaskSensor` | Tasks inside a Group wire directly with `>>` / `<<` |
| **UI experience** | SubDAGs open as a separate DAG view; navigation is clunky | Groups collapse inline in the same graph view |
| **Code complexity** | Requires a separate `dag()` factory function, deeper nesting, and more boilerplate | A single file, one `with TaskGroup(...)` context manager |

## Code Example — TaskGroup (Preferred)

References `../code/10-comparison-taskgroup.py`.

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup


def _extract() -> None:
    print("Extract")


def _load() -> None:
    print("Load")


with DAG(
    dag_id="taskgroup_approach",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
):
    start = EmptyOperator(task_id="start")

    with TaskGroup(group_id="etl") as etl:
        extract = PythonOperator(task_id="extract", python_callable=_extract)
        load = PythonOperator(task_id="load", python_callable=_load)
        extract >> load

    end = EmptyOperator(task_id="end")

    start >> etl >> end
```

## Code Example — SubDAG (Not Recommended)

References `../code/10-comparison-subdag.py`.

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.subdag import SubDagOperator


def _extract() -> None:
    print("Extract")


def _load() -> None:
    print("Load")


def etl_subdag(parent_dag_id: str, child_dag_id: str, args: dict) -> DAG:
    with DAG(
        dag_id=f"{parent_dag_id}.{child_dag_id}",
        start_date=args["start_date"],
        schedule=args["schedule"],
        catchup=args.get("catchup", False),
    ) as dag:
        extract = PythonOperator(
            task_id="extract",
            python_callable=_extract,
        )
        load = PythonOperator(
            task_id="load",
            python_callable=_load,
        )
        extract >> load
    return dag


with DAG(
    dag_id="subdag_approach",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:
    start = EmptyOperator(task_id="start")

    etl = SubDagOperator(
        task_id="etl",
        subdag=etl_subdag("subdag_approach", "etl", dag.default_args or {}),
    )

    end = EmptyOperator(task_id="end")

    start >> etl >> end
```

The SubDAG version requires a factory function, a separate `DAG(...)` context, and careful argument passing. It also introduces a hidden DAG (`subdag_approach.etl`) that the scheduler will scan — increasing overhead for no benefit.

## Running the DAGs

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/10-comparison-taskgroup.py /tmp/airflow_test/dags/
cp ../code/10-comparison-subdag.py /tmp/airflow_test/dags/
airflow dags list
airflow dags test taskgroup_approach 2024-01-01
airflow dags test subdag_approach 2024-01-01
```

## Key Takeaways
- **Always prefer TaskGroups over SubDAGs** for new code
- SubDAGs add scheduler load, deadlock risk, and boilerplate code
- TaskGroups are zero-overhead, render beautifully in the UI, and support all modern Airflow features
- The only remaining use case for SubDAGs is if you need a **separate, reusable** DAG definition that lives in its own file — but even then, consider importing the DAG directly instead of nesting it
