# Custom Operators

When the built-in operators don't fit your use case, you can create a custom operator by subclassing `BaseOperator` and implementing the `execute()` method. Custom operators encapsulate reusable business logic and keep DAG files concise.

## Key Concepts
- **`BaseOperator`** — the parent class all operators inherit from; provides `task_id`, `retries`, `pool`, and more
- **`execute(context)`** — the single method you must override; contains the actual work
- **`__init__`** — define custom constructor parameters and call `super().__init__()` with Airflow-standard args
- **Return values** — `execute()` can return a value that is stored in XComs automatically
- **Templates** — use `template_fields` to let users pass Jinja-templated strings

## Code Example

References `../code/12-custom-operator.py`.

```python
from __future__ import annotations

from typing import Any

import requests
from airflow.models import BaseOperator
from airflow.utils.context import Context


class ApiFetchOperator(BaseOperator):
    """Fetches data from a REST API and pushes the response via XCom."""

    def __init__(self, endpoint: str, method: str = "GET", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.endpoint = endpoint
        self.method = method

    def execute(self, context: Context) -> dict:
        resp = requests.request(self.method, self.endpoint, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        self.log.info("Fetched %d records from %s", len(data), self.endpoint)
        return data
```

Use it in a DAG like any built-in operator:

```python
fetch_task = ApiFetchOperator(
    task_id="fetch_users",
    endpoint="https://api.example.com/users",
    dag=dag,
)
```

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/12-custom-operator.py /tmp/airflow_test/dags/
airflow dags test custom_operator_demo 2024-01-01
```

## Key Takeaways
- Override `execute(self, context)` — that is the only required method
- Accept `**kwargs` in `__init__` and forward them to `super().__init__()` so Airflow can inject task-level params like `retries` and `pool`
- The return value of `execute()` is automatically pushed to XCom under the key `return_value`
- Use `self.log` for structured logging inside the operator
- Package custom operators as a Python package and install it in the Airflow environment for reuse across DAGs
