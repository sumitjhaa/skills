"""Capstone — full data pipeline with all concepts."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from airflow.models.baseoperator import BaseOperator


class DataQualityOperator(BaseOperator):
    def __init__(self, data: list, min_count: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.min_count = min_count

    def execute(self, context):
        count = len(self.data)
        print(f"Data quality check: {count} records (min: {self.min_count})")
        assert count >= self.min_count, f"Only {count} records, need {self.min_count}"
        return count


dag = DAG(
    "20_capstone_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["capstone"],
    default_args={"retries": 1, "retry_delay": timedelta(minutes=2)},
)


def extract(**kwargs):
    data = [{"id": i, "value": f"item_{i}"} for i in range(10)]
    kwargs["ti"].xcom_push(key="raw_data", value=data)
    print(f"Extracted {len(data)} records")
    return data


def transform(**kwargs):
    ti = kwargs["ti"]
    data = ti.xcom_pull(key="raw_data", task_ids="extract")
    transformed = {item["id"]: item["value"].upper() for item in data}
    ti.xcom_push(key="transformed", value=transformed)
    print(f"Transformed {len(transformed)} items")


start = EmptyOperator(task_id="start", dag=dag)

with TaskGroup("etl", dag=dag) as etl:
    extract_task = PythonOperator(task_id="extract", python_callable=extract, dag=dag)
    transform_task = PythonOperator(task_id="transform", python_callable=transform, dag=dag)
    extract_task >> transform_task

quality = DataQualityOperator(task_id="quality_check", data=[1, 2, 3], min_count=3, dag=dag)
end = EmptyOperator(task_id="end", dag=dag)

start >> etl >> quality >> end
