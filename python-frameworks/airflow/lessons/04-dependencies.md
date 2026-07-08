# Dependencies

Dependencies define the order in which tasks execute. Airflow provides a clean, readable syntax to wire tasks together, ensuring that the graph remains acyclic.

## Key Concepts
- **Bit-shift operators** — `>>` (downstream) and `<<` (upstream) are the idiomatic way to set dependencies; `a >> b` means `a` runs before `b`
- **set_upstream / set_downstream** — explicit methods that work as alternatives: `b.set_upstream(a)` is equivalent to `a >> b`
- **chain patterns** — linear chains (`a >> b >> c`), fan-out (`a >> [b, c]`), fan-in (`[a, b] >> c`), and mixed topologies
- **cross-DAG dependencies** — `ExternalTaskSensor` or `ExternalPythonOperator` for dependencies across DAGs (advanced)

## Code Example

References `../code/04-dependencies.py`.

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


def _task_a() -> None:
    print("Task A")


def _task_b() -> None:
    print("Task B")


def _task_c() -> None:
    print("Task C")


def _task_d() -> None:
    print("Task D")


with DAG(
    dag_id="dependency_patterns",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
):
    start = EmptyOperator(task_id="start")

    task_a = PythonOperator(task_id="task_a", python_callable=_task_a)
    task_b = PythonOperator(task_id="task_b", python_callable=_task_b)
    task_c = PythonOperator(task_id="task_c", python_callable=_task_c)
    task_d = PythonOperator(task_id="task_d", python_callable=_task_d)

    end = EmptyOperator(task_id="end")

    # Linear chain
    start >> task_a

    # Fan-out: task_a triggers both task_b and task_c
    task_a >> [task_b, task_c]

    # Fan-in: both task_b and task_c must finish before task_d
    [task_b, task_c] >> task_d

    # Finish
    task_d >> end

    # Equivalent using set_upstream / set_downstream:
    # end.set_upstream(task_d)
```

The bit-shift operators are concise and read naturally left-to-right. `a >> [b, c]` means `b` and `c` run in parallel after `a` succeeds. Using `task_a.set_downstream(task_b)` works identically but is less common.

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/04-dependencies.py /tmp/airflow_test/dags/
airflow dags list
airflow dags test dependency_patterns 2024-01-01
```

## Key Takeaways
- `>>` and `<<` are the preferred, Pythonic way to declare task dependencies
- Lists create fan-out/fan-in: `a >> [b, c]` makes `b` and `c` parallel downstream of `a`
- Dependencies are always one-directional; cycles are rejected by the scheduler
- Use `chain()` from `airflow.models.baseoperator` for long linear pipelines
