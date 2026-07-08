"""Probability Calibration (Platt scaling, isotonic regression) from scratch."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import brier_score_loss

class PlattCalibration:
    def __init__(self):
        self.a = 0; self.b = 0

    def fit(self, scores, y):
        pos = y.sum(); neg = len(y) - pos
        t = np.where(y == 1, (pos+1)/(pos+2), 1/(neg+2))
        self.a, self.b = 0, 0
        for _ in range(100):
            p = 1 / (1 + np.exp(self.a * scores + self.b))
            grad_a = (p * (1-p) * scores * (p - t)).sum()
            grad_b = (p * (1-p) * (p - t)).sum()
            self.a -= 0.01 * grad_a
            self.b -= 0.01 * grad_b
        return self

    def predict(self, scores):
        return 1 / (1 + np.exp(self.a * scores + self.b))

class IsotonicRegression:
    def __init__(self):
        self.boundaries = None; self.values = None

    def fit(self, scores, y):
        idx = np.argsort(scores)
        scores, y = scores[idx], y[idx]
        n = len(scores)
        y_hat = y.copy()
        for _ in range(n):
            changed = False
            for i in range(n-1):
                if y_hat[i] > y_hat[i+1]:
                    y_hat[i] = y_hat[i+1] = (y_hat[i] + y_hat[i+1]) / 2
                    changed = True
            if not changed: break
        uniq, uniq_idx = np.unique(scores, return_index=True)
        self.boundaries = uniq
        self.values = y_hat[uniq_idx]
        return self

    def predict(self, scores):
        return np.interp(scores, self.boundaries, self.values)

if __name__ == "__main__":
    X, y = make_classification(n_samples=500, n_features=5, random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    from sklearn.linear_model import LogisticRegression
    lr = LogisticRegression(max_iter=200).fit(X_tr, y_tr)
    raw_scores = lr.decision_function(X_te)
    probs = lr.predict_proba(X_te)[:, 1]

    print(f"Before calibration - Brier: {brier_score_loss(y_te, probs):.4f}")

    platt = PlattCalibration()
    platt.fit(raw_scores[:50], y_te[:50])
    cal_probs = platt.predict(raw_scores)
    print(f"Platt calibrated - Brier: {brier_score_loss(y_te, cal_probs):.4f}")

    iso = IsotonicRegression()
    iso.fit(raw_scores[:50], y_te[:50])
    iso_probs = iso.predict(raw_scores)
    print(f"Isotonic calibrated - Brier: {brier_score_loss(y_te, iso_probs):.4f}")
