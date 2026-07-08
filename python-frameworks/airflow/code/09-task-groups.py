"""Task groups — group tasks visually in the UI."""
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup

dag = DAG(
    "09_task_groups",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)

start = EmptyOperator(task_id="start", dag=dag)

with TaskGroup("data_pipeline", dag=dag) as data_group:
    extract = EmptyOperator(task_id="extract", dag=dag)
    transform = EmptyOperator(task_id="transform", dag=dag)
    load = EmptyOperator(task_id="load", dag=dag)
    extract >> transform >> load

with TaskGroup("ml_pipeline", dag=dag) as ml_group:
    train = EmptyOperator(task_id="train", dag=dag)
    evaluate = EmptyOperator(task_id="evaluate", dag=dag)
    train >> evaluate

end = EmptyOperator(task_id="end", dag=dag)

start >> data_group >> ml_group >> end
