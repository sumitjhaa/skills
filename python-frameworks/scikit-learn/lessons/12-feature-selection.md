# 🔍 Feature Selection
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** SelectKBest, RFE, L1 regularization, mutual information.

## SelectKBest

```python
from sklearn.feature_selection import SelectKBest, f_classif

selector = SelectKBest(score_func=f_classif, k=5)
X_selected = selector.fit_transform(X, y)
```

## Recursive Feature Elimination

```python
from sklearn.feature_selection import RFE
from sklearn.svm import SVC

selector = RFE(estimator=SVC(kernel='linear'), n_features_to_select=5)
selector.fit(X, y)
print(selector.support_)     # Selected features
print(selector.ranking_)     # Feature ranks
```

## L1 Regularization

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(penalty='l1', solver='liblinear', C=0.1)
model.fit(X, y)
print(model.coef_)  # Many zeros = features eliminated
```

## Mutual Information

```python
from sklearn.feature_selection import mutual_info_classif

mi = mutual_info_classif(X, y)
```

<!-- 🤔 L1 regularization automatically removes irrelevant features — no separate selector needed. -->

## Run the Code

```bash
python code/12-feature-selection.py
```
