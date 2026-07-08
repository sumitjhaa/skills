from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def _api_call(task_id: str) -> None:
    print(f"Executing {task_id}")


with DAG(
    dag_id="pool_demo",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
):
    task_a = PythonOperator(
        task_id="api_call_a",
        python_callable=_api_call,
        op_kwargs={"task_id": "api_call_a"},
        pool="external_api",
        pool_slots=1,
    )

    task_b = PythonOperator(
        task_id="api_call_b",
        python_callable=_api_call,
        op_kwargs={"task_id": "api_call_b"},
        pool="external_api",
        pool_slots=1,
    )
