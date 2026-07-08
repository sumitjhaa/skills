"""
Mock Airflow DAG — demonstrates pipeline orchestration concepts by
simulating a DAG with tasks, dependencies, retries, and scheduling.
"""

import time
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Task:
    task_id: str
    callable: Callable
    retries: int = 2
    deps: list[str] = field(default_factory=list)
    status: str = "pending"


class MockDAG:
    """A minimal Airflow-like DAG runner."""

    def __init__(self, dag_id: str, schedule: str = "@daily"):
        self.dag_id = dag_id
        self.schedule = schedule
        self.tasks: dict[str, Task] = {}

    def add_task(self, task: Task):
        self.tasks[task.task_id] = task

    def set_dependencies(self, upstream: str, downstream: str):
        self.tasks[downstream].deps.append(upstream)

    def _get_ready_tasks(self, completed: set[str]) -> list[Task]:
        ready = []
        for task in self.tasks.values():
            if task.status == "pending" and all(d in completed for d in task.deps):
                ready.append(task)
        return ready

    def run(self):
        print(f"--- Running DAG: {self.dag_id} (schedule={self.schedule}) ---")
        completed: set[str] = set()

        while len(completed) < len(self.tasks):
            ready = self._get_ready_tasks(completed)
            if not ready:
                raise RuntimeError("Deadlock detected in DAG")
            for task in ready:
                task.status = "running"
                for attempt in range(1, task.retries + 2):
                    try:
                        print(f"  [{task.task_id}] attempt {attempt}")
                        task.callable()
                        task.status = "success"
                        completed.add(task.task_id)
                        break
                    except Exception as e:
                        print(f"  [{task.task_id}] failed: {e}")
                        if attempt <= task.retries:
                            print(f"  [{task.task_id}] retrying...")
                            time.sleep(0.1)
                        else:
                            task.status = "failed"
                            raise
        print(f"--- DAG {self.dag_id} completed successfully ---")


def extract():
    print("    extract: pulling raw data from API")


def validate():
    print("    validate: checking data quality")


def train():
    print("    train: training model")


def evaluate():
    print("    evaluate: computing metrics")


def deploy():
    print("    deploy: pushing model to staging")


if __name__ == "__main__":
    dag = MockDAG(dag_id="ml_retraining_pipeline", schedule="@weekly")

    t_extract = Task(task_id="extract", callable=extract)
    t_validate = Task(task_id="validate", callable=validate)
    t_train = Task(task_id="train", callable=train)
    t_evaluate = Task(task_id="evaluate", callable=evaluate)
    t_deploy = Task(task_id="deploy", callable=deploy)

    for t in [t_extract, t_validate, t_train, t_evaluate, t_deploy]:
        dag.add_task(t)

    dag.set_dependencies("extract", "validate")
    dag.set_dependencies("validate", "train")
    dag.set_dependencies("train", "evaluate")
    dag.set_dependencies("evaluate", "deploy")

    dag.run()
