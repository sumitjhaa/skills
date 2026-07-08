from __future__ import annotations

from datetime import datetime
from typing import Any

import requests
from airflow import DAG
from airflow.hooks.base import BaseHook
from airflow.operators.python import PythonOperator


def _fetch_from_api() -> None:
    conn = BaseHook.get_connection("my_api")
    headers = {"Authorization": f"Bearer {conn.password}"}
    resp = requests.get(
        f"https://{conn.host}/data",
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    print(resp.json())


with DAG(
    dag_id="hooks_demo",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
):
    fetch = PythonOperator(
        task_id="fetch_data",
        python_callable=_fetch_from_api,
    )
