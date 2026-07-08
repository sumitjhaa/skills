"""Multi-Label Learning (Binary Relevance, Classifier Chains) from scratch."""
import numpy as np

class BinaryRelevance:
    def __init__(self):
        self.models = {}

    def fit(self, X, Y):
        n_labels = Y.shape[1]
        for l in range(n_labels):
            from sklearn.linear_model import LogisticRegression
            m = LogisticRegression(max_iter=200)
            m.fit(X, Y[:, l])
            self.models[l] = m

    def predict(self, X):
        Y_pred = np.zeros((X.shape[0], len(self.models)))
        for l, m in self.models.items():
            Y_pred[:, l] = m.predict(X)
        return Y_pred

class ClassifierChain:
    def __init__(self, order=None):
        self.order = order
        self.models = {}

    def fit(self, X, Y):
        n, d = X.shape
        n_labels = Y.shape[1]
        if self.order is None:
            self.order = list(range(n_labels))
        X_aug = X.copy()
        for l in self.order:
            from sklearn.linear_model import LogisticRegression
            m = LogisticRegression(max_iter=200)
            m.fit(X_aug, Y[:, l])
            self.models[l] = m
            X_aug = np.c_[X_aug, Y[:, l]]

    def predict(self, X):
        X_aug = X.copy()
        Y_pred = np.zeros((X.shape[0], len(self.models)))
        for l in self.order:
            Y_pred[:, l] = self.models[l].predict(X_aug)
            X_aug = np.c_[X_aug, Y_pred[:, l]]
        return Y_pred

def hamming_loss(Y_true, Y_pred):
    return np.mean(Y_true != Y_pred)

if __name__ == "__main__":
    np.random.seed(42)
    n = 300; d = 10; n_labels = 5
    X = np.random.randn(n, d)
    Y = np.random.randint(0, 2, size=(n, n_labels))

    split = n // 2
    X_tr, X_te = X[:split], X[split:]
    Y_tr, Y_te = Y[:split], Y[split:]

    br = BinaryRelevance()
    br.fit(X_tr, Y_tr)
    br_pred = br.predict(X_te)
    print(f"Binary Relevance Hamming Loss: {hamming_loss(Y_te, br_pred):.4f}")

    cc = ClassifierChain()
    cc.fit(X_tr, Y_tr)
    cc_pred = cc.predict(X_te)
    print(f"Classifier Chain Hamming Loss: {hamming_loss(Y_te, cc_pred):.4f}")
