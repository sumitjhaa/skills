"""Tasks — dependencies, bit-shift operators, upstream/downstream."""
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator

dag = DAG(
    "03_tasks",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)

t1 = EmptyOperator(task_id="t1", dag=dag)
t2 = EmptyOperator(task_id="t2", dag=dag)
t3 = EmptyOperator(task_id="t3", dag=dag)
t4 = EmptyOperator(task_id="t4", dag=dag)
t5 = EmptyOperator(task_id="t5", dag=dag)

t1 >> [t2, t3] >> t4 >> t5
# Equivalent: t1.set_downstream([t2, t3])
#             t4.set_upstream([t2, t3])
#             t4.set_downstream(t5)
