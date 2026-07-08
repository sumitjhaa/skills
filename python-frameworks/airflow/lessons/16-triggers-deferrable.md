# Triggers & Deferrable Operators

Deferrable operators (Airflow 2.2+) free up worker slots while waiting for external events. Instead of a worker polling in a tight loop, a lightweight **Trigger** runs asynchronously and resumes the task when the condition is met. This dramatically reduces resource usage for long-running sensors.

## Key Concepts
- **Deferrable operator** — a task that suspends itself by raising `TriggerEvent` and defers to a trigger
- **Trigger** — an async class that runs in a dedicated event loop; must implement `run()` and yield `TriggerEvent`
- **`defer()` method** — called inside `execute()` to hand off control; accepts a trigger class and kwargs
- **Triggerer process** — a separate Airflow component that runs triggers; start with `airflow triggerer`
- **`mode="reschedule"`** — classic sensors can also be efficient, but triggers are the most lightweight option

## Code Example

References `../code/16-triggers-deferrable.py`.

```python
from __future__ import annotations

import asyncio
from typing import Any

from airflow.models import BaseOperator
from airflow.triggers.base import BaseTrigger, TriggerEvent
from airflow.utils.context import Context


class FileSensorTrigger(BaseTrigger):
    def __init__(self, filepath: str):
        super().__init__()
        self.filepath = filepath

    def serialize(self) -> tuple[str, dict[str, Any]]:
        return ("file_sensor_trigger", {"filepath": self.filepath})

    async def run(self):
        while True:
            try:
                with open(self.filepath) as f:
                    content = f.read()
                yield TriggerEvent({"content": content})
                return
            except FileNotFoundError:
                await asyncio.sleep(5)


class DeferrableFileSensor(BaseOperator):
    def __init__(self, filepath: str, **kwargs: Any):
        super().__init__(**kwargs)
        self.filepath = filepath

    def execute(self, context: Context) -> None:
        self.defer(
            trigger=FileSensorTrigger(filepath=self.filepath),
            method_name="resume",
        )

    def resume(self, context: Context, event: dict[str, Any] | None = None) -> None:
        if event:
            self.log.info("File found with content: %s", event["content"][:100])
```

Start the triggerer process alongside the scheduler:

```bash
airflow triggerer &
airflow scheduler &
```

## Running the DAG

```bash
export AIRFLOW_HOME=/tmp/airflow_test
airflow db migrate
cp ../code/16-triggers-deferrable.py /tmp/airflow_test/dags/
airflow dags test deferrable_demo 2024-01-01
```

## Key Takeaways
- Deferrable operators use a separate `Triggerer` process, not workers — run `airflow triggerer` alongside the scheduler
- Your trigger class must implement `run()` (async generator) and `serialize()` (for persistence across restarts)
- Call `self.defer(trigger=..., method_name="resume")` inside `execute()` to hand off
- The resume method receives the `TriggerEvent` payload and finishes execution
- Use deferrable operators for any task that spends most of its time waiting: file sensors, API pollers, cloud operation watchers
