# Lesson 11.03: Feature Engineering Pipeline

## Learning Objectives
- Understand feature engineering for ML pipelines
- Implement feature stores (Feast, Tecton)
- Apply feature computation, validation, and serving

## Feature Engineering Challenges

- **Consistency**: Train and serve features must match
- **Reproducibility**: Features must be computable at inference
- **Scale**: Billions of feature values across millions of entities

## Feature Store

### Architecture
```
Raw data → Feature computation → Feature store (offline + online)
                                              ↓
                              Training (offline)  Serving (online)
```

### Offline Store
- Historical feature values for training
- Stored in Parquet/Delta Lake
- Low latency queries not required

### Online Store
- Latest feature values for inference
- Stored in Redis/DynamoDB
- Millisecond latency

## Feast

### Feature Definition
```python
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64

customer = Entity(name="customer_id", join_keys=["customer_id"])

customer_stats_source = FileSource(
    path="s3://bucket/customer_stats.parquet",
    timestamp_field="event_timestamp",
)

customer_stats = FeatureView(
    name="customer_stats",
    entities=[customer],
    ttl=timedelta(days=1),
    schema=[
        Field(name="total_purchases", dtype=Int64),
        Field(name="avg_order_value", dtype=Float32),
        Field(name="days_since_last_purchase", dtype=Int64),
    ],
    source=customer_stats_source,
)
```

## Feature Computation

### Batch Features
```python
import pandas as pd
from datetime import datetime, timedelta

def compute_customer_features(transactions: pd.DataFrame):
    """Compute features for each customer"""
    now = datetime.now()
    features = transactions.groupby("customer_id").agg({
        "amount": ["sum", "mean", "count"],
        "transaction_date": "max",
    })
    features.columns = ["total_amount", "avg_amount", "num_transactions", "last_transaction"]
    features["days_since_last"] = (now - features["last_transaction"]).dt.days
    return features.reset_index()
```

### Streaming Features
```python
from kafka import KafkaConsumer
import json

def process_streaming_features():
    consumer = KafkaConsumer("user_events")
    for message in consumer:
        event = json.loads(message.value)
        feature_value = compute_running_mean(event["user_id"], event["value"])
        update_feature_store(event["user_id"], "running_mean", feature_value)
```

## Code: Feature Pipeline

```python
import pandas as pd
from datetime import datetime
from typing import Dict, List

class FeaturePipeline:
    def __init__(self, feature_store):
        self.feature_store = feature_store

    def compute_features(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        features = pd.DataFrame()
        features["customer_id"] = raw_data["customer_id"]
        features["total_purchases"] = raw_data.groupby("customer_id")["amount"].transform("count")
        features["avg_order_value"] = raw_data.groupby("customer_id")["amount"].transform("mean")
        features["days_since_last"] = (
            datetime.now() - 
            raw_data.groupby("customer_id")["transaction_date"].transform("max")
        ).dt.days
        return features

    def validate_features(self, features: pd.DataFrame) -> bool:
        checks = [
            features["total_purchases"].min() >= 0,
            features["avg_order_value"].min() >= 0,
            features["days_since_last"].min() >= 0,
            not features.isnull().any().any(),
        ]
        return all(checks)

    def write_to_offline(self, features: pd.DataFrame):
        self.feature_store.write_offline(features, 
            start_date=datetime.now() - timedelta(days=7),
            end_date=datetime.now()
        )

    def write_to_online(self, latest_features: pd.DataFrame):
        for _, row in latest_features.iterrows():
            self.feature_store.set_online(
                entity_id=row["customer_id"],
                features=row.to_dict()
            )

    def get_training_features(self, entity_ids: List[str], 
                              start_date: datetime, end_date: datetime) -> pd.DataFrame:
        return self.feature_store.get_historical_features(
            entity_ids=entity_ids,
            start_date=start_date,
            end_date=end_date,
        )

    def get_serving_features(self, entity_ids: List[str]) -> Dict:
        return self.feature_store.get_online_features(entity_ids=entity_ids)
```

## Feature Validation

| Check | Description | Example |
|-------|-------------|---------|
| Range | Values within bounds | age ∈ [0, 120] |
| Type | Correct data type | count is integer |
| Distribution | No distribution shift | KS test p > 0.05 |
| Missingness | Acceptable null rate | < 5% missing |
| Freshness | Features not stale | updated < 1 hour ago |

## Tools Comparison

| Tool | Offline | Online | Streaming | Open Source |
|------|---------|--------|-----------|-------------|
| Feast | Yes | Yes | Limited | Yes |
| Tecton | Yes | Yes | Yes | No |
| SageMaker | Yes | Yes | No | No |
| Hopsworks | Yes | Yes | Yes | Yes |

## References
- Feast documentation: https://docs.feast.dev/
- Tecton: https://www.tecton.ai/
- Zinkevich, "Rules of Machine Learning: Best Practices for ML Engineering", 2017
- Baylor, Breck, et al., "TFX: A TensorFlow-Based Production-Scale Machine Learning Platform", KDD 2017
