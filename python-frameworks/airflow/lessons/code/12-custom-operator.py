from __future__ import annotations

from datetime import datetime
from typing import Any

import requests
from airflow import DAG
from airflow.models import BaseOperator
from airflow.operators.python import PythonOperator
from airflow.utils.context import Context


class ApiFetchOperator(BaseOperator):
    """Fetches data from a REST API and pushes the response via XCom."""

    def __init__(self, endpoint: str, method: str = "GET", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.endpoint = endpoint
        self.method = method

    def execute(self, context: Context) -> dict:
        resp = requests.request(self.method, self.endpoint, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        self.log.info("Fetched %d records from %s", len(data), self.endpoint)
        return data


with DAG(
    dag_id="custom_operator_demo",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
):
    fetch_task = ApiFetchOperator(
        task_id="fetch_users",
        endpoint="https://api.example.com/users",
    )
