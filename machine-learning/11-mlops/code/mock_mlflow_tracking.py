"""
Mock MLflow Tracking — logs parameters, metrics, and artifacts to a local
MLflow-compatible experiment store.
"""

import json
import os
import uuid
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Run:
    run_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    params: dict = field(default_factory=dict)
    metrics: dict = field(default_factory=dict)
    artifacts: list = field(default_factory=list)
    start_time: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class MockMlflow:
    """A minimal MLflow Tracking client mock."""

    def __init__(self, experiment_name="default"):
        self.experiment_name = experiment_name
        self.runs: list[Run] = []
        self._active_run: Run | None = None

    def start_run(self):
        self._active_run = Run()
        return self._active_run.run_id

    def log_param(self, key, value):
        if self._active_run:
            self._active_run.params[key] = value

    def log_metric(self, key, value):
        if self._active_run:
            self._active_run.metrics[key] = value

    def log_artifact(self, path, content=""):
        if self._active_run:
            self._active_run.artifacts.append({"path": path, "content": content})

    def end_run(self):
        if self._active_run:
            self.runs.append(self._active_run)
            self._active_run = None

    def search_runs(self):
        return self.runs

    def get_best_run(self, metric_key="accuracy"):
        valid = [r for r in self.runs if metric_key in r.metrics]
        if not valid:
            return None
        return max(valid, key=lambda r: r.metrics[metric_key])


if __name__ == "__main__":
    mlflow = MockMlflow(experiment_name="iris_classifier")

    hyperparams = [
        {"lr": 0.01, "max_depth": 3, "seed": 42},
        {"lr": 0.05, "max_depth": 5, "seed": 123},
        {"lr": 0.001, "max_depth": 7, "seed": 7},
    ]

    for hp in hyperparams:
        run_id = mlflow.start_run()
        mlflow.log_param("learning_rate", hp["lr"])
        mlflow.log_param("max_depth", hp["max_depth"])
        mlflow.log_param("seed", hp["seed"])

        fake_accuracy = 0.85 + 0.1 * hp["lr"] + 0.02 * hp["max_depth"]
        mlflow.log_metric("accuracy", round(fake_accuracy, 4))
        mlflow.log_metric("f1_score", round(fake_accuracy * 0.96, 4))

        mlflow.log_artifact("confusion_matrix.png", "base64-fake-image-data")
        mlflow.end_run()

    best = mlflow.get_best_run("accuracy")
    assert best is not None
    print(f"Experiment : {mlflow.experiment_name}")
    print(f"Total runs : {len(mlflow.runs)}")
    print(f"Best run   : {best.run_id}")
    print(f"Best acc   : {best.metrics['accuracy']}")
    print(f"Best params: {best.params}")
    print("All runs saved to experiment store.")
