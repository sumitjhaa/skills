"""Dependencies — linear, fan-out, fan-in, conditional-like branching."""
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator

dag = DAG(
    "04_dependencies",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)

a1 = EmptyOperator(task_id="a1", dag=dag)
a2 = EmptyOperator(task_id="a2", dag=dag)
a3 = EmptyOperator(task_id="a3", dag=dag)
b1 = EmptyOperator(task_id="b1", dag=dag)
b2 = EmptyOperator(task_id="b2", dag=dag)
b3 = EmptyOperator(task_id="b3", dag=dag)
c1 = EmptyOperator(task_id="c1", dag=dag)

a1 >> a2 >> a3
a1 >> b1 >> b2 >> b3
[a3, b3] >> c1
