"""Naive Bayes (Gaussian, Multinomial, Bernoulli) from scratch."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class GaussianNB:
    def fit(self, X, y):
        self.classes_ = np.unique(y)
        self.means_ = {}
        self.stds_ = {}
        self.priors_ = {}
        for c in self.classes_:
            Xc = X[y == c]
            self.means_[c] = Xc.mean(axis=0)
            self.stds_[c] = Xc.std(axis=0) + 1e-10
            self.priors_[c] = len(Xc) / len(X)
    def predict(self, X):
        probs = []
        for c in self.classes_:
            l = np.log(self.priors_[c])
            l += -0.5 * np.sum(np.log(2 * np.pi * self.stds_[c]**2))
            l += -0.5 * np.sum(((X - self.means_[c]) / self.stds_[c])**2, axis=1)
            probs.append(l)
        return self.classes_[np.argmax(probs, axis=0)]

class MultinomialNB:
    def __init__(self, alpha=1.0):
        self.alpha = alpha
    def fit(self, X, y):
        self.classes_ = np.unique(y)
        self.feature_log_prob_ = {}
        self.class_log_prior_ = {}
        for c in self.classes_:
            Xc = X[y == c]
            smoothed = Xc.sum(axis=0) + self.alpha
            self.feature_log_prob_[c] = np.log(smoothed / smoothed.sum())
            self.class_log_prior_[c] = np.log(len(Xc) / len(X))
    def predict(self, X):
        probs = []
        for c in self.classes_:
            l = self.class_log_prior_[c] + (X @ self.feature_log_prob_[c])
            probs.append(l)
        return self.classes_[np.argmax(probs, axis=0)]

class BernoulliNB:
    def __init__(self, alpha=1.0):
        self.alpha = alpha
    def fit(self, X, y):
        self.classes_ = np.unique(y)
        for c in self.classes_:
            Xc = X[y == c]
            self.feature_prob_[c] = (Xc.sum(axis=0) + self.alpha) / (len(Xc) + 2 * self.alpha)
            self.class_log_prior_[c] = np.log(len(Xc) / len(X))
    def predict(self, X):
        probs = []
        for c in self.classes_:
            p = self.feature_prob_[c]
            l = self.class_log_prior_[c]
            l += (X @ np.log(p + 1e-10)) + ((1 - X) @ np.log(1 - p + 1e-10))
            probs.append(l)
        return self.classes_[np.argmax(probs, axis=0)]

if __name__ == "__main__":
    X, y = make_classification(n_samples=500, n_features=10, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    gnb = GaussianNB()
    gnb.fit(X_train, y_train)
    print(f"Gaussian NB Accuracy: {accuracy_score(y_test, gnb.predict(X_test)):.4f}")

    from sklearn.naive_bayes import GaussianNB as SKGNB
    sk = SKGNB().fit(X_train, y_train)
    print(f"sklearn Gaussian NB Accuracy: {accuracy_score(y_test, sk.predict(X_test)):.4f}")
