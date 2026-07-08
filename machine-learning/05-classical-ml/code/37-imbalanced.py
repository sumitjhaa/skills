"""Imbalanced Learning (SMOTE, cost-sensitive) from scratch."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

class SMOTE:
    def __init__(self, k_neighbors=5, sampling_strategy='auto'):
        self.k = k_neighbors

    def fit_resample(self, X, y):
        classes, counts = np.unique(y, return_counts=True)
        maj_class = classes[np.argmax(counts)]
        min_class = classes[np.argmin(counts)]
        X_min = X[y == min_class]
        n_min = len(X_min)

        dist = np.sum(X_min**2, axis=1)[:, None] + np.sum(X_min**2, axis=1)[None, :] - 2 * X_min @ X_min.T
        np.fill_diagonal(dist, np.inf)

        n_synthetic = counts.max() - n_min
        synthetic = []

        for _ in range(n_synthetic):
            i = np.random.randint(n_min)
            nn = np.argsort(dist[i])[:self.k]
            j = nn[np.random.randint(len(nn))]
            lam = np.random.random()
            syn = X_min[i] + lam * (X_min[j] - X_min[i])
            synthetic.append(syn)

        X_res = np.vstack([X, np.array(synthetic)])
        y_res = np.append(y, [min_class] * len(synthetic))
        return X_res, y_res

class CostSensitiveLR:
    def __init__(self, class_weight=None):
        self.class_weight = class_weight
        self.w = None

    def fit(self, X, y):
        n, d = X.shape
        X = np.c_[np.ones(n), X]
        self.w = np.zeros(d+1)
        if self.class_weight is None:
            self.class_weight = {0: 1.0, 1: 1.0}
        for _ in range(200):
            p = 1 / (1 + np.exp(-X @ self.w))
            weights = np.array([self.class_weight[int(yi)] for yi in y])
            grad = X.T @ (weights * (p - y)) / n
            self.w -= 0.1 * grad

    def predict(self, X):
        X = np.c_[np.ones(X.shape[0]), X]
        return (1 / (1 + np.exp(-X @ self.w)) >= 0.5).astype(int)

if __name__ == "__main__":
    X, y = make_classification(n_samples=500, n_features=5, weights=[0.9, 0.1], random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"Original class distribution: {np.bincount(y_tr)}")

    X_res, y_res = SMOTE().fit_resample(X_tr, y_tr)
    print(f"SMOTE resampled: {np.bincount(y_res)}")

    lr = LogisticRegression()
    lr.fit(X_res, y_res) if hasattr(LogisticRegression, 'fit') else None
    from sklearn.linear_model import LogisticRegression as SKLR
    smote_model = SKLR(max_iter=200).fit(X_res, y_res)
    print(f"SMOTE + LR F1: {f1_score(y_te, smote_model.predict(X_te)):.4f}")

    cs_model = CostSensitiveLR(class_weight={0: 1.0, 1: 9.0})
    cs_model.fit(X_tr, y_tr)
    print(f"Cost-sensitive LR F1: {f1_score(y_te, cs_model.predict(X_te)):.4f}")

    baseline = SKLR(max_iter=200).fit(X_tr, y_tr)
    print(f"Baseline LR F1: {f1_score(y_te, baseline.predict(X_te)):.4f}")
