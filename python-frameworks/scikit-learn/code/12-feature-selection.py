"""Feature selection — SelectKBest, RFE, L1, mutual information."""
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif, RFE, mutual_info_classif
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification


print("=== Feature Selection ===\n")

X, y = make_classification(n_samples=500, n_features=20, n_informative=5,
                           n_redundant=5, random_state=42)
feature_names = [f"f{i}" for i in range(20)]

print(f"Total features: {X.shape[1]}")
print(f"Informative: 5, Redundant: 5, Noise: 10\n")

selector = SelectKBest(score_func=f_classif, k=5)
X_selected = selector.fit_transform(X, y)
selected_idx = selector.get_support(indices=True)
print(f"SelectKBest (k=5): {selected_idx}")
print(f"  Scores: {selector.scores_[selected_idx].round(2)}")

rfe = RFE(estimator=SVC(kernel='linear'), n_features_to_select=5)
rfe.fit(X, y)
print(f"\nRFE selected: {np.where(rfe.support_)[0]}")
print(f"  Rankings: {rfe.ranking_}")

model = LogisticRegression(penalty='l1', solver='liblinear', C=0.1, random_state=42)
model.fit(X, y)
l1_selected = np.where(np.abs(model.coef_[0]) > 1e-5)[0]
print(f"\nL1 selected ({len(l1_selected)} features): {l1_selected}")

mi = mutual_info_classif(X, y)
top_mi = np.argsort(mi)[-5:][::-1]
print(f"\nMutual info top 5: {top_mi}")
print(f"  Scores: {mi[top_mi].round(4)}")
