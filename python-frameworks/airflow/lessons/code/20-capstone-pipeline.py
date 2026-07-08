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
