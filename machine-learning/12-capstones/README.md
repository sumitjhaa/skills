# Phase 12: Grand Capstone Projects

## Overview

| # | Project | Domain | Difficulty | Est. Lines |
|---|---------|--------|------------|------------|
| 12.01 | Autograd from scratch + Neural Net | Core ML | ★★★☆☆ | ~400 |
| 12.02 | Transformer from scratch (GPT-2 scale) | NLP | ★★★★☆ | ~600 |
| 12.03 | Diffusion model from scratch | Generative | ★★★★☆ | ~500 |
| 12.04 | Mamba from scratch + Transformer comparison | SSM | ★★★★★ | ~700 |
| 12.05 | RLHF / DPO from scratch | Alignment | ★★★★★ | ~600 |
| 12.06 | Full RAG system with evaluation | Retrieval | ★★★★☆ | ~500 |
| 12.07 | Distributed training with FSDP | Scaling | ★★★★★ | ~500 |
| 12.08 | AutoML system | Automation | ★★★★☆ | ~600 |
| 12.09 | ML monitoring platform | MLOps | ★★★★☆ | ~500 |
| 12.10 | Reproduce SOTA paper + improve | Research | ★★★★★ | ~700 |
| 12.11 | Open-source novel contribution | Research | ★★★★★ | ~800 |

## Structure

```
12-capstones/
├── README.md
├── lessons/
│   ├── 01-autograd-from-scratch.md
│   ├── 02-transformer-from-scratch.md
│   ├── 03-diffusion-model.md
│   ├── 04-mamba-from-scratch.md
│   ├── 05-rlhf-dpo.md
│   ├── 06-rag-system.md
│   ├── 07-distributed-training.md
│   ├── 08-automl-system.md
│   ├── 09-ml-monitoring.md
│   ├── 10-reproduce-paper.md
│   └── 11-novel-contribution.md
├── code/
│   ├── 01_autograd.py
│   ├── 02_transformer.py
│   ├── 03_diffusion.py
│   ├── 04_mamba.py
│   ├── 05_rlhf_dpo.py
│   ├── 06_rag.py
│   ├── 07_distributed.py
│   ├── 08_automl.py
│   ├── 09_monitoring.py
│   ├── 10_reproduce_paper.py
│   └── 11_novel_contribution.py
└── practice/
    └── phase12-exercises.md
```

## How to Run

Each code file is self-contained. Install dependencies:

```bash
pip install numpy scipy matplotlib scikit-learn
```

Then run any project:

```bash
python code/01_autograd.py
```

## Learning Objectives

- Build production-grade ML systems from scratch
- Understand core algorithmic innovations by reimplementing them
- Develop the ability to reproduce and improve on SOTA research
- Create a portfolio of substantial, demonstrable ML projects
