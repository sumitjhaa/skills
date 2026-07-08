from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def _validate() -> None:
    print("Running CI validation checks")


with DAG(
    dag_id="cicd_demo",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
):
    validate = PythonOperator(
        task_id="validate_dags",
        python_callable=_validate,
    )
