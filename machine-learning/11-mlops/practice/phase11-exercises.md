# Phase 11 Exercises — MLOps & Engineering at Scale

## 1. Experiment Tracking Integration
Set up MLflow (or use the mock from code/01) to track 5 runs of a scikit-learn model on the Iris dataset. Log accuracy, F1, all hyperparameters, and a confusion matrix plot artifact. Query the best run programmatically.

## 2. Data Versioning Pipeline
Create a DVC-like pipeline (or use code/02) with three stages: `ingest`, `preprocess`, `train`. Simulate a dataset change and show that `reproduce` detects the change and re-runs downstream stages. Add a fourth stage `evaluate` downstream of `train`.

## 3. Feature Store for Real-Time Inference
Using code/03, extend the MockFeatureStore to support feature transformations (e.g., normalize a feature on the fly during `get_online_features`). Add a `feature_service` concept that bundles multiple feature views.

## 4. Build a DAG with Conditional Branching
Using code/04, add a conditional branch: if validate passes → train; else → send alert (mock print). Add a third branch for a retraining schedule that checks drift before triggering.

## 5. Model A/B Testing Simulation
Using code/08, simulate an A/B test with 10,000 users split 50/50 between model A (control, 11% conversion) and model B (treatment, 13% conversion). Run a t-test and state whether B is significantly better at α=0.05. Implement a sequential test that stops early if significance is reached.

## 6. Continuous Training with Drift Detection
Combine code/06 and code/09: when drift_score > 0.25, trigger the continuous training pipeline. If the new model beats the current best, register and transition to staging. Log the trigger reason and model accuracy to history.

## 7. Distributed Training Scaling Analysis
Using code/11, run the MockTrainer with world_size = 1, 2, 4, 8. Plot (or print) the loss curves and memory savings per GPU. Discuss the trade-off between communication overhead and per-GPU memory savings.

## 8. GPU Optimization Profiling
Using code/12, compare training step time for 4 configurations:
- FP32, no optimizations
- FP32 + gradient checkpointing
- FP16 AMP
- FP16 AMP + checkpointing

Report the speedup of the best config over the worst.

## 9. Fairness Audit
Using code/15, train a classifier on a dataset with a sensitive attribute. Compute demographic parity and equal opportunity difference. Apply a reweighing technique to mitigate bias and re-measure. Show that fairness improved (perhaps at a small accuracy cost).

## 10. Cost Optimization Plan
Using code/16, analyze the infrastructure of a team running:
- 4 x p4d.24xlarge on-demand for training (100 hrs each / week)
- 2 x g5.xlarge spot for HPO (always on)
- 10 TB of S3 Standard data (accessed weekly)

Recommend an optimized setup with spot/reserved instances and storage lifecycle policies. Calculate the monthly savings.

## Bonus: CI/CD Pipeline for ML
Write a GitHub Actions workflow (`.github/workflows/ml-pipeline.yml`) that:
1. Runs data tests on PR
2. Trains a model on a small subset
3. Runs model tests (invariance, performance floor)
4. If tests pass and branch is `main`, registers the model (mock)

Save the workflow file in the repository.
