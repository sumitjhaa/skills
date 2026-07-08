# Phase 12 — Capstone Projects

## 1. Phase Overview

| Field | Value |
|---|---|
| **Phase** | 12 — Capstone Projects |
| **Lessons** | 11 |
| **Core topics** | Autograd from scratch, transformer from scratch, diffusion model, Mamba from scratch, RLHF/DPO, RAG system, distributed training, AutoML system, ML monitoring, reproduce paper, novel contribution |

## 2. Prerequisites

- **ALL prior phases** — Each capstone integrates knowledge from multiple earlier phases:
  - [Phase 01](../01-linear-algebra/INDEX.md) (all linear algebra foundations)
  - [Phase 02](../02-calculus-optimization/INDEX.md) (gradients, optimization)
  - [Phase 03](../03-probability-statistics/INDEX.md) (MLE, Bayesian inference)
  - [Phase 04](../04-advanced-math/INDEX.md) (information theory, geometry)
  - [Phase 05](../05-classical-ml/INDEX.md) (evaluation, model selection)
  - [Phase 06](../06-deep-learning/INDEX.md) (backprop, transformers, training pipelines)
  - [Phase 07](../07-advanced-architectures/INDEX.md) (SSMs, diffusion, advanced architectures)
  - [Phase 08](../08-computer-vision/INDEX.md) (vision models)
  - [Phase 09](../09-nlp/INDEX.md) (LLMs, RAG, alignment)
  - [Phase 10](../10-reinforcement-learning/INDEX.md) (RLHF, policy gradients)
  - [Phase 11](../11-mlops/INDEX.md) (distributed training, monitoring, AutoML)

- **Python frameworks:** [`../../python-frameworks/pytorch/`](../../python-frameworks/pytorch/) (all capstones), [`../../python-frameworks/scikit-learn/`](../../python-frameworks/scikit-learn/) (evaluation baselines), [`../../python-frameworks/numpy-pandas/`](../../python-frameworks/numpy-pandas/) (data handling)

## 3. Lesson Table

| # | Title | What You'll Learn | Lesson | Code | Cross-References |
|---|---|---|---|---|---|
| 01 | Autograd from Scratch | Build a full reverse-mode autograd engine | [lesson](lessons/01-autograd-from-scratch.md) | [code](code/01_autograd.py) | Builds on: Phase 02 (backprop), Phase 06 (autograd framework) |
| 02 | Transformer from Scratch | Implement transformer encoder-decoder | [lesson](lessons/02-transformer-from-scratch.md) | [code](code/02_transformer.py) | Builds on: Phase 06 (attention, transformers), Phase 09 (LLMs) |
| 03 | Diffusion Model | DDPM/DDIM from scratch | [lesson](lessons/03-diffusion-model.md) | [code](code/03_diffusion.py) | Builds on: Phase 07 (diffusion models), Phase 04 (SDEs) |
| 04 | Mamba from Scratch | SSM-based language model | [lesson](lessons/04-mamba-from-scratch.md) | [code](code/04_mamba.py) | Builds on: Phase 07 (SSM variants), Phase 06 (sequence models) |
| 05 | RLHF / DPO | Preference optimization pipeline | [lesson](lessons/05-rlhf-dpo.md) | [code](code/05_rlhf_dpo.py) | Builds on: Phase 10 (RLHF), Phase 09 (alignment), Phase 06 (PPO training) |
| 06 | RAG System | Retrieval-augmented generation pipeline | [lesson](lessons/06-rag-system.md) | [code](code/06_rag.py) | Builds on: Phase 09 (RAG, embeddings), Phase 11 (pipeline orchestration) |
| 07 | Distributed Training | Multi-GPU training with FSDP/DeepSpeed | [lesson](lessons/07-distributed-training.md) | [code](code/07_distributed.py) | Builds on: Phase 11 (distributed training), Phase 06 (mixed precision) |
| 08 | AutoML System | Automated model search and tuning | [lesson](lessons/08-automl-system.md) | [code](code/08_automl.py) | Builds on: Phase 05 (AutoML, Bayesian opt), Phase 11 (experiment tracking) |
| 09 | ML Monitoring | Drift detection, alerting, observability | [lesson](lessons/09-ml-monitoring.md) | [code](code/09_monitoring.py) | Builds on: Phase 11 (monitoring), Phase 05 (anomaly detection) |
| 10 | Reproduce Paper | Reproduce a published ML paper | [lesson](lessons/10-reproduce-paper.md) | [code](code/10_reproduce_paper.py) | Builds on: Phase 07 (SOTA reproduction), all prior phases |
| 11 | Novel Contribution | Original research contribution | [lesson](lessons/11-novel-contribution.md) | [code](code/11_novel_contribution.py) | Builds on: ALL phases (full curriculum synthesis) |

## 4. Builds Toward

- These capstones are the **culmination** of the entire curriculum. They are not prerequisites for further phases but serve as portfolio-ready projects demonstrating mastery of the full ML stack.

## 5. Quick Start

```bash
python3 code/01_autograd.py
```
