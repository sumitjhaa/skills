from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "data_engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email_on_retry": False,
    "email": ["alerts@example.com"],
}

with DAG(
    dag_id="production_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["production", "etl"],
    description="Main production ETL pipeline — do not modify without code review.",
    default_args=default_args,
):
    extract = BashOperator(
        task_id="extract",
        bash_command="python /scripts/extract.py",
    )

    load = BashOperator(
        task_id="load",
        bash_command="python /scripts/load.py",
        retries=3,
    )

    extract >> load
