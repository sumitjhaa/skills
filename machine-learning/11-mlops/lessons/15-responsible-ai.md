# 11.15 Responsible AI

## Objective
Build fair, interpretable, and privacy-preserving ML systems.

## Fairness
- **Demographic parity**: P(pred=1 | group=A) ≈ P(pred=1 | group=B).
- **Equal opportunity**: TPR across groups should match.
- **Disparate impact**: ratio of positive rates < 0.8 is discriminatory.

```python
from fairlearn.metrics import demographic_parity_difference

dpd = demographic_parity_difference(y_true, y_pred, sensitive_features=groups)
assert dpd < 0.1
```

## Interpretability
- **SHAP** — Shapley values for feature importance.
  ```python
  import shap
  explainer = shap.Explainer(model)
  shap_values = explainer(X)
  shap.summary_plot(shap_values, X)
  ```
- **LIME** — local surrogate explanations.
- **Partial Dependence Plots** — marginal effect of a feature.

## Privacy
- **Differential Privacy (DP-SGD)** — add calibrated noise during training.
  ```python
  from opacus import PrivacyEngine
  privacy_engine = PrivacyEngine()
  model, optimizer, loader = privacy_engine.make_private(
      module=model, optimizer=optimizer, data_loader=loader,
      noise_multiplier=1.0, max_grad_norm=1.0,
  )
  ```
- **Federated Learning** — train across decentralized data without sharing raw data.

## Model Cards
Standardized documentation template:
- **Intended Use** & out-of-scope uses
- **Training Data** — sources, size, demographics
- **Performance** — overall + sliced by groups
- **Limitations & Biases**
- **Ethical Considerations**

## Best Practices
1. Evaluate fairness on all relevant demographic groups before deployment.
2. Generate and review SHAP explanations for every model version.
3. Include a model card in the model registry artifact.
4. Conduct red-teaming / adversarial testing for high-stakes models.
