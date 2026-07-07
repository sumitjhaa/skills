# 🤝 Ensemble Methods
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** Voting classifiers, stacking, bagging, boosting.

## Voting Classifier

```python
from sklearn.ensemble import VotingClassifier

vote = VotingClassifier(estimators=[
    ('lr', LogisticRegression()),
    ('rf', RandomForestClassifier(n_estimators=100)),
    ('svm', SVC(probability=True)),
], voting='soft')  # 'soft' averages probabilities
```

## Stacking

```python
from sklearn.ensemble import StackingClassifier

stack = StackingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(n_estimators=100)),
        ('svm', SVC(probability=True)),
    ],
    final_estimator=LogisticRegression(),
)
```

## Bagging

```python
from sklearn.ensemble import BaggingClassifier

bag = BaggingClassifier(
    estimator=DecisionTreeClassifier(),
    n_estimators=100,
    max_samples=0.8,
    bootstrap=True,
)
```

## Gradient Boosting

```python
from sklearn.ensemble import GradientBoostingClassifier

gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3)
```

<!-- 🤔 Ensembles almost always outperform individual models. Start with Random Forest, then try stacking. -->

## Run the Code

```bash
python code/15-ensemble-methods.py
```
