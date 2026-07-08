# 11.06 Monitoring & Observability

## Objective
Detect drift, data quality issues, and performance degradation with **Evidently** and **Prometheus**.

## Evidently
- Open-source ML monitoring.
- Reports: Data Drift, Target Drift, Data Quality, Model Performance.
- Column-level drift (PSI, Jensen-Shannon, Wasserstein).

```python
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=ref, current_data=cur)
report.save_html("drift_report.html")
```

## Prometheus + Grafana
- Time-series metrics collection (latency, throughput, error rate).
- ML-specific custom metrics: prediction mean, confidence, drift score.

```python
from prometheus_client import Histogram, Gauge, start_http_server

prediction_latency = Histogram("prediction_latency_seconds", "Inference time")
prediction_count = Gauge("prediction_count", "Total predictions")
```

## Key Metrics to Monitor
1. **Data Drift** — distribution change in features
2. **Target Drift** — distribution change in labels
3. **Prediction Drift** — output distribution change
4. **Model Performance** — accuracy, precision, recall (when ground truth arrives)
5. **System Metrics** — latency, throughput, memory, GPU utilization

## Alerting Rules
```yaml
groups:
  - name: ml_alerts
    rules:
      - alert: HighDataDrift
        expr: drift_score > 0.3
        for: 1h
```

## Best Practices
1. Set baseline reference window (training data or first N production days).
2. Monitor both per-feature and aggregate drift.
3. Log all prediction inputs/outputs for offline analysis.
4. Trigger retraining pipeline when drift exceeds threshold.
