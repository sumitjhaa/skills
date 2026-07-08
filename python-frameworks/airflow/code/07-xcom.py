"""XCom — share data between tasks."""
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


def push_value(**kwargs):
    ti = kwargs["ti"]
    ti.xcom_push(key="my_key", value="hello_xcom")
    return "return_value_also_stored"


def pull_value(**kwargs):
    ti = kwargs["ti"]
    pushed = ti.xcom_pull(key="my_key", task_ids="push_task")
    returned = ti.xcom_pull(task_ids="push_task")
    print(f"Pushed value: {pushed}")
    print(f"Return value: {returned}")


dag = DAG(
    "07_xcom",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)

push_task = PythonOperator(task_id="push_task", python_callable=push_value, dag=dag)
pull_task = PythonOperator(task_id="pull_task", python_callable=pull_value, dag=dag)

push_task >> pull_task
