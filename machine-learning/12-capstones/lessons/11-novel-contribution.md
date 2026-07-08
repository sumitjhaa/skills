# Lesson 12.11: Open-Source a Novel Contribution

## Project Architecture

Design, implement, and open-source a novel ML method or system. This is the most open-ended capstone: the goal is to make a genuine contribution to the ML ecosystem.

```
Project Lifecycle
├── 1. Ideation
│    ├── Identify a gap / problem in existing ML tools or methods
│    ├── Read 10+ papers in the area (related work)
│    ├── Formulate a hypothesis: "Can we do X better by Y?"
│    └── Scope: achievable in 2-4 weeks
│
├── 2. Design
│    ├── Algorithm / system architecture
│    ├── Theoretical justification (why should this work?)
│    ├── Success metrics (quantitative + qualitative)
│    └── Minimal viable prototype scope
│
├── 3. Implementation
│    ├── Clean, well-documented code
│    ├── Unit tests for all components
│    ├── Reproducible experiment scripts
│    └── Integration with existing ecosystem (if relevant)
│
├── 4. Experimentation
│    ├── Baseline comparison (against standard methods)
│    ├── Ablation studies
│    ├── Hyperparameter sensitivity
│    └── Scaling properties
│
├── 5. Open Source Release
│    ├── GitHub repository with README, license, contributing guide
│    ├── PyPI package (if applicable)
│    ├── Colab notebook demo
│    ├── Documentation (API reference + tutorial)
│    └── Social media announcement
│
└── 6. Iteration
     ├── Gather community feedback
     ├── Fix issues and add features
     └── Write a blog post / paper
```

## Design Decisions

### Project ideas (choose one or propose your own)

**a) Efficient Finetuning Library for Small LMs**
- Implement LoRA, AdaLoRA, IA3, (IA)^3 adapters
- Unified API: `apply_lora(model, target_modules, rank)`
- Benchmark: accuracy vs. parameter count for each method
- Novelty: adapter combination strategies, dynamic rank allocation

**b) Gradient-Free Neural Architecture Search**
- Use evolutionary algorithms with weight inheritance
- Support CNN and transformer search spaces
- Novelty: Lamarckian inheritance, fitness prediction
- Benchmark: CIFAR-100, ImageNet-1K subset

**c) Self-Supervised Learning with Adaptive Objectives**
- Combine multiple SSL objectives (contrastive, masked, clustering)
- Learn to weight objectives per sample
- Novelty: meta-learning the SSL objective weights
- Benchmark: linear eval on ImageNet-100

**d) ML Pipeline Debugger / Visualizer**
- Wrap sklearn/numpy pipelines to track intermediate values
- Detect: data leakage, feature correlation drift, gradient issues
- Dashboard: interactive pipeline visualization
- Novelty: automated pipeline debugging suggestions

**e) Memory-Efficient Transformer Training**
- Implement gradient checkpointing, activation offloading, mixed-precision
- Novelty: adaptive checkpointing strategy based on memory budget
- Benchmark: train BERT-base on 8GB GPU

### Novelty criteria
- Not published in a prior paper (check arXiv / proceedings)
- Not available in existing open-source libraries
- Solves a real problem faced by practitioners
- Reproducible and well-evaluated

## Implementation Guide

1. **Brainstorm and select project idea** (with justification)
2. **Write a mini-proposal** (problem, approach, evaluation plan)
3. **Design the API / architecture**
4. **Implement core algorithm**
5. **Write unit tests** (cover edge cases)
6. **Implement baselines** (existing methods)
7. **Run experiments** (compare against baselines)
8. **Analyze results** (statistical tests, plots)
9. **Create GitHub repo** with README, license, examples
10. **Create Colab demo**
11. **Write a blog post** explaining the method
12. **Submit to open-source channels** (Reddit, Twitter, Hacker News)

## Key Insights

- Novelty does not need to be a new SOTA result. A well-engineered tool, a clever combination of existing ideas, or a systematic study of an under-explored setting is valuable.
- Good documentation and clean code matter more than algorithmic novelty for adoption.
- Open-source contributions build your portfolio and reputation.
- Negative results are still contributions if they answer an important question.
- The best projects come from scratching your own itch.
