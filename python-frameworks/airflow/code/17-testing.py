"""Testing DAGs — unit test a DAG with pytest patterns."""
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator


def process(**kwargs):
    value = kwargs.get("value", 0)
    result = value * 2
    print(f"Processed: {result}")
    return result


dag = DAG(
    "17_testing",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)

start = EmptyOperator(task_id="start", dag=dag)
process = PythonOperator(
    task_id="process", python_callable=process, op_kwargs={"value": 21}, dag=dag
)
end = EmptyOperator(task_id="end", dag=dag)

start >> process >> end

# Testing pattern:
# from airflow.models import DagBag
# dagbag = DagBag(dag_folder="dags/", include_examples=False)
# dag = dagbag.get_dag("17_testing")
# assert len(dag.tasks) == 3
