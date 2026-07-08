# Phase 11: MLOps & Engineering at Scale

> **Goal:** Production-grade ML pipelines — experiment tracking, orchestration, monitoring, governance, and cost-aware deployment.

| # | Lesson | Topics | Code |
|---|--------|--------|------|
| 11.01 | Experiment Tracking | MLflow, Weights & Biases | `mock_mlflow_tracking.py` |
| 11.02 | Data Versioning | DVC, LakeFS | `mock_dvc_pipeline.py` |
| 11.03 | Feature Engineering | Feast, feature stores | `mock_feast_feature_store.py` |
| 11.04 | Pipeline Orchestration | Airflow, Prefect | `mock_airflow_dag.py` |
| 11.05 | Model Serving | TorchServe, vLLM, Triton | `mock_model_serving.py` |
| 11.06 | Monitoring & Observability | Evidently, Prometheus | `mock_drift_detection.py` |
| 11.07 | Model Governance | Registry, versioning, audits | `mock_model_registry.py` |
| 11.08 | A/B Testing | Statistical inference, bandits | `mock_ab_testing.py` |
| 11.09 | Continuous Training | Retraining pipelines, triggers | `mock_continuous_training.py` |
| 11.10 | Infrastructure as Code | Terraform, Kubernetes | `mock_terraform_ml.py` |
| 11.11 | Distributed Training | DDP, FSDP, DeepSpeed | `mock_distributed_training.py` |
| 11.12 | GPU Optimization | CUDA graphs, memory, profiling | `mock_gpu_optimization.py` |
| 11.13 | Data Pipeline Optimization | Caching, partitioning, streaming | `mock_data_pipeline_opt.py` |
| 11.14 | Testing for ML | Data/ model/ infra tests | `mock_ml_testing.py` |
| 11.15 | Responsible AI | Fairness, interpretability, privacy | `mock_responsible_ai.py` |
| 11.16 | Cost Optimization | Spot instances, autoscaling | `mock_cost_optimization.py` |

---

## Quick Start

```bash
# Run any lesson's code
python code/01-mock_mlflow_tracking.py

# Read a lesson
cat lessons/01-experiment-tracking.md

# Practice exercises
code practice/phase11-exercises.md
```

**Dependencies:** `numpy`, `scipy`, `matplotlib`, `scikit-learn`

**Directory structure**

```
lessons/          — 16 markdown lesson files (01-*.md … 16-*.md)
code/             — 16 standalone Python scripts demonstrating each concept
practice/         — phase11-exercises.md (~10 exercises)
```
