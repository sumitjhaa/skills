"""
Mock Continuous Training — simulates an automated retraining pipeline
that checks for drift, retrains, evaluates, and registers a new model.
"""

import json
import os
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class ModelMetadata:
    version: int
    accuracy: float
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    trigger: str = ""


class MockContinuousTraining:
    """Automated retraining pipeline with drift-based triggers."""

    def __init__(self, model_dir: str | Path):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.best_accuracy: float = 0.0
        self.current_version: int = 0
        self.history: list[ModelMetadata] = []

    def check_drift(self, drift_score: float, threshold: float = 0.3) -> bool:
        """Drift check (mock Evidently)."""
        return drift_score > threshold

    def ingest_data(self) -> int:
        """Simulate ingesting new data rows."""
        return 5000  # pretend we got 5k new rows

    def train(self, data_rows: int) -> float:
        """Simulate training and return accuracy."""
        import numpy as np
        fake_acc = 0.85 + np.random.uniform(-0.03, 0.08)
        return round(float(fake_acc), 4)

    def evaluate(self, model_accuracy: float) -> bool:
        """Check if new model beats current best."""
        return model_accuracy > self.best_accuracy

    def register(self, accuracy: float, trigger: str):
        self.current_version += 1
        meta = ModelMetadata(
            version=self.current_version,
            accuracy=accuracy,
            trigger=trigger,
        )
        self.history.append(meta)
        if accuracy > self.best_accuracy:
            self.best_accuracy = accuracy

        manifest = {
            "version": meta.version,
            "accuracy": meta.accuracy,
            "trigger": meta.trigger,
            "timestamp": meta.timestamp,
        }
        with open(self.model_dir / f"model_v{meta.version}.json", "w") as f:
            json.dump(manifest, f, indent=2)
        print(f"  Registered model v{meta.version} (acc={accuracy}, trigger={trigger})")

    def run_pipeline(self, drift_score: Optional[float] = None, force: bool = False):
        print(f"\n--- Continuous Training Pipeline ({datetime.utcnow().isoformat()}) ---")

        trigger = "scheduled"

        if drift_score is not None and self.check_drift(drift_score):
            print(f"  Drift detected (score={drift_score:.2f}) — triggering retrain")
            trigger = "drift"
        elif force:
            print("  Manual force trigger")
            trigger = "manual"
        else:
            print("  No drift — running scheduled retrain anyway")

        data_rows = self.ingest_data()
        print(f"  Ingested {data_rows} new rows")

        accuracy = self.train(data_rows)
        print(f"  New model accuracy: {accuracy} (best: {self.best_accuracy})")

        if self.evaluate(accuracy):
            self.register(accuracy, trigger)
        else:
            print(f"  Model rejected — did not beat best ({self.best_accuracy})")

        print(f"  Current best: v{self.current_version} @ {self.best_accuracy}")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        pipeline = MockContinuousTraining(tmpdir)

        pipeline.run_pipeline()
        pipeline.run_pipeline(drift_score=0.45)  # drift triggers retrain
        pipeline.run_pipeline(force=True)

        print(f"\nFinal best accuracy: {pipeline.best_accuracy}")
        print(f"Total versions registered: {len(pipeline.history)}")
