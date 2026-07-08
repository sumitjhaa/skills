"""Pools — limit concurrent task execution."""
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

dag = DAG(
    "14_pools",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)


def limited_task(**kwargs):
    task_id = kwargs["ti"].task_id
    print(f"{task_id} is running (pool slot acquired)")


tasks = []
for i in range(6):
    t = PythonOperator(
        task_id=f"pool_task_{i}",
        python_callable=limited_task,
        pool="default_pool",
        pool_slots=1,
        dag=dag,
    )
    tasks.append(t)

# Create pool via CLI:
# airflow pools set my_pool 3 "Pool description"
