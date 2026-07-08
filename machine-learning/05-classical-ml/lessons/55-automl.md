# Lesson 05.55: AutoML / Auto-sklearn / TPOT / H2O

## Learning Objectives
- Understand AutoML problem formulation (CASH)
- Implement combined algorithm selection and hyperparameter optimization
- Apply meta-learning for warm-starting
- Use Bayesian optimization and bandit methods for efficient search
- Compare AutoML frameworks (auto-sklearn, TPOT, H2O)

## CASH Problem
Combined Algorithm Selection and Hyperparameter optimization:

$$A^* = \arg\min_{A \in \mathcal{A}, \lambda \in \Lambda_A} \frac{1}{K} \sum_{i=1}^K \mathcal{L}(A_\lambda, D^{(i)}_{\text{train}}, D^{(i)}_{\text{val}})$$

- $\mathcal{A}$: Set of ML algorithms
- $\Lambda_A$: Hyperparameter space for algorithm $A$
- $K$-fold cross-validation
- NP-hard in general — requires approximation

## Auto-sklearn

### Architecture
1. **Meta-learning**: Warm-start using past evaluations
2. **Bayesian optimization**: SMAC (sequential model-based optimization)
3. **Ensemble selection**: Combine top models from search

### Meta-Learning
Given a new dataset $D$:
1. Extract 38 meta-features (statistical + information-theoretic)
2. Compute distance to meta-features of 140+ OpenML datasets
3. Rank algorithms by performance on nearest datasets
4. Start BO from top $k$ configurations

### Bayesian Optimization via SMAC
1. Random forest surrogate: $\hat{p}(y | \lambda) = \mathcal{N}(\mu(\lambda), \sigma^2(\lambda))$
2. Acquisition: Expected Improvement $EI(\lambda) = \mathbb{E}[\max(f^* - f(\lambda), 0)]$
3. Conditional spaces: Handle algorithm choice conditionally

### Ensemble Selection
Greedy ensemble from ensemble library (top 50 models):
```
S = {}
for step in 1..50:
    for M in candidates:
        S' = S ∪ {M}
        score = eval_ensemble(S')
    S = S ∪ best_M
    if no improvement: break
```

## TPOT
Tree-based Pipeline Optimization Tool:

- **Representation**: Each pipeline is a tree (operators = nodes, data flow = edges)
- **Search**: Genetic programming (GP)
- **Crossover**: Swap subtrees between two pipelines
- **Mutation**: Insert/replace/remove operator; change hyperparameter
- **Selection**: Tournament selection on CV accuracy
- **Initialization**: Random, optionally seeded with common pipelines

### Genetic Programming Loop
```
population = initialize(N)
for generation in 1..G:
    fitness = [eval(p) for p in population]
    new_pop = []
    for _ in range(N/2):
        p1, p2 = tournament_select(population)
        child1, child2 = crossover(p1, p2)
        new_pop += [mutate(child1), mutate(child2)]
    population = new_pop
return best(population)
```

### Preprocessing Operators
Imputation, scaling (standard, minmax, robust), PCA, feature selection (SelectKBest, RFE), polynomial features, OneHotEncoding, etc.

## H2O AutoML
Optimized for tabular data, production deployment:

1. **Base models**: XGBoost, GBM, GLM, RF, Deep Learning (fixed grid)
2. **Stacked ensembles**: Multiple metalearners (GLM, RF, GBM)
3. **Stopping**: Early stopping on leaderboard metric
4. **Time constraint**: BL1 (base + random grid if time allows)

### H2O Stacking
```
base_learners = [LR, RF, GBM, XGB, DL]
metalearner = GLM(elastic_net=0.5)
# Train base learners with CV
for model in base_learners:
    out_of_fold_preds = kfold_predict(model, data)
# Train metalearner on out-of-fold predictions
stacked_model = metalearner.fit(out_of_fold_preds, y)
```

## Code: AutoML with FLAML

```python
from flaml import AutoML

automl = AutoML()
automl.fit(
    X_train, y_train,
    task="classification",
    time_budget=120,  # 2 minutes
    metric="accuracy",
    ensemble=True,
    max_iter=100
)

# Best model and config
print(automl.best_config)
print(automl.best_loss)

# Predict
preds = automl.predict(X_test)
probas = automl.predict_proba(X_test)
```

## Framework Comparison

| Feature | Auto-sklearn | TPOT | H2O | FLAML |
|---------|-------------|------|-----|-------|
| Search | SMAC (BO) | GP | Grid | CFO (Budget) |
| Ensemble | Greedy + stacking | Voting | Stacked | Optional |
| Meta-learning | Yes (OpenML) | No | No | No |
| Search space | Conditional | DAG | Fixed list | Learned |
| Time control | Yes | Early stop | Yes | Budget |
| Cold start | Fast (meta) | Slow | Fast | Fast |

## Search Space Design
- **Conditional**: If `algorithm = SVM`, then enable `kernel`, `C`, `gamma`
- **Hierarchical**: `preprocessor` (PCA, ICA, etc.) → `n_components`
- **Hardware-aware**: Memory limits, GPU support, parallel workers

## Practical Considerations
- **Time budget**: 1h for small datasets, 12-24h for large
- **Data prep**: AutoML handles missing values, scaling, encoding
- **Overfitting**: Use CV, early stopping, ensemble averaging
- **Cold start**: Meta-learning saves 10x evaluations (auto-sklearn)
- **Interpretability**: TPOT produces human-readable pipelines
- **Reproducibility**: Set `random_state`, log all configs
- **Large data**: H2O/framework-specific optimized backends

## Current Trends
- **Neural architecture search (NAS)**: AutoML for deep learning
- **NAS-Bench**: Benchmark datasets for NAS evaluation
- **AutoML-Zero**: Discover ML algorithms from basic math operations
- **Foundation model adaptation**: Auto-fine-tuning, prompt search
- **Federated AutoML**: Distributed search across data silos

## References
- Thornton et al., "Auto-WEKA: Combined Selection and Hyperparameter Optimization" (NeurIPS 2013)
- Feurer et al., "Efficient and Robust Automated Machine Learning" (NeurIPS 2015, auto-sklearn)
- Olson et al., "Evaluation of a Tree-based Pipeline Optimization Tool" (TPOT, GECCO 2016)
- LeDell & Poirier, "H2O AutoML: Scalable Automatic Machine Learning" (AutoML Workshop, 2020)
- Wang et al., "FLAML: A Fast and Lightweight AutoML Library" (MLSys 2021)
- Hutter, Kotthoff, Vanschoren (eds.), "Automated Machine Learning" (Springer, 2019)
