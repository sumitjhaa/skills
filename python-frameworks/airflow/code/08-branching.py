"""Branching — run different paths based on condition."""
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator


def choose_branch(**kwargs):
    value = kwargs.get("value", "a")
    if value == "a":
        return "branch_a"
    return "branch_b"


def branch_a(**kwargs):
    print("Executing branch A")


def branch_b(**kwargs):
    print("Executing branch B")


dag = DAG(
    "08_branching",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)

start = EmptyOperator(task_id="start", dag=dag)
branch = BranchPythonOperator(
    task_id="branch", python_callable=choose_branch, op_kwargs={"value": "a"}, dag=dag
)
task_a = PythonOperator(task_id="branch_a", python_callable=branch_a, dag=dag)
task_b = PythonOperator(task_id="branch_b", python_callable=branch_b, dag=dag)
merge = EmptyOperator(task_id="merge", dag=dag, trigger_rule="none_failed")

start >> branch >> [task_a, task_b] >> merge
