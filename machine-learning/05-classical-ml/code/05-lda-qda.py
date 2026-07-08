"""LDA and QDA from scratch."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class LDA:
    def fit(self, X, y):
        self.classes_ = np.unique(y)
        n, d = X.shape
        self.priors_ = {}
        self.means_ = {}
        within_class_cov = np.zeros((d, d))
        for c in self.classes_:
            Xc = X[y == c]
            self.priors_[c] = len(Xc) / n
            self.means_[c] = Xc.mean(axis=0)
            centered = Xc - self.means_[c]
            within_class_cov += centered.T @ centered
        self.cov_ = within_class_cov / (n - len(self.classes_))
        self.cov_inv_ = np.linalg.pinv(self.cov_)

    def decision_function(self, X):
        scores = []
        for c in self.classes_:
            mu = self.means_[c]
            score = X @ self.cov_inv_ @ mu - 0.5 * mu @ self.cov_inv_ @ mu + np.log(self.priors_[c])
            scores.append(score)
        return np.column_stack(scores)

    def predict(self, X):
        return self.classes_[np.argmax(self.decision_function(X), axis=1)]

class QDA:
    def fit(self, X, y):
        self.classes_ = np.unique(y)
        n, d = X.shape
        self.priors_ = {}
        self.means_ = {}
        self.covs_ = {}
        self.cov_invs_ = {}
        self.log_dets_ = {}
        for c in self.classes_:
            Xc = X[y == c]
            self.priors_[c] = len(Xc) / n
            self.means_[c] = Xc.mean(axis=0)
            centered = Xc - self.means_[c]
            cov = centered.T @ centered / (len(Xc) - 1)
            self.covs_[c] = cov + 1e-6 * np.eye(d)
            self.cov_invs_[c] = np.linalg.pinv(self.covs_[c])
            self.log_dets_[c] = np.log(np.linalg.det(self.covs_[c]) + 1e-12)

    def decision_function(self, X):
        scores = []
        for c in self.classes_:
            mu = self.means_[c]
            centered = X - mu
            quad = np.sum(centered @ self.cov_invs_[c] * centered, axis=1)
            score = -0.5 * quad - 0.5 * self.log_dets_[c] + np.log(self.priors_[c])
            scores.append(score)
        return np.column_stack(scores)

    def predict(self, X):
        return self.classes_[np.argmax(self.decision_function(X), axis=1)]

if __name__ == "__main__":
    X, y = make_classification(n_samples=300, n_features=5, n_informative=5,
                                n_redundant=0, n_clusters_per_class=1, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    lda = LDA()
    lda.fit(X_train, y_train)
    print(f"LDA Accuracy: {accuracy_score(y_test, lda.predict(X_test)):.4f}")

    qda = QDA()
    qda.fit(X_train, y_train)
    print(f"QDA Accuracy: {accuracy_score(y_test, qda.predict(X_test)):.4f}")

    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
    print(f"sklearn LDA: {accuracy_score(y_test, LinearDiscriminantAnalysis().fit(X_train, y_train).predict(X_test)):.4f}")
    print(f"sklearn QDA: {accuracy_score(y_test, QuadraticDiscriminantAnalysis().fit(X_train, y_train).predict(X_test)):.4f}")
