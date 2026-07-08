"""Operators — PythonOperator, BashOperator, EmptyOperator."""
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator


def python_task(**kwargs):
    print("PythonOperator executed")


dag = DAG(
    "02_operators",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)

start = EmptyOperator(task_id="start", dag=dag)
py_task = PythonOperator(task_id="py_task", python_callable=python_task, dag=dag)
bash_task = BashOperator(task_id="bash_task", bash_command="echo 'hello from bash'", dag=dag)
end = EmptyOperator(task_id="end", dag=dag)

start >> [py_task, bash_task] >> end
