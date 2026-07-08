"""DAG basics — define a minimal DAG with one task."""
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


def hello(**kwargs):
    print("Hello from Airflow!")


dag = DAG(
    "01_dag_basics",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    description="A minimal DAG with one Python task",
)

t1 = PythonOperator(task_id="hello_task", python_callable=hello, dag=dag)
