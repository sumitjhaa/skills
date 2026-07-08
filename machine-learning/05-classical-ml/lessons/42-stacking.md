# Lesson 05.42: Stacking / Blending

## Learning Objectives
- Understand stacked generalization for ensemble combination
- Implement CV stacking to prevent overfitting
- Design meta-model architectures
- Apply stacking to classification and regression

## Stacked Generalization
Two-level ensemble architecture:

1. **Level-0 (base models)**: $M$ diverse models trained on training data
2. **Level-1 data**: Base model predictions (out-of-fold) as features
3. **Level-1 (meta model)**: Trained on base model predictions

### Why Stacking Works
- Diversifies across model families (linear, tree-based, neural)
- Meta-model learns to weight models adaptively per region
- Reduces bias (if base models underfit) and variance (if overfit)
- Won Netflix Prize by combining SVD, RBM, PMF, and matrix factorization variants

## CV Stacking (K-Fold)
To prevent overfitting, generate meta-features via cross-validation:

```
for fold f in k-folds:
    hold out fold f as validation
    for each base model m:
        train m on k-1 folds
        predict on fold f (out-of-fold predictions)
concatenate all fold predictions = meta-features
train meta-model on out-of-fold predictions
```

Training base models on full data afterward is optional.

## Blending
Simpler variant:
1. Hold out a validation set (e.g., 10% of data)
2. Train base models on training set (remaining 90%)
3. Predict on validation set → meta-features
4. Train meta-model on validation predictions

**Tradeoffs**: Blending is faster (no CV) but uses less data for meta features → more prone to overfitting.

## Meta-Model Choices

| Meta-model | When to use | Properties |
|-----------|-------------|------------|
| Logistic Regression | Classification | Simple, calibrated, interpretable |
| Linear Regression | Regression | Simple, can be regularized (Ridge) |
| Decision Tree | Any | Interpretable, captures non-linear weights |
| Neural Net (1 layer) | Large data | Non-linear weighting |
| Gradient Boosting | Any | Powerful but can overfit meta-features |
| Average/Median | Baseline | Simple, often surprisingly good |

**Key insight**: Simple models often work best — complex meta-models easily overfit.

## Advanced Techniques

### Feature-Weighted Stacking
Include original features alongside base predictions:

$$z_i = [\hat{y}_i^{(1)}, \dots, \hat{y}_i^{(M)}, x_i]$$

Allows meta-model to learn feature-specific corrections.

### Multi-Level Stacking
Stack more than two levels: Level-2 predictions become features for Level-3, etc.

**Rule of thumb**: Rarely helpful beyond 2 levels (diminishing returns).

### Multi-Response Stacking
For multi-label/multi-output: meta-model predicts all targets jointly.

## Code: K-Fold Stacking

```python
import numpy as np
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression

def stacking_cv(base_models, meta_model, X, y, n_folds=5):
    kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)
    meta_features = np.zeros((len(X), len(base_models)))
    for fold, (train_idx, val_idx) in enumerate(kf.split(X)):
        X_train, y_train = X[train_idx], y[train_idx]
        X_val = X[val_idx]
        for m_idx, model in enumerate(base_models):
            model_clone = model.__class__(**model.get_params())
            model_clone.fit(X_train, y_train)
            meta_features[val_idx, m_idx] = model_clone.predict_proba(X_val)[:, 1]
    # Train meta-model
    meta_model.fit(meta_features, y)
    # Retrain base models on full data (optional)
    for model in base_models:
        model.fit(X, y)
    return base_models, meta_model

def predict_stacking(base_models, meta_model, X):
    meta_features = np.column_stack([m.predict_proba(X)[:, 1] for m in base_models])
    return meta_model.predict_proba(meta_features)[:, 1]
```

## Practical Considerations
- **Base model diversity**: Most important factor — combine very different model families
- **Correlated predictions**: If all base models agree, stacking adds little
- **CV fold choice**: 5-fold is standard; fewer folds increase bias, more folds increase variance
- **Probability vs class labels**: Using probabilities as meta-features preserves more information
- **Time series**: Use forward-chaining CV (time-aware splits)
- **Calibration**: Calibrate base model probabilities before stacking

## Common Pitfalls
- **Data leakage**: Always generate meta-features via CV — never on training predictions
- **Overfitting meta-model**: Use simple (regularized) meta-model
- **Base models too similar**: No diversity → no stacking benefit
- **Ignoring scale**: Base model outputs may need normalization for meta-model

## Results
- Usually 5-10% improvement over best single model
- Diminishing returns with more than 5-10 base models
- Averaging often achieves 80-90% of stacking's benefit
- Stacking most valuable when:
  - Base models have complementary strengths
  - Data is large enough for reliable CV
  - Computational budget allows multiple model training

## References
- Wolpert, "Stacked Generalization" (Neural Networks, 1992)
- Breiman, "Stacked Regressions" (Machine Learning, 1996)
- Ting & Witten, "Issues in Stacked Generalization" (JAIR, 1999)
- Sill et al., "Feature-Weighted Linear Stacking" (arXiv, 2009)
- LeDell, "Feature-Weighted Stacking" (PhD thesis, 2015)
