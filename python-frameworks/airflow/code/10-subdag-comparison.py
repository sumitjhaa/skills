"""SubDAGs (legacy) vs TaskGroups — comparison."""
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator

dag = DAG(
    "10_subdag_comparison",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)

start = EmptyOperator(task_id="start", dag=dag)

# Modern approach: TaskGroups (preferred over SubDAGs)
# from airflow.utils.task_group import TaskGroup
# with TaskGroup("data", dag=dag):
#     ...

end = EmptyOperator(task_id="end", dag=dag)
start >> end
