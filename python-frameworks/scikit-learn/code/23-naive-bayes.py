"""Naive Bayes — Gaussian, Multinomial, Bernoulli."""
import numpy as np
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import make_classification


print("=== Naive Bayes ===\n")

X, y = make_classification(n_samples=500, n_features=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

gnb = GaussianNB()
gnb.fit(X_train, y_train)
y_pred = gnb.predict(X_test)
print(f"GaussianNB: accuracy={accuracy_score(y_test, y_pred):.4f}")
scores = cross_val_score(gnb, X_train, y_train, cv=5, scoring='accuracy')
print(f"  CV accuracy: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

print(f"\nMultinomialNB (bag-of-words demo):")
rng = np.random.default_rng(42)
X_text = rng.poisson(1, (300, 50))  # Simulated word counts
y_text = rng.integers(0, 3, 300)
X_text_train, X_text_test, y_text_train, y_text_test = train_test_split(
    X_text, y_text, test_size=0.2, random_state=42
)
mnb = MultinomialNB()
mnb.fit(X_text_train, y_text_train)
print(f"  Accuracy: {accuracy_score(y_text_test, mnb.predict(X_text_test)):.4f}")

print(f"\nBernoulliNB (binary features):")
X_binary = rng.binomial(1, 0.3, (300, 20))
y_binary = rng.integers(0, 2, 300)
bnb = BernoulliNB()
bnb.fit(X_binary, y_binary)
scores = cross_val_score(bnb, X_binary, y_binary, cv=5, scoring='accuracy')
print(f"  CV accuracy: {scores.mean():.4f}")

print(f"\nProbabilities (first 5 samples):")
probs = gnb.predict_proba(X_test[:5])
for i, p in enumerate(probs):
    print(f"  Sample {i}: class0={p[0]:.4f}, class1={p[1]:.4f}")
