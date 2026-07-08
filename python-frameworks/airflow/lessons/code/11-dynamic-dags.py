from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

CUSTOMERS = ["acme", "globex", "initech"]


def _process_customer(customer: str) -> None:
    print(f"Processing {customer}")


def build_dag(customer: str) -> DAG:
    with DAG(
        dag_id=f"process_{customer}",
        start_date=datetime(2024, 1, 1),
        schedule="@daily",
        catchup=False,
        description=f"Pipeline for customer {customer}",
    ) as dag:
        PythonOperator(
            task_id=f"process_{customer}",
            python_callable=_process_customer,
            op_kwargs={"customer": customer},
        )
    return dag


for customer in CUSTOMERS:
    globals()[f"dag_process_{customer}"] = build_dag(customer)
