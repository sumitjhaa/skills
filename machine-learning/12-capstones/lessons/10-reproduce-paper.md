# Lesson 12.10: Reproduce a SOTA Paper + Improve It

## Project Architecture

Select a recent influential ML paper, reproduce its core results, and then propose and implement a meaningful improvement.

```
Phase 1: Paper Selection
  Criteria:
  ├── Reproducible: clear methods, available datasets
  ├── Significant: influential paper (100+ citations)
  ├── Feasible: trainable in reasonable time
  └── Examples: LoRA, SwAV, SimCLR, BYOL, MAE, etc.

Phase 2: Reproduction
  ├── Parse the paper → extract algorithm details
  ├── Identify all hyperparameters from paper + appendix
  ├── Implement from scratch (no official repo copy)
  ├── Train on the same dataset(s)
  ├── Match reported metrics (within noise)
  └── Document discrepancies and debugging process

Phase 3: Ablation Studies
  ├── What happens if we remove component X?
  ├── Sensitivity to key hyperparameters
  ├── Scaling behavior (small → large)
  └── Failure mode analysis

Phase 4: Improvement
  ├── Identify a limitation of the original method
  ├── Propose a modification (theoretical or empirical)
  ├── Implement the modification
  ├── Run controlled experiment (same setup ± change)
  └── Statistical significance testing

Phase 5: Report
  ├── Paper reproduction results (table + plots)
  ├── Ablation findings
  ├── Improvement method and results
  └── Discussion of what worked and what didn't
```

## Design Decisions

### Paper choice: SimCLR
SimCLR is a good target because:
- Conceptually elegant (contrastive learning)
- Reproducible with moderate compute
- Clear ablation studies to verify
- Multiple avenues for improvement

### SimCLR summary
- **Objective**: learn visual representations without labels
- **Method**: augment image twice → encode → contrastive loss (NT-Xent)
- **Key components**: strong augmentations, large batch, projection head, temperature

### Reproduction setup
- Dataset: CIFAR-10 (no labels needed for pretraining)
- Encoder: ResNet-18 (simplified from ResNet-50)
- Batch size: 512 (simulated via gradient accumulation)
- Projection head: MLP (2048 → 2048 → 128)
- Temperature: 0.5
- Optimizer: LARS or AdamW with cosine decay

### Improvement ideas
1. **Adaptive augmentation**: learn which augmentations help per sample
2. **Hard negative mining**: weight negatives by similarity
3. **Multi-crop**: more views per image for cheaper
4. **Prototype-based**: add clustering objective to contrastive loss
5. **Adapter for finetuning**: parameter-efficient transfer

### Evaluation
- Linear evaluation protocol: freeze encoder, train linear classifier
- Compare top-1 accuracy against reported SimCLR baseline
- Ablate improvement component

## Implementation Guide

1. **Select paper and read thoroughly**
2. **Implement data augmentations** (random crop, color jitter, gaussian blur, grayscale)
3. **Implement the encoder** (ResNet-18)
4. **Implement projection head** (MLP)
5. **Implement NT-Xent loss** (contrastive loss)
6. **Implement pretraining loop** (large batch via grad accumulation)
7. **Implement linear evaluation protocol**
8. **Reproduce baseline metrics** and document any gaps
9. **Design and implement improvement**
10. **Run controlled comparison** (baseline vs. improved)
11. **Write report** with tables, plots, and analysis

## Key Insights

- Reproducing papers is harder than it looks: missing hyperparameters, subtle implementation details, hardware differences
- Ablations are often more informative than the main result
- A good improvement starts with understanding why the original works
- Statistical significance matters: run multiple seeds
- Not all improvements work — negative results are valuable too
