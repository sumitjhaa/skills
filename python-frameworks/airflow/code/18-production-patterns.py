"""Production Patterns — retries, email alerts, tags, description."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

default_args = {
    "owner": "data_team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["alerts@example.com"],
    "max_active_tis_per_dag": 3,
}

dag = DAG(
    "18_production_patterns",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["production", "etl"],
    description="Production ETL pipeline with retries and alerts",
    default_args=default_args,
    max_active_runs=1,
)


def safe_task(**kwargs):
    print("Task running with retry config")


t1 = PythonOperator(task_id="safe_task", python_callable=safe_task, dag=dag)
