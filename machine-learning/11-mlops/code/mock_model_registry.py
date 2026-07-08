"""
Mock Model Registry — implements model versioning, stage transitions,
and governance checks similar to MLflow Model Registry.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class Stage(Enum):
    NONE = "None"
    STAGING = "Staging"
    PRODUCTION = "Production"
    ARCHIVED = "Archived"


@dataclass
class ModelVersion:
    version: int
    run_id: str
    stage: Stage = Stage.NONE
    metrics: dict = field(default_factory=dict)
    model_card: Optional[dict] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def transition_to(self, new_stage: Stage):
        self.stage = new_stage
        print(f"  Model v{self.version} → {new_stage.value}")


class MockModelRegistry:
    """Minimal model registry with governance checks."""

    def __init__(self):
        self._models: dict[str, list[ModelVersion]] = {}

    def create_registered_model(self, name: str):
        if name not in self._models:
            self._models[name] = []
            print(f"Registered model: {name}")

    def create_version(self, model_name: str, run_id: str, metrics: dict = None) -> ModelVersion:
        versions = self._models.get(model_name)
        if versions is None:
            raise ValueError(f"Model {model_name} not registered")
        v = ModelVersion(version=len(versions) + 1, run_id=run_id, metrics=metrics or {})
        versions.append(v)
        print(f"Created {model_name} v{v.version} (run={run_id[:8]}...)")
        return v

    def transition(self, model_name: str, version: int, stage: Stage):
        for v in self._models.get(model_name, []):
            if v.version == version:
                v.transition_to(stage)
                return
        raise ValueError(f"Version {version} not found")

    def get_latest_version(self, model_name: str, stage: Stage = Stage.PRODUCTION) -> Optional[ModelVersion]:
        versions = self._models.get(model_name, [])
        for v in reversed(versions):
            if v.stage == stage:
                return v
        return None

    def governance_check(self, model_name: str, version: int) -> bool:
        """Simulate automated governance gates."""
        versions = self._models.get(model_name, [])
        target = next((v for v in versions if v.version == version), None)
        if target is None:
            return False
        checks = []

        # Performance gate
        prod = self.get_latest_version(model_name, Stage.PRODUCTION)
        if prod and target.metrics:
            perf_ok = target.metrics.get("accuracy", 0) > prod.metrics.get("accuracy", 0)
            checks.append(("performance", perf_ok))
        else:
            checks.append(("performance", True))

        # Fairness gate (mock)
        fairness_ok = True
        checks.append(("fairness", fairness_ok))

        # Explainability gate (mock)
        explain_ok = target.model_card is not None
        checks.append(("explainability", explain_ok))

        for name, passed in checks:
            status = "PASS" if passed else "FAIL"
            print(f"    [{status}] {name} gate")
        return all(p for _, p in checks)


if __name__ == "__main__":
    registry = MockModelRegistry()
    registry.create_registered_model("FraudDetector")

    v1 = registry.create_version("FraudDetector", run_id="abc123def456", metrics={"accuracy": 0.92})
    v2 = registry.create_version("FraudDetector", run_id="def789ghi012", metrics={"accuracy": 0.95})
    v2.model_card = {"intended_use": "Fraud detection", "limitations": "May false-positive on new merchant types"}

    print("\n--- Governance Check v2 ---")
    passed = registry.governance_check("FraudDetector", 2)
    if passed:
        registry.transition("FraudDetector", 2, Stage.PRODUCTION)

    print(f"\nProduction version: {registry.get_latest_version('FraudDetector').version}")
