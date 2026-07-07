"""Ensemble methods — voting, stacking, bagging, boosting."""
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier, VotingClassifier,
    StackingClassifier, BaggingClassifier, GradientBoostingClassifier)
from sklearn.svm import SVC
from sklearn.datasets import make_classification


print("=== Ensemble Methods ===\n")

X, y = make_classification(n_samples=500, n_features=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree":       DecisionTreeClassifier(random_state=42),
    "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42),
    "SVM":                 SVC(probability=True, random_state=42),
}

for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=3, scoring='accuracy')
    print(f"{name:<20s}: CV accuracy={scores.mean():.4f}")

voting_soft = VotingClassifier(
    estimators=[('lr', LogisticRegression()), ('rf', RandomForestClassifier(n_estimators=100)),
                ('svm', SVC(probability=True))],
    voting='soft'
)
voting_soft.fit(X_train, y_train)
print(f"\nVoting (soft):           {accuracy_score(y_test, voting_soft.predict(X_test)):.4f}")

stacking = StackingClassifier(
    estimators=[('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
                ('svm', SVC(probability=True, random_state=42))],
    final_estimator=LogisticRegression(),
)
stacking.fit(X_train, y_train)
print(f"Stacking:                {accuracy_score(y_test, stacking.predict(X_test)):.4f}")

bagging = BaggingClassifier(
    estimator=DecisionTreeClassifier(),
    n_estimators=100, random_state=42
)
bagging.fit(X_train, y_train)
print(f"Bagging (100 trees):     {accuracy_score(y_test, bagging.predict(X_test)):.4f}")

gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
gb.fit(X_train, y_train)
print(f"Gradient Boosting:       {accuracy_score(y_test, gb.predict(X_test)):.4f}")
