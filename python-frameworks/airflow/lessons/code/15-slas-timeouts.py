from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def _sla_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    print(f"SLA missed on DAG {dag.dag_id}")
    for sla in slas:
        print(f"Task {sla.task_id} expected by {sla.end_date}")


def _slow_task() -> None:
    import time
    time.sleep(20)


with DAG(
    dag_id="sla_timeout_demo",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    dagrun_timeout=timedelta(minutes=30),
    sla_miss_callback=_sla_callback,
):
    critical = PythonOperator(
        task_id="critical_etl",
        python_callable=_slow_task,
        execution_timeout=timedelta(minutes=5),
        sla=timedelta(minutes=2),
    )
