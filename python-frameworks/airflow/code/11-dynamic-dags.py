"""Dynamic DAGs — generate DAGs programmatically."""
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


def make_print_fn(name):
    def print_fn(**kwargs):
        print(f"Processing {name}")
    return print_fn


for i in range(5):
    dag_id = f"11_dynamic_{i}"
    dag = DAG(dag_id, start_date=datetime(2024, 1, 1), schedule=None, catchup=False)
    task = PythonOperator(
        task_id=f"task_{i}",
        python_callable=make_print_fn(dag_id),
        dag=dag,
    )
    globals()[dag_id] = dag
