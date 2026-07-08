"""SLAs & timeouts — set task-level and DAG-level SLAs."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

dag = DAG(
    "15_slas_timeouts",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    sla_miss_callback=lambda *args, **kwargs: print("SLA missed!"),
)


def slow_task(**kwargs):
    import time
    time.sleep(2)
    print("Slow task completed")


t1 = PythonOperator(
    task_id="slow_task",
    python_callable=slow_task,
    execution_timeout=timedelta(seconds=10),
    sla=timedelta(seconds=5),
    dag=dag,
)
