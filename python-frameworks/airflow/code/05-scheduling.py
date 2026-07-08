"""Scheduling — cron expressions, timedelta, data intervals."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator

dag = DAG(
    "05_scheduling",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=30),
)

t1 = EmptyOperator(task_id="daily_task", dag=dag)

# Common schedules:
# @daily       — run once per day
# @hourly     — run once per hour
# @weekly     — run once per week
# @monthly    — run once per month
# @yearly     — run once per year
# 0 9 * * 1  — every Monday at 9 AM
# */15 * * * * — every 15 minutes
