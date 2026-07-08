from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def _extract() -> None:
    print("Extracting data")


def _transform() -> None:
    print("Transforming data")


def _load() -> None:
    print("Loading data")


with DAG(
    dag_id="testing_demo",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
):
    extract = PythonOperator(task_id="extract", python_callable=_extract)
    transform = PythonOperator(task_id="transform", python_callable=_transform)
    load = PythonOperator(task_id="load", python_callable=_load)

    extract >> transform >> load
