# 🌳 Decision Trees
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Tree-based models, feature importance, overfitting, pruning.

## Training

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)
```

## Feature Importance

```python
importances = model.feature_importances_
for name, imp in zip(feature_names, importances):
    print(f"{name}: {imp:.3f}")
```

## Overfitting Control

| Parameter | Effect |
|-----------|--------|
| `max_depth` | Limit tree depth |
| `min_samples_split` | Min samples to split a node |
| `min_samples_leaf` | Min samples per leaf |
| `max_features` | Features to consider per split |

## Visualization

```python
from sklearn.tree import plot_tree

plot_tree(model, feature_names=feature_names, class_names=class_names)
```

<!-- 🤔 Deep trees overfit easily. Use `max_depth=3-10` and `min_samples_leaf=5+` for robust models. -->

## Run the Code

```bash
python code/04-decision-trees.py
```
