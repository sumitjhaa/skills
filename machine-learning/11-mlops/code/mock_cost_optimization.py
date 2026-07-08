"""
Mock Cost Optimization — demonstrates cost tracking, spot instance simulation,
autoscaling logic, and storage lifecycle management for ML workloads.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Resource:
    name: str
    instance_type: str
    hourly_cost: float
    is_spot: bool = False
    hours_used: float = 0.0
    spot_savings: float = 0.0

    def cost(self) -> float:
        return self.hourly_cost * self.hours_used


@dataclass
class StorageTier:
    name: str
    cost_per_gb_month: float
    size_gb: float = 0.0

    def monthly_cost(self) -> float:
        return self.size_gb * self.cost_per_gb_month


class MockCostTracker:
    """Track and optimize ML infrastructure costs."""

    def __init__(self, project: str = "ml-project"):
        self.project = project
        self.resources: list[Resource] = []
        self.storage: list[StorageTier] = []
        self.tags: dict = {}

    def add_resource(self, resource: Resource):
        self.resources.append(resource)

    def add_storage(self, storage: StorageTier):
        self.storage.append(storage)

    def compute_total(self) -> dict:
        compute_cost = sum(r.cost() for r in self.resources)
        storage_cost = sum(s.monthly_cost() for s in self.storage)
        return {
            "compute": round(compute_cost, 2),
            "storage": round(storage_cost, 2),
            "total": round(compute_cost + storage_cost, 2),
        }

    def spot_savings_report(self) -> dict:
        spot_resources = [r for r in self.resources if r.is_spot]
        spot_cost = sum(r.cost() for r in spot_resources)
        on_demand_cost = sum(
            r.hourly_cost * r.hours_used * (1.0 / 0.35 if r.is_spot else 1.0)
            for r in self.resources
        )
        savings = on_demand_cost - spot_cost
        return {
            "spot_cost": round(spot_cost, 2),
            "equivalent_on_demand": round(on_demand_cost, 2),
            "savings": round(savings, 2),
            "savings_pct": round(savings / on_demand_cost * 100, 1) if on_demand_cost > 0 else 0,
        }

    def autoscale_decision(self, current_load: float, target_gpus: int = 4) -> dict:
        """Decide whether to scale up/down based on load."""
        if current_load > 0.8:
            desired = min(target_gpus * 2, 16)
            action = "scale_up"
        elif current_load < 0.2 and target_gpus > 1:
            desired = max(target_gpus // 2, 1)
            action = "scale_down"
        else:
            desired = target_gpus
            action = "no_change"

        return {
            "action": action,
            "current_gpus": target_gpus,
            "desired_gpus": desired,
            "current_load": current_load,
        }

    def lifecycle_recommendation(self, days_since_last_access: int) -> str:
        if days_since_last_access > 90:
            return "Archive to Glacier (70% savings)"
        elif days_since_last_access > 30:
            return "Move to Infrequent Access (40% savings)"
        else:
            return "Keep in Standard tier"


def build_typical_ml_infra() -> MockCostTracker:
    tracker = MockCostTracker(project="ml-training")

    # On-demand (critical serving)
    tracker.add_resource(Resource("serving-a100", "p4d.24xlarge", 32.77, hours_used=720))
    # Spot instances (training)
    tracker.add_resource(Resource("training-spot", "p4d.24xlarge", 9.83, is_spot=True, hours_used=300))
    tracker.add_resource(Resource("hpo-spot", "g4dn.xlarge", 0.14, is_spot=True, hours_used=200))

    # Dev notebook
    tracker.add_resource(Resource("dev-notebook", "ml.t3.medium", 0.05, hours_used=160))

    return tracker


if __name__ == "__main__":
    tracker = build_typical_ml_infra()

    print("=== Cost Report ===")
    costs = tracker.compute_total()
    print(f"  Compute: ${costs['compute']}")
    print(f"  Storage: ${costs['storage']}")
    print(f"  Total:   ${costs['total']}")

    print("\n=== Spot Savings ===")
    savings = tracker.spot_savings_report()
    print(f"  Spot cost:              ${savings['spot_cost']}")
    print(f"  On-demand equivalent:   ${savings['equivalent_on_demand']}")
    print(f"  Savings:                ${savings['savings']} ({savings['savings_pct']}%)")

    print("\n=== Autoscaling Decisions ===")
    for load in [0.15, 0.45, 0.92]:
        decision = tracker.autoscale_decision(load, target_gpus=4)
        print(f"  Load {load*100:3.0f}% -> {decision['action']:12s}  ({decision['current_gpus']}->{decision['desired_gpus']} GPUs)")

    print("\n=== Storage Lifecycle ===")
    for days in [5, 45, 180]:
        rec = tracker.lifecycle_recommendation(days)
        print(f"  {days:3d} days since access: {rec}")

    # Cost optimization with right-sizing
    print("\n=== Right-Sizing Check ===")
    gpu_utilization = np.random.uniform(15, 95, 10)
    avg_util = gpu_utilization.mean()
    if avg_util < 40:
        print(f"  Avg GPU util: {avg_util:.1f}% — consider smaller instance or spot")
    else:
        print(f"  Avg GPU util: {avg_util:.1f}% — good utilization")
