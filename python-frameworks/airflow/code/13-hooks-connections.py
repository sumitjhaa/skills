"""Hooks & connections — database connections using hooks."""
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.hooks.base import BaseHook

dag = DAG(
    "13_hooks_connections",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)


def demo_connection(**kwargs):
    conn = BaseHook.get_connection("airflow_db")
    print(f"Connection: {conn.conn_id}")
    print(f"Host:       {conn.host}")
    print(f"Login:      {conn.login}")
    print(f"Port:       {conn.port}")
    print(f"Schema:     {conn.schema}")


t1 = PythonOperator(task_id="demo_conn", python_callable=demo_connection, dag=dag)
