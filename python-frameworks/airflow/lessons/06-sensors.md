# Sensors

Sensors are a special kind of operator that waits for a condition to be met. They keep polling or listening until the external event happens, then succeed and let downstream tasks proceed.

## Key Concepts
- **FileSensor** — waits for a file or directory to appear at a given path
- **TimeDeltaSensor** — waits until a specified `timedelta` after the DAG Run's `logical_date`
- **Poke vs Reschedule** — `mode="poke"` (default) keeps the task slot occupied and polls every `poke_interval` seconds; `mode="reschedule"` frees the slot between pokes, which is more resource-efficient for long waits
- **Timeout** — `timeout` (in seconds) raises `AirflowSensorTimeout` if the condition isn't met within the limit; combined with `soft_fail=True` it skips the task instead of failing it

## Code Example

References `../code/06-sensors.py`.

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.time_delta import TimeDeltaSensor


def _process_file() -> None:
    print("Processing file ...")


with DAG(
    dag_id="sensor_examples",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
):
    wait_for_data_file = FileSensor(
        task_id="wait_for_data_file",
        filepath="/tmp/incoming/data.csv",
        poke_interval=30,    # check every 30 seconds
        timeout=600,          # give up after 10 minutes
        mode="reschedule",    # free the worker slot between pokes
    )

    wait_for_offset = TimeDeltaSensor(
        task_id="wait_for_offset",
        delta=timedelta(hours=1),  # run 1 hour after logical_date
    )

    process = PythonOperator(
        task_id="process",
        python_callable=_process_file,
    )

    wait_for_data_file >> process
    wait_for_offset >> process
```

`FileSensor` blocks `process` until the file exists. Using `mode="reschedule"` avoids holding a worker slot during the wait — recommended for any sensor with a long or unpredictable wait time.

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/06-sensors.py /tmp/airflow_test/dags/
airflow dags list
# Create the file the sensor is waiting for (or the sensor will time out)
touch /tmp/incoming/data.csv
airflow dags test sensor_examples 2024-01-01
```

## Key Takeaways
- Sensors poll a condition; they succeed when it is met and fail when `timeout` expires
- Use `mode="reschedule"` for long-running sensors to avoid tying up worker slots
- Always set a `timeout` — an infinite sensor will block a pipeline forever
- `soft_fail=True` turns a timeout into a skip, which is useful when the file is optional
