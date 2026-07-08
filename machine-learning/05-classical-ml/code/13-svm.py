"""SVM with SMO algorithm from scratch."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class SVM:
    def __init__(self, C=1.0, kernel='linear', max_iter=1000, tol=1e-3):
        self.C = C
        self.kernel = kernel
        self.max_iter = max_iter
        self.tol = tol

    def _kernel_func(self, x1, x2):
        if self.kernel == 'linear':
            return np.dot(x1, x2)
        elif self.kernel == 'rbf':
            gamma = 1.0 / self.d
            return np.exp(-gamma * np.linalg.norm(x1-x2)**2)

    def fit(self, X, y):
        n, self.d = X.shape
        y = y.astype(float) * 2 - 1
        K = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                K[i, j] = self._kernel_func(X[i], X[j])

        alpha = np.zeros(n)
        b = 0.0
        passes = 0

        while passes < self.max_iter:
            num_changed = 0
            for i in range(n):
                Ei = np.sum(alpha * y * K[:, i]) + b - y[i]
                if (y[i]*Ei < -self.tol and alpha[i] < self.C) or (y[i]*Ei > self.tol and alpha[i] > 0):
                    j = np.random.choice([x for x in range(n) if x != i])
                    Ej = np.sum(alpha * y * K[:, j]) + b - y[j]
                    ai_old, aj_old = alpha[i], alpha[j]

                    if y[i] != y[j]:
                        L = max(0, alpha[j] - alpha[i])
                        H = min(self.C, self.C + alpha[j] - alpha[i])
                    else:
                        L = max(0, alpha[i] + alpha[j] - self.C)
                        H = min(self.C, alpha[i] + alpha[j])
                    if abs(L - H) < 1e-5: continue

                    eta = 2*K[i,j] - K[i,i] - K[j,j]
                    if eta >= 0: continue

                    alpha[j] -= y[j] * (Ei - Ej) / eta
                    alpha[j] = np.clip(alpha[j], L, H)
                    if abs(alpha[j] - aj_old) < 1e-5: continue

                    alpha[i] += y[i]*y[j]*(aj_old - alpha[j])

                    b1 = b - Ei - y[i]*(alpha[i]-ai_old)*K[i,i] - y[j]*(alpha[j]-aj_old)*K[i,j]
                    b2 = b - Ej - y[i]*(alpha[i]-ai_old)*K[i,j] - y[j]*(alpha[j]-aj_old)*K[j,j]
                    b = (b1 + b2) / 2
                    num_changed += 1

            passes += 1
            if num_changed == 0: passes += 1

        sv_idx = alpha > 1e-5
        self.alpha = alpha[sv_idx]
        self.sv_X = X[sv_idx]
        self.sv_y = y[sv_idx]
        self.b = b

    def predict(self, X):
        pred = []
        for x in X:
            s = self.b
            for a, sv, sy in zip(self.alpha, self.sv_X, self.sv_y):
                s += a * sy * self._kernel_func(x, sv)
            pred.append(np.sign(s))
        return ((np.array(pred) + 1) // 2).astype(int)

if __name__ == "__main__":
    X, y = make_classification(n_samples=200, n_features=5, random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    svm = SVM(C=1.0, max_iter=100)
    svm.fit(X_tr, y_tr)
    print(f"SVM Accuracy: {accuracy_score(y_te, svm.predict(X_te)):.4f}")

    from sklearn.svm import SVC
    sk = SVC(C=1.0, kernel='linear', gamma='scale').fit(X_tr, y_tr)
    print(f"sklearn SVM: {accuracy_score(y_te, sk.predict(X_te)):.4f}")
