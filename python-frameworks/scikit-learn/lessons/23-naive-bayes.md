# 📊 Naive Bayes
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** GaussianNB, MultinomialNB, BernoulliNB, when to use each.

## Gaussian Naive Bayes

```python
from sklearn.naive_bayes import GaussianNB

model = GaussianNB()
model.fit(X_train, y_train)
```

## Variants

```python
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, ComplementNB

# For text classification (word counts)
mnb = MultinomialNB()

# For binary features
bnb = BernoulliNB()

# For imbalanced text data
cnb = ComplementNB()
```

## Pros & Cons

| Pros | Cons |
|------|------|
| Fast to train & predict | Assumes feature independence |
| Works with small data | Correlated features hurt |
| Good for text classification | Calibrated probabilities need work |

<!-- 🤔 Naive Bayes is a great baseline for text classification. It's surprisingly effective despite the "naive" assumption. -->

## Run the Code

```bash
python code/23-naive-bayes.py
```
