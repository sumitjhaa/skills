# 06.31 CIFAR Experiments

Using CIFAR-10/100 as a benchmark for deep learning experiments.

## Dataset

- CIFAR-10: 60K 32x32 color images, 10 classes (50K train, 10K test)
- CIFAR-100: 60K images, 100 classes (20 superclasses)

## Baseline Setup

- ResNet-20 or ResNet-56
- SGD with momentum (0.9), weight decay (0.0001)
- Cosine LR schedule, 200 epochs
- Batch size 128
- Random horizontal flip + random crop + normalization

Expected baseline: ~92% on CIFAR-10, ~70% on CIFAR-100

## Ablation Studies

Systematically vary one component at a time:

### Normalization
- BatchNorm vs LayerNorm vs GroupNorm vs None
- Measure: accuracy, training speed, batch size sensitivity

### Augmentation
- None vs basic (flip+crop) vs Cutout vs Mixup vs RandAugment
- Measure: accuracy, overfitting gap

### Depth
- ResNet-20 vs ResNet-32 vs ResNet-56 vs ResNet-110
- Measure: accuracy vs parameters

### Width
- Base width vs 2x vs 0.5x
- Measure: accuracy vs FLOPs

### Regularization
- Dropout (0.0, 0.1, 0.3, 0.5)
- Weight decay (0, 1e-5, 1e-4, 5e-4)
- Label smoothing (0, 0.05, 0.1, 0.2)

## Training Curves

For each experiment, log:
- Training loss (step-wise)
- Training accuracy (epoch-wise)
- Validation accuracy (epoch-wise)
- Gradient norm
- Learning rate

## Overfitting Diagnosis

- Training loss << Validation loss: overfitting
- Training loss ≈ Validation loss: underfitting or well-fit
- Validation loss increasing: overfitting from epoch N onward

## Learning Rate Sensitivity

Test peak LR: [0.01, 0.03, 0.1, 0.3, 1.0]
Test warmup steps: [0, 100, 500, 1000]

## Reporting

For each experiment, report:
1. Final test accuracy (mean ± std over 3 seeds)
2. Best epoch
3. Training time
4. Gradient statistics
