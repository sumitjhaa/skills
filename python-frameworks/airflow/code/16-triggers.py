"""Triggers & deferrable operators — async task execution."""
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

dag = DAG(
    "16_triggers",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)


def regular_task(**kwargs):
    print("Regular task completed")


t1 = PythonOperator(task_id="regular", python_callable=regular_task, dag=dag)

# Deferrable operators (Airflow 2.6+) use a trigger for async execution:
#   from airflow.triggers.temporal import DateTimeTrigger
#   from airflow.operators.trigger_dagrun import TriggerDagRunOperator
