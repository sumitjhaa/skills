# Phase 11 — MLOps

## 1. Phase Overview

| Field | Value |
|---|---|
| **Phase** | 11 — MLOps |
| **Lessons** | 16 |
| **Core topics** | Experiment tracking, data versioning, feature engineering, pipeline orchestration, model serving, monitoring, model governance, A/B testing, continuous training, infrastructure as code, distributed training, GPU optimization, data pipeline optimization, testing for ML, responsible AI, cost optimization |

## 2. Prerequisites

- **Prior phases:** [Phase 05](../05-classical-ml/INDEX.md) (baseline models, evaluation), [Phase 06](../06-deep-learning/INDEX.md) (training pipelines, optimizers, mixed precision)
- **Python frameworks:** [`../../python-frameworks/airflow/`](../../python-frameworks/airflow/) (pipeline orchestration), [`../../python-frameworks/pytest-deep/`](../../python-frameworks/pytest-deep/) (ML testing), [`../../python-frameworks/celery/`](../../python-frameworks/celery/) (distributed tasks)

## 3. Lesson Table

| # | Title | What You'll Learn | Lesson | Code | Cross-References |
|---|---|---|---|---|---|
| 01 | Experiment Tracking | MLflow, W&B, metadata storage | [lesson](lessons/01-experiment-tracking.md) | [code](code/mock_mlflow_tracking.py) | Used in: Phase 05 (model selection) |
| 02 | Data Versioning | DVC, git-lfs, data lineage | [lesson](lessons/02-data-versioning.md) | [code](code/mock_dvc_pipeline.py) | Used in: Phase 03 (data pipelines) |
| 03 | Feature Engineering | Feast, Tecton, feature stores | [lesson](lessons/03-feature-engineering.md) | [code](code/mock_feast_feature_store.py) | Used in: Phase 05 (feature engineering) |
| 04 | Pipeline Orchestration | Airflow, Kubeflow, Dagster | [lesson](lessons/04-pipeline-orchestration.md) | [code](code/mock_airflow_dag.py) | Used in: Phase 06 (training pipeline) |
| 05 | Model Serving | TorchServe, Triton, FastAPI, serverless | [lesson](lessons/05-model-serving.md) | [code](code/mock_model_serving.py) | Used in: Phase 09 (LLM serving) |
| 06 | Monitoring | Drift detection, data quality, alerts | [lesson](lessons/06-monitoring.md) | [code](code/mock_drift_detection.py) | Used in: Phase 05 (anomaly detection) |
| 07 | Model Governance | Registry, audit, compliance, lineage | [lesson](lessons/07-model-governance.md) | [code](code/mock_model_registry.py) | Used in: Phase 09 (AI governance) |
| 08 | A/B Testing | Statistical tests, MAB, gradual rollout | [lesson](lessons/08-ab-testing.md) | [code](code/mock_ab_testing.py) | Used in: Phase 03 (hypothesis testing), Phase 05 (bandits) |
| 09 | Continuous Training | Retraining triggers, auto-RL, CI/CD | [lesson](lessons/09-continuous-training.md) | [code](code/mock_continuous_training.py) | Used in: Phase 06 (training pipeline) |
| 10 | Infrastructure as Code | Terraform, Docker, K8s, Helm | [lesson](lessons/10-infrastructure-as-code.md) | [code](code/mock_terraform_ml.py) | Used in: Phase 11 (deployment) |
| 11 | Distributed Training | FSDP, DeepSpeed, Horovod, Ray | [lesson](lessons/11-distributed-training.md) | [code](code/mock_distributed_training.py) | Used in: Phase 06 (distributed), Phase 12 |
| 12 | GPU Optimization | CUDA graphs, memory, kernel fusion | [lesson](lessons/12-gpu-optimization.md) | [code](code/mock_gpu_optimization.py) | Used in: Phase 06 (mixed precision) |
| 13 | Data Pipeline Optimization | Data loading, preprocessing at scale | [lesson](lessons/13-data-pipeline-optimization.md) | [code](code/mock_data_pipeline_opt.py) | Used in: Phase 08 (data loading) |
| 14 | Testing for ML | Data tests, model tests, CI for ML | [lesson](lessons/14-testing-for-ml.md) | [code](code/mock_ml_testing.py) | Used in: Phase 06 (testing) |
| 15 | Responsible AI | Fairness, bias, explainability, privacy | [lesson](lessons/15-responsible-ai.md) | [code](code/mock_responsible_ai.py) | Used in: Phase 09 (AI governance) |
| 16 | Cost Optimization | Spot instances, auto-scaling, budgeting | [lesson](lessons/16-cost-optimization.md) | [code](code/mock_cost_optimization.py) | Used in: Phase 12 (distributed training) |

## 4. Builds Toward

- **Phase 12** (distributed training capstone, ML monitoring capstone, AutoML system, all production-ready capstones)

## 5. Quick Start

```bash
python3 code/mock_airflow_dag.py
```
