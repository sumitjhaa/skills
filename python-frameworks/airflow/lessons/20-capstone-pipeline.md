# Capstone Pipeline

This capstone lesson combines everything from Phase 02 into a realistic pipeline: dynamic task generation, a custom operator, hooks for secure connections, TaskGroups for organisation, XComs for data passing, and quality checks with conditional branching. The pipeline processes a batch of files from an SFTP server, validates each file, and loads it into a database.

## Key Concepts
- **Dynamic tasks** — create one task per file using a loop over a list of filenames
- **Custom operators** — encapsulate the file-processing logic in a reusable `FileProcessorOperator`
- **Hooks** — use `BaseHook` to retrieve SFTP and database credentials
- **XComs** — pass file metadata and quality-check results between tasks
- **TaskGroups** — group the quality-check sub-pipeline for a cleaner graph view
- **Branching** — skip the load step when quality checks fail

## Code Example

References `../code/20-capstone-pipeline.py`.

```python
from __future__ import annotations

from datetime import datetime
from typing import Any

from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from airflow.models import BaseOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.context import Context
from airflow.utils.task_group import TaskGroup

FILES = ["sales_20240101.csv", "sales_20240102.csv"]


class FileProcessorOperator(BaseOperator):
    def __init__(self, filename: str, **kwargs: Any):
        super().__init__(**kwargs)
        self.filename = filename

    def execute(self, context: Context) -> dict:
        conn = BaseHook.get_connection("sftp_target")
        self.log.info("Fetching %s from %s", self.filename, conn.host)
        result = {"filename": self.filename, "rows": 1200, "status": "ok"}
        return result


def _should_load(**kwargs: Any) -> str:
    ti = kwargs["ti"]
    results = ti.xcom_pull(key="return_value", task_ids=[
        f"process_{f.replace('.', '_')}" for f in FILES
    ])
    for r in results:
        if r and r.get("status") != "ok":
            return "skip_load"
    return "load_data"


@dag(
    dag_id="capstone_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
)
def capstone() -> None:
    for f in FILES:
        task_id = f"process_{f.replace('.', '_')}"
        FileProcessorOperator(task_id=task_id, filename=f)

    with TaskGroup(group_id="quality_checks") as quality:
        check = BranchPythonOperator(
            task_id="check_quality",
            python_callable=_should_load,
        )

        @task(task_id="skip_load")
        def log_skip() -> None:
            print("Quality checks failed — skipping load.")

        check >> log_skip()

    @task(task_id="load_data")
    def load() -> None:
        print("Loading data into warehouse...")

    quality >> load()


capstone()
```

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/20-capstone-pipeline.py /tmp/airflow_test/dags/
airflow dags test capstone_pipeline 2024-01-01
```

## Key Takeaways
- Dynamic task generation (iterating over `FILES`) keeps the DAG concise when the workload varies by a parameter
- A custom operator (`FileProcessorOperator`) encapsulates reusable file-processing logic with hook-based credential retrieval
- TaskGroups visually organise the quality-check sub-pipeline without adding scheduler overhead
- XComs pass results between dynamically generated tasks and the branching decision point
- BranchPythonOperator conditionally skips the load on quality failure, demonstrating defensive pipeline design
