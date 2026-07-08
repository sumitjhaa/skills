# Lesson 11.09: Continuous Training

## Learning Objectives
- Understand continuous training pipelines
- Implement automated retraining triggers
- Apply model freshness and data drift detection

## Continuous Training Pipeline

### Architecture
```
Data source → Trigger → Training → Evaluation → Deploy → Monitor
```

### Triggers
- Schedule-based (daily, weekly)
- Performance-based (accuracy drops)
- Data-based (new data available, distribution shift)
- Manual (developer-initiated)

## Retraining Strategies

| Strategy | Frequency | Data | Cost | When to Use |
|----------|-----------|------|------|-------------|
| Scheduled | Daily/weekly | Fixed window | Medium | Stable data |
| Triggered | On drift | Recent data | Low | Changing data |
| Online | Every sample | Streaming | High | Real-time needs |
| Rolling window | Continuous | Sliding window | Medium | Most common |

## Code: Continuous Training

```python
import time
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

class ContinuousTrainer:
    def __init__(self, model_class, data_source, config):
        self.model_class = model_class
        self.data_source = data_source
        self.config = config
        self.current_model = None
        self.last_trained = None

    def should_retrain(self):
        if self.last_trained is None:
            return True
        
        # Check schedule
        elapsed = datetime.now() - self.last_trained
        if elapsed > timedelta(hours=self.config.retrain_interval_hours):
            return True
        
        # Check data freshness
        latest_data_time = self.data_source.get_latest_timestamp()
        if latest_data_time > self.last_trained:
            return True
        
        # Check model performance
        current_accuracy = self.evaluate_current()
        if current_accuracy < self.config.min_accuracy:
            return True
        
        return False

    def train_new_model(self):
        logger.info("Starting model retraining")
        
        data = self.data_source.load_training_data(
            lookback_days=self.config.training_window_days
        )
        X_train, y_train, X_val, y_val = self.split_data(data)
        
        model = self.model_class(self.config.hyperparameters)
        model.fit(X_train, y_train)
        
        metrics = model.evaluate(X_val, y_val)
        logger.info(f"New model metrics: {metrics}")
        
        if self.should_deploy(metrics):
            self.current_model = model
            self.last_trained = datetime.now()
            self.save_model(model)
            logger.info("Model deployed to production")
        
        return model, metrics

    def should_deploy(self, metrics):
        if self.current_model is None:
            return True
        
        current_metrics = self.current_model.evaluate_on_validation()
        improvement = metrics[self.config.primary_metric] - \
                     current_metrics[self.config.primary_metric]
        
        return improvement > self.config.min_improvement

    def evaluate_current(self):
        if self.current_model is None:
            return 0.0
        return self.current_model.evaluate_on_production()

    def run_loop(self):
        while True:
            try:
                if self.should_retrain():
                    self.train_new_model()
            except Exception as e:
                logger.error(f"Training failed: {e}")
            time.sleep(self.config.check_interval_seconds)
```

## Data Drift Detection

```python
import numpy as np
from scipy.stats import ks_2samp, wasserstein_distance

class DataDriftDetector:
    def __init__(self, reference_data, threshold=0.05):
        self.reference = reference_data
        self.threshold = threshold

    def detect_drift(self, current_data):
        drifts = {}
        for column in self.reference.columns:
            stat, p_value = ks_2samp(
                self.reference[column], 
                current_data[column]
            )
            drifts[column] = {
                "statistic": stat,
                "p_value": p_value,
                "drifted": p_value < self.threshold,
                "wasserstein_distance": wasserstein_distance(
                    self.reference[column], 
                    current_data[column]
                ),
            }
        return drifts

    def trigger_if_drifted(self, current_data):
        drifts = self.detect_drift(current_data)
        num_drifted = sum(1 for d in drifts.values() if d["drifted"])
        drift_ratio = num_drifted / len(drifts)
        
        if drift_ratio > 0.3:
            logger.warning(f"Significant drift detected: {drift_ratio:.0%} of features drifted")
            return True
        return False
```

## CI/CD Pipeline Integration

```yaml
# .github/workflows/continuous-training.yml
name: Continuous Training
on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM
  workflow_dispatch:       # Manual trigger

jobs:
  train:
    runs-on: gpu-runner
    steps:
      - uses: actions/checkout@v3
      - name: Train model
        run: python train.py
      - name: Evaluate
        run: python evaluate.py
      - name: Deploy
        if: ${{ success() }}
        run: python deploy.py
      - name: Notify
        if: ${{ failure() }}
        run: python notify_slack.py
```

## Best Practices
- **Shadow mode**: Deploy new model alongside production but don't serve
- **Gradual rollout**: Increase traffic to new model slowly (10% → 50% → 100%)
- **Rollback plan**: Keep previous model available for instant recovery
- **Metrics comparison**: Track both technical (accuracy) and business (revenue) metrics
- **Data pipeline health**: Monitor upstream data quality, not just model

## References
- Baylor, Breck, et al., "TFX: A TensorFlow-Based Production-Scale Machine Learning Platform", KDD 2017
- Breck, Cai, et al., "The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction", 2017
- Hapke, Nelson, "Building Machine Learning Pipelines", O'Reilly 2020
- Sculley, Holt, et al., "Hidden Technical Debt in Machine Learning Systems", NeurIPS 2015
