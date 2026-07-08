"""Custom operators — subclass BaseOperator."""
from datetime import datetime
from airflow import DAG
from airflow.models.baseoperator import BaseOperator
from airflow.providers.standard.operators.python import PythonOperator


class MultiplyOperator(BaseOperator):
    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(**kwargs)
        self.x = x
        self.y = y

    def execute(self, context):
        result = self.x * self.y
        print(f"{self.x} × {self.y} = {result}")
        return result


dag = DAG(
    "12_custom_operator",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)

mult = MultiplyOperator(task_id="multiply", x=6, y=7, dag=dag)
