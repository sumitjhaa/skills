# Task Groups

Task Groups allow you to visually and logically group tasks in the Airflow UI. They are a lightweight grouping mechanism that collapses into a single node in the graph view, making complex DAGs much more readable.

## Key Concepts
- **TaskGroup context manager** — use `with TaskGroup(group_id="...") as group:` to wrap a set of tasks; all tasks defined inside belong to the group
- **UI grouping** — in the Airflow web UI, groups are rendered as collapsible containers; clicking expands them to reveal individual tasks
- **Nested groups** — TaskGroups can be nested inside other TaskGroups, creating a hierarchy in the UI
- **Prefix convention** — each task inside a group has its `task_id` automatically prefixed with `group_id.` (e.g., `data_prep.extract`, `data_prep.transform`)

## Code Example

References `../code/09-task-groups.py`.

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup


def _extract() -> None:
    print("Extracting ...")


def _transform() -> None:
    print("Transforming ...")


def _load() -> None:
    print("Loading ...")


with DAG(
    dag_id="task_group_demo",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
):
    start = EmptyOperator(task_id="start")

    with TaskGroup(group_id="data_prep") as data_prep:
        extract = PythonOperator(task_id="extract", python_callable=_extract)
        transform = PythonOperator(task_id="transform", python_callable=_transform)
        load = PythonOperator(task_id="load", python_callable=_load)
        extract >> transform >> load

    with TaskGroup(group_id="reporting") as reporting:
        build_report = EmptyOperator(task_id="build_report")
        send_report = EmptyOperator(task_id="send_report")
        build_report >> send_report

    end = EmptyOperator(task_id="end")

    start >> data_prep >> reporting >> end
```

The `data_prep` group in the UI shows as a single bordered rectangle containing `extract`, `transform`, and `load`. The `reporting` group is another collapsible block. Task IDs under the hood become `data_prep.extract`, `data_prep.transform`, etc., keeping the namespace clean.

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/09-task-groups.py /tmp/airflow_test/dags/
airflow dags list
airflow dags test task_group_demo 2024-01-01
```

## Key Takeaways
- Use TaskGroups to organize related tasks without changing the underlying DAG topology
- Tasks inside a TaskGroup get an automatic `group_id.` prefix on their `task_id`
- Groups can be nested for deep hierarchies; the UI renders them as expandable folders
- TaskGroups are purely a UI and organisational feature — they do **not** affect execution semantics
