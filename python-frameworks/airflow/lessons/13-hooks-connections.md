# Hooks & Connections

Hooks are Airflow's interface to external systems — databases, APIs, cloud services. They leverage **Connections** (stored credentials) so your code never handles secrets directly. After you define a Connection in the UI or via a CLI/env-var, any hook can use it to authenticate.

## Key Concepts
- **`BaseHook`** — abstract base class; provides `get_connection(conn_id)` to retrieve a Connection object
- **Connection object** — holds `conn_type`, `host`, `port`, `login`, `password`, `extra` (JSON), and `schema`
- **Connection types** — `postgres`, `http`, `s3`, `gcp`, `mysql`, etc.; each has a corresponding hook class
- **`get_conn()`** — hook method that returns an underlying client (e.g., a `psycopg2` connection or `boto3` client)
- **Storing secrets** — use Airflow's Secrets Backends (Vault, AWS Secrets Manager, GCP Secret Manager) for production; never hard-code credentials

## Code Example

References `../code/13-hooks-connections.py`.

```python
from __future__ import annotations

from typing import Any

import requests
from airflow.hooks.base import BaseHook


def _fetch_from_api() -> None:
    conn = BaseHook.get_connection("my_api")
    headers = {"Authorization": f"Bearer {conn.password}"}
    resp = requests.get(
        f"https://{conn.host}/data",
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    print(resp.json())
```

Set up the connection via the UI (**Admin → Connections**) or the CLI:

```bash
airflow connections add my_api \
    --conn-type http \
    --conn-host api.example.com \
    --conn-password "your-bearer-token"
```

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/13-hooks-connections.py /tmp/airflow_test/dags/
airflow dags test hooks_demo 2024-01-01
```

## Key Takeaways
- Use `BaseHook.get_connection("conn_id")` to retrieve credentials; never embed secrets in DAG code
- The `Connection` object exposes `login`, `password`, `host`, `port`, `schema`, and `extra` fields
- For production, configure a Secrets Backend so connections are stored outside the Airflow metadata DB
- Hook classes (e.g. `PostgresHook`, `S3Hook`) wrap `BaseHook` and return a ready-to-use client from `get_conn()`
