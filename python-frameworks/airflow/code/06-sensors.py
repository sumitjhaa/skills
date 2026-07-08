"""Sensors — wait for file, time delta, or external condition."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.providers.standard.sensors.time_delta import TimeDeltaSensor
from airflow.providers.standard.operators.empty import EmptyOperator

dag = DAG(
    "06_sensors",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    default_args={"owner": "airflow"},
)

start = EmptyOperator(task_id="start", dag=dag)

wait_for_file = FileSensor(
    task_id="wait_for_file",
    filepath="/tmp/airflow_trigger.txt",
    poke_interval=5,
    timeout=60,
    dag=dag,
)

wait_delta = TimeDeltaSensor(
    task_id="wait_5s",
    delta=timedelta(seconds=5),
    dag=dag,
)

done = EmptyOperator(task_id="done", dag=dag)

start >> wait_for_file >> wait_delta >> done
