from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any

from airflow import DAG
from airflow.models import BaseOperator
from airflow.operators.python import PythonOperator
from airflow.triggers.base import BaseTrigger, TriggerEvent
from airflow.utils.context import Context


class FileSensorTrigger(BaseTrigger):
    def __init__(self, filepath: str):
        super().__init__()
        self.filepath = filepath

    def serialize(self) -> tuple[str, dict[str, Any]]:
        return ("file_sensor_trigger", {"filepath": self.filepath})

    async def run(self):
        while True:
            try:
                with open(self.filepath) as f:
                    content = f.read()
                yield TriggerEvent({"content": content})
                return
            except FileNotFoundError:
                await asyncio.sleep(5)


class DeferrableFileSensor(BaseOperator):
    def __init__(self, filepath: str, **kwargs: Any):
        super().__init__(**kwargs)
        self.filepath = filepath

    def execute(self, context: Context) -> None:
        self.defer(
            trigger=FileSensorTrigger(filepath=self.filepath),
            method_name="resume",
        )

    def resume(self, context: Context, event: dict[str, Any] | None = None) -> None:
        if event:
            self.log.info("File found with content: %s", event["content"][:100])


with DAG(
    dag_id="deferrable_demo",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
):
    wait_for_file = DeferrableFileSensor(
        task_id="wait_for_file",
        filepath="/tmp/data_ready.signal",
    )

    def _next_step() -> None:
        print("Proceeding with next step")

    next_step = PythonOperator(
        task_id="next_step",
        python_callable=_next_step,
    )

    wait_for_file >> next_step
