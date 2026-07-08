# Lesson 12.08: AutoML System

## Project Architecture

Build an end-to-end AutoML system that performs automated model selection, hyperparameter optimization, feature engineering, and ensemble construction for tabular data.

```
Input: Raw dataset (CSV)
│
├── 1. Data Profiling
│    ├── Detect column types (numeric, categorical, text, date)
│    ├── Missing value analysis
│    ├── Distribution analysis (skewness, outliers)
│    └── Cardinality for categoricals
│
├── 2. Feature Engineering
│    ├── Imputation (mean, median, mode, constant)
│    ├── Encoding (one-hot, label, target encoding)
│    ├── Scaling (standard, min-max, robust)
│    ├── Polynomial features
│    ├── Numeric → categorical binning
│    └── Feature selection (variance, correlation, mutual info)
│
├── 3. Model Selection
│    ├── Candidate pool: Linear, RF, XGBoost, MLP, SVM
│    ├── Pre-training with default params → prune weak models
│    └── Meta-learning: recommend models based on dataset meta-features
│
├── 4. Hyperparameter Optimization
│    ├── Strategies: Grid, Random, Bayesian (GP-based)
│    ├── Multi-fidelity: Successive Halving, HyperBand
│    ├── Early stopping: median stopping rule
│    └── Cross-validation: 5-fold stratified
│
├── 5. Ensemble
│    ├── Weighted averaging (learn weights via stacking)
│    ├── Greedy ensemble selection (Caruana's method)
│    └── Blending (holdout set for meta-learner)
│
└── 6. Output
     ├── Best model + config
     ├── Leaderboard of all trials
     ├── Feature importance
     └── Predictions on test set
```

## Design Decisions

### Search strategies
- Random Search: baseline, good for high-dimensional spaces
- Bayesian Optimization: Gaussian Process surrogate with Expected Improvement
- HyperBand: adaptive resource allocation, terminates poor performers early

### Configuration space
- Define a `ConfigSpace` with categorical, integer, float, and conditional parameters
- Parameters like: `n_estimators=[50,500]`, `max_depth=[3,30]`, `learning_rate=[1e-4,1e-1]`

### Trial management
- Each trial = (config, score, model, timestamp)
- Trial history stored for analysis and resume capability
- Asynchronous trial execution

### Pruning
- Median stopping rule: stop if best metric hasn't improved over past K evaluations
- Successive Halving: allocate budget to promising configs

### Metalearning
- Dataset meta-features: #rows, #cols, #classes, skewness, entropy, etc.
- KNN-based recommendation from previous experiments

## Implementation Guide

1. **Implement data profiler** (column type detection, statistics)
2. **Implement feature engineering pipeline** (impute, encode, scale)
3. **Implement model pool** (sklearn models with unified interface)
4. **Implement ConfigSpace** (parameter definitions)
5. **Implement Random Search**
6. **Implement Bayesian Optimization** (GP with EI)
7. **Implement HyperBand / Successive Halving**
8. **Implement trial database** (configs + results)
9. **Implement ensemble builder** (stacking, weighted averaging)
10. **Implement end-to-end AutoML pipeline**
11. **Test on multiple datasets and compare to single-model baselines**

## Key Insights

- Bayesian optimization is sample-efficient but expensive per iteration
- HyperBand can find good configs 5x faster than random search
- Feature engineering often matters more than model choice
- Ensembles almost always beat single models
- The data profiling step is critical: garbage in, garbage out
