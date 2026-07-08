"""Kernel SVM with RBF from scratch."""
import numpy as np
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class KernelSVM:
    def __init__(self, C=1.0, gamma=1.0, max_iter=200, tol=1e-3):
        self.C = C
        self.gamma = gamma
        self.max_iter = max_iter
        self.tol = tol

    def _rbf(self, x1, x2):
        return np.exp(-self.gamma * np.linalg.norm(x1-x2)**2)

    def fit(self, X, y):
        n = X.shape[0]
        y = y.astype(float) * 2 - 1
        K = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                K[i, j] = self._rbf(X[i], X[j])

        alpha = np.zeros(n)
        b = 0.0
        n_iter = 0

        while n_iter < self.max_iter:
            n_changed = 0
            for i in range(n):
                Ei = np.sum(alpha * y * K[:, i]) + b - y[i]
                cond = (y[i]*Ei < -self.tol and alpha[i] < self.C) or (y[i]*Ei > self.tol and alpha[i] > 0)
                if not cond: continue
                j = np.random.choice([k for k in range(n) if k != i])
                Ej = np.sum(alpha * y * K[:, j]) + b - y[j]
                ai, aj = alpha[i], alpha[j]
                if y[i] != y[j]:
                    L = max(0, alpha[j] - alpha[i])
                    H = min(self.C, self.C + alpha[j] - alpha[i])
                else:
                    L = max(0, alpha[i] + alpha[j] - self.C)
                    H = min(self.C, alpha[i] + alpha[j])
                if abs(L-H) < 1e-5: continue
                eta = 2*K[i,j] - K[i,i] - K[j,j]
                if eta >= 0: continue
                alpha[j] -= y[j] * (Ei - Ej) / eta
                alpha[j] = np.clip(alpha[j], L, H)
                if abs(alpha[j] - aj) < 1e-5: continue
                alpha[i] += y[i]*y[j]*(aj - alpha[j])
                b1 = b - Ei - y[i]*(alpha[i]-ai)*K[i,i] - y[j]*(alpha[j]-aj)*K[i,j]
                b2 = b - Ej - y[i]*(alpha[i]-ai)*K[i,j] - y[j]*(alpha[j]-aj)*K[j,j]
                b = (b1 + b2) / 2
                n_changed += 1
            n_iter += 1
            if n_changed == 0: break

        sv = alpha > 1e-5
        self.alpha = alpha[sv]
        self.sv_X = X[sv]
        self.sv_y = y[sv]
        self.b = b

    def predict(self, X):
        preds = []
        for x in X:
            s = self.b
            for a, sv, sy in zip(self.alpha, self.sv_X, self.sv_y):
                s += a * sy * self._rbf(x, sv)
            preds.append(np.sign(s))
        return ((np.array(preds) + 1) // 2).astype(int)

if __name__ == "__main__":
    X, y = make_circles(n_samples=300, noise=0.1, factor=0.5, random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    ksvm = KernelSVM(C=1.0, gamma=1.0, max_iter=200)
    ksvm.fit(X_tr, y_tr)
    print(f"Kernel SVM (RBF) Accuracy: {accuracy_score(y_te, ksvm.predict(X_te)):.4f}")

    from sklearn.svm import SVC
    sk = SVC(C=1.0, gamma=1.0, kernel='rbf').fit(X_tr, y_tr)
    print(f"sklearn RBF SVM: {accuracy_score(y_te, sk.predict(X_te)):.4f}")
