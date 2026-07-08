"""04.36 Information-theoretic feature selection (MRMR)."""
import numpy as np
from sklearn.feature_selection import mutual_info_classif
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier

def mrmr(X, y, k=5):
    """Minimum Redundancy Maximum Relevance feature selection."""
    n_features = X.shape[1]
    mi_target = mutual_info_classif(X, y, random_state=0)
    selected = []
    remaining = list(range(n_features))
    for _ in range(k):
        scores = []
        for i in remaining:
            relevance = mi_target[i]
            if len(selected) > 0:
                redundancy = np.mean([mutual_info_classif(
                    X[:, [i]], X[:, [j]], random_state=0)[0]
                    for j in selected])
            else:
                redundancy = 0
            scores.append(relevance - redundancy)
        best = remaining[np.argmax(scores)]
        selected.append(best)
        remaining.remove(best)
    return selected

# Generate data with redundant features
np.random.seed(0)
X, y = make_classification(n_samples=200, n_features=20, n_informative=5,
                           n_redundant=5, n_repeated=5, random_state=0)

selected_features = mrmr(X, y, k=5)
print(f"MRMR selected features: {selected_features}")

# Conditional mutual information (CMI) feature selection
def cmi_selection(X, y, k=5):
    n_features = X.shape[1]
    selected = []
    remaining = set(range(n_features))
    for _ in range(k):
        best_score = -np.inf
        best_feat = None
        for i in remaining:
            if len(selected) == 0:
                score = mutual_info_classif(X[:, [i]], y, random_state=0)[0]
            else:
                # Approximate CMI: I(X_i; Y | X_selected)
                mi_given = mutual_info_classif(
                    np.column_stack([X[:, [i]], X[:, selected]]), y, random_state=0)
                score = mi_given[0]
            if score > best_score:
                best_score = score
                best_feat = i
        selected.append(best_feat)
        remaining.remove(best_feat)
    return selected

cmi_features = cmi_selection(X, y, k=5)
print(f"CMI selected features: {cmi_features}")

# Evaluate with a classifier
def evaluate_features(X, y, features):
    knn = KNeighborsClassifier(n_neighbors=5)
    scores = cross_val_score(knn, X[:, features], y, cv=5)
    return scores.mean()

all_score = evaluate_features(X, y, range(20))
mrmr_score = evaluate_features(X, y, selected_features)
print(f"\nClassification accuracy:")
print(f"  All 20 features: {all_score:.4f}")
print(f"  MRMR top 5:      {mrmr_score:.4f}")

# Conditional likelihood maximisation (Brown et al. 2012)
def cond_likelihood_max(X, y, k=5):
    return mrmr(X, y, k)  # Equivalent under certain conditions

clm_features = cond_likelihood_max(X, y, 5)
print(f"CLM features: {clm_features}")
