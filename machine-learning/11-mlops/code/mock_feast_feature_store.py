"""
Mock Feast Feature Store — demonstrates feature engineering at scale
with a local in-memory feature store, point-in-time joins, and online serving.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class FeatureView:
    name: str
    entities: list[str]
    features: list[str]
    ttl: timedelta = timedelta(days=7)


class MockFeatureStore:
    """Minimal Feast-like feature store with offline + online access."""

    def __init__(self):
        self._views: dict[str, FeatureView] = {}
        self._online_store: dict[str, dict] = {}  # entity_key -> {feature: value}

    def apply(self, feature_view: FeatureView):
        self._views[feature_view.name] = feature_view
        print(f"Applied feature view: {feature_view.name}")

    def _entity_key(self, entity_row: dict) -> str:
        return "_".join(str(v) for v in sorted(entity_row.items()))

    def ingest_online(self, entity_row: dict, features: dict):
        key = self._entity_key(entity_row)
        self._online_store[key] = features

    def get_online_features(self, features: list[str], entity_rows: list[dict]) -> list[dict]:
        results = []
        for row in entity_rows:
            key = self._entity_key(row)
            stored = self._online_store.get(key, {})
            result = {f.split(":")[-1]: stored.get(f.split(":")[-1]) for f in features}
            results.append(result)
        return results

    def get_historical_features(self, entity_df: list[dict], features: list[str]) -> list[dict]:
        """Simulate point-in-time join (mock: just return recent values)."""
        return self.get_online_features(features, entity_df)


if __name__ == "__main__":
    fs = MockFeatureStore()

    fv = FeatureView(
        name="driver_stats",
        entities=["driver_id"],
        features=["avg_daily_trips", "avg_rating", "lifetime_trips"],
    )
    fs.apply(fv)

    drivers = [
        {"driver_id": 101},
        {"driver_id": 102},
        {"driver_id": 103},
    ]

    features_data = [
        {"avg_daily_trips": 12.5, "avg_rating": 4.8, "lifetime_trips": 3200},
        {"avg_daily_trips": 8.3, "avg_rating": 4.2, "lifetime_trips": 1500},
        {"avg_daily_trips": 15.1, "avg_rating": 4.9, "lifetime_trips": 8700},
    ]

    for driver, feat in zip(drivers, features_data):
        fs.ingest_online(driver, feat)

    request = [{"driver_id": 101}, {"driver_id": 103}]
    result = fs.get_online_features(
        features=["driver_stats:avg_daily_trips", "driver_stats:avg_rating"],
        entity_rows=request,
    )

    for r in result:
        print(f"Online features: avg_daily_trips={r['avg_daily_trips']}, avg_rating={r['avg_rating']}")

    print("\nFeature store ready for training & inference.")
