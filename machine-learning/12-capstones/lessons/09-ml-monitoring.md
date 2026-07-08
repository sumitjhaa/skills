# Lesson 12.09: ML Monitoring Platform

## Project Architecture

Build a full ML monitoring system that tracks model predictions, detects data drift, concept drift, and performance degradation, with alerting and a dashboard.

```
┌─────────────────────────────────────────────────────┐
│                    ML Model                          │
│  (serving predictions on incoming data)              │
└──────────────────────┬──────────────────────────────┘
                       │ predictions
                       ▼
┌─────────────────────────────────────────────────────┐
│                 Monitoring Agent                      │
│                                                      │
│  1. Prediction Logging                               │
│     ├── Input features + prediction + timestamp      │
│     ├── Model version + id                           │
│     └── Ground truth (when available)                │
│                                                      │
│  2. Drift Detection                                  │
│     ├── Data drift: KS-test, χ²-test, PSI            │
│     ├── Feature drift: per-feature distributions     │
│     ├── Prediction drift: label distribution shift   │
│     └── Concept drift: accuracy over time windows    │
│                                                      │
│  3. Performance Monitoring                           │
│     ├── Accuracy, Precision, Recall, F1 (sliding)    │
│     ├── Confusion matrix over time                   │
│     └── Latency / throughput                         │
│                                                      │
│  4. Alerting                                         │
│     ├── Threshold-based: drift > p-value < 0.05     │
│     ├── Trend-based: accuracy dropping for 7 days    │
│     └── Severity levels: INFO, WARN, CRITICAL        │
│                                                      │
│  5. Dashboard                                        │
│     ├── Time series of metrics                       │
│     ├── Drift heatmaps (feature × time)              │
│     └── Alert history                                │
└─────────────────────────────────────────────────────┘
```

## Design Decisions

### Data storage
- Use numpy memmap for time-series metric storage
- SQLite for metadata and alert history
- JSON for prediction logs (sampled, not all)

### Drift detection methods
- **PSI (Population Stability Index)**: `Σ (p_i - q_i) * ln(p_i / q_i)` — measures distribution shift
- **KS-test**: non-parametric test for continuous features
- **Chi-squared test**: for categorical features
- **Wasserstein distance**: earth mover's distance for continuous features

### Reference window
- Training data distribution as reference
- Sliding window (last N predictions) as current
- Configurable window sizes

### Concept drift
- Monitor accuracy over time (sliding window)
- Page-Hinkley test for detecting change points
- DDM (Drift Detection Method): track error rate and standard deviation

### Dashboard
- Terminal-based dashboard using `rich` library
- Or matplotlib-based static plots generated periodically
- Key metrics displayed with thresholds color-coded

### Alerting
- Rule-based alerts with configurable thresholds
- Alert deduplication (no repeated alerts within cooldown period)
- Alert severity levels based on deviation magnitude

## Implementation Guide

1. **Implement prediction logger** (store inputs, predictions, metadata)
2. **Implement reference statistics** (compute from training data)
3. **Implement PSI calculator** for data drift
4. **Implement KS-test** for continuous feature drift
5. **Implement chi-squared test** for categorical drift
6. **Implement concept drift detector** (Page-Hinkley, DDM)
7. **Implement performance tracker** (sliding window metrics)
8. **Implement alert engine** (thresholds, dedup, severity)
9. **Implement dashboard** (plots and tables)
10. **Simulate a production scenario** (drift injection + monitoring)
11. **Generate monitoring report**

## Key Insights

- Data drift ≠ concept drift: data drifts when P(X) changes, concept drifts when P(Y|X) changes
- Monitoring without ground truth can only detect data drift, not concept drift
- PSI is industry standard for monitoring score distribution shifts
- Statistical tests need multiple testing correction when monitoring many features
- Alert fatigue is real — tune thresholds carefully and use severity levels
