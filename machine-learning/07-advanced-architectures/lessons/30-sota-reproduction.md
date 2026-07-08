# Lesson 07.30: SOTA Reproduction

## Learning Objectives
- Develop a systematic approach to reading and implementing ML papers
- Design reproduction experiments with proper baselines and ablations
- Handle common pitfalls: preprocessing, hyperparameters, hardware
- Build reproducible research code and documentation

## Theory
Reproducing state-of-the-art (SOTA) results is a critical skill. It validates understanding, builds implementation skills, and enables building on prior work.

### Reproduction Spectrum
| Level | Description | Effort | Value |
|-------|-------------|--------|-------|
| Read-only | Understand the paper conceptually | Low | Low |
| Conceptual reimplementation | Own code following paper description | High | High |
| Full reimplementation | Exact reproduction of reported results | Very high | Very high |
| Extension | Add/modify components, beat SOTA | Very high | Highest |

## Paper Reading Strategy

### Anatomy of a ML Paper
1. **Abstract**: What, how, results (1-2 sentences each)
2. **Introduction**: Motivation, gap, contribution
3. **Related work**: Positioning relative to prior work
4. **Method**: Core contribution — equations, architecture, algorithm
5. **Experiments**: Setup, baselines, ablations, results
6. **Conclusion**: Summary, limitations, future work
7. **Appendix**: Implementation details, hyperparameters, additional results

### Active Reading Questions
- What is the core contribution? (one sentence)
- What problem does it solve that prior work didn't?
- What's the key equation or algorithm?
- How is it evaluated? What metrics?
- What are the limitations not discussed?

## Implementation Strategy

### Step-by-Step
1. **Collect information**: Paper, supplementary, official code, unofficial codes
2. **Set up environment**: Dependencies, GPU, data storage
3. **Implement baseline**: Known working repro (often available in libraries)
4. **Modularize contribution**: Isolate the novel component
5. **Match training setup**: Batch size, LR schedule, augmentation, seeds
6. **Debug on small scale**: Overfit on 1-2 batches first
7. **Scale up**: Full dataset, distributed training
8. **Ablate**: Verify each component's contribution

### Code Organization
```
project/
  configs/         # YAML config files
  data/            # Dataset classes
  models/          # Model implementations
  losses/          # Custom loss functions
  trainers/        # Training loop
  utils/           # Metrics, visualization, logging
  run.py           # Entry point
  reproduce.sh     # Script to reproduce results
```

## Common Pitfalls

### Data Preprocessing
| Issue | Example | Impact |
|-------|---------|--------|
| Missing augmentation | RandomErasing not applied | 1-2% accuracy drop |
| Wrong normalization | Mean/std not matching training | Random performance |
| Data leakage | Augmentation after train/test split | Overestimated metric |
| Resolution mismatch | Paper uses 224, you use 256 | Architecture mismatch |

### Training Details
- **Learning rate**: Often paper reports base LR for specific batch size; scale with linear rule
- **Weight decay**: Critical for regularization; 1e-4 vs 1e-5 can change results by 1%+
- **Warmup**: 5-10% of total steps; missing warmup can prevent convergence
- **Label smoothing**: 0.1 default; missing it affects calibration
- **EMA**: 0.999 decay for model averaging; use separate copy

## Hyperparameter Transfer

### Linear Scaling Rule
$$lr_{\text{new}} = lr_{\text{base}} \times \frac{\text{batch\_size}_{\text{new}}}{\text{batch\_size}_{\text{base}}}$$

### Square Root Scaling (Adam)
$$lr_{\text{new}} = lr_{\text{base}} \times \sqrt{\frac{\text{batch\_size}_{\text{new}}}{\text{batch\_size}_{\text{base}}}}$$

### Rule of Thumb
- Double batch size → multiply LR by $1x-2x$
- Halve batch size → divide LR by $1x-2x$
- Adjust warmup steps proportionally to batch size change

## Code: Reproduction Checklist

```python
"""Reproduction checklist for ML paper"""
CHECKLIST = {
    "data": [
        "Download correct dataset version",
        "Apply same augmentations (size, crop, flip, color)",
        "Use correct normalization (mean, std)",
        "Split train/val/test same way as paper",
    ],
    "model": [
        "Verify architecture matches paper diagram",
        "Check parameter count matches paper",
        "Verify initialization (Xavier, Kaiming, etc.)",
        "Check activation functions and normalization placement",
    ],
    "training": [
        "Batch size (adjust if necessary for GPU memory)",
        "Learning rate + schedule (cosine, step, warmup)",
        "Weight decay, optimizer (SGD with momentum, AdamW)",
        "Number of epochs/iterations",
        "Gradient clipping threshold",
        "Mixed precision (FP16 vs FP32)",
    ],
    "evaluation": [
        "Same metric implementation (macro vs micro)",
        "Check reported vs actual metric scale",
        "Run multiple seeds (3-5) for variance estimate",
        "Verify no test set leakage during hyperparameter tuning",
    ],
}
```

## Ablation Studies

### Purpose
- Isolate contribution of each component
- Understand what matters and why
- Verify each design choice is justified

### Example Structure
| Component | Full model | Without A | Without B | Ablation |
|-----------|------------|-----------|-----------|----------|
| Accuracy | 95.0 | 93.2 (-1.8) | 94.1 (-0.9) | C is critical |

### Key Ablations
- Remove each novel component independently
- Replace with simpler baseline variant
- Vary hyperparameters of key components
- Test on multiple datasets/domains

## Documentation and Reproducibility

### What to Record
- All hyperparameters and their values
- Hardware details (GPU model, count, RAM, storage)
- Software versions (Python, CUDA, libraries)
- Random seeds used (one per run)
- Data preprocessing scripts
- Training time and convergence curves
- Final metrics with confidence intervals

### Tools
| Tool | Purpose |
|------|---------|
| Weights & Biases | Experiment tracking |
| MLflow | Model registry |
| DVC | Data versioning |
| Hydra | Config management |
| Sacred | Experiment seeds |
| Docker | Environment reproduction |

## References
- Raff, "A Step-by-Step Guide to Reproducing ML Papers", 2022
- Gundersen, Coakley, et al., "The State of Reproducibility in ML Research", Communications of the ACM 2023
- Pineau, "Reproducibility Checklist for ML Papers", NeurIPS 2019-2023
- Joppa, "The Case for Reproducible Research in Machine Learning", 2020
- Various: Official GitHub repos for major architecture reproductions
