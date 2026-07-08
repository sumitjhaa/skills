"""Conditional Random Fields (linear-chain) from scratch."""
import numpy as np

class CRF:
    def __init__(self, n_states, n_features, max_iter=100, lr=0.1):
        self.n = n_states
        self.d = n_features
        self.max_iter = max_iter
        self.lr = lr
        self.w = np.random.randn(n_states * n_features + n_states * n_states) * 0.01

    def _features(self, X, y_t, y_tm1, t):
        n_feats = self.n * self.d
        feat = np.zeros(self.n * self.d + self.n * self.n)
        for s in range(self.n):
            if y_t == s:
                feat[s * self.d:(s+1)*self.d] = X[t]
        if y_tm1 is not None:
            feat[n_feats + y_tm1 * self.n + y_t] = 1
        return feat

    def _score(self, X, y):
        T = len(X)
        s = 0
        for t in range(T):
            prev = y[t-1] if t > 0 else None
            s += self.w @ self._features(X, y[t], prev, t)
        return s

    def _forward_backward(self, X):
        T = len(X)
        alpha = np.zeros((T, self.n))
        alpha[0] = np.exp([self.w @ self._features(X, s, None, 0) for s in range(self.n)])
        alpha[0] /= alpha[0].sum()
        for t in range(1, T):
            for s in range(self.n):
                unary = self.w @ self._features(X, s, None, t)
                trans = np.array([self.w[self.n*self.d + prev*self.n + s] for prev in range(self.n)])
                alpha[t, s] = np.exp(unary) * np.sum(alpha[t-1] * np.exp(trans))
            alpha[t] /= alpha[t].sum() + 1e-300
        beta = np.zeros((T, self.n))
        beta[-1] = 1
        for t in range(T-2, -1, -1):
            for s in range(self.n):
                trans = np.array([self.w[self.n*self.d + s*self.n + sn] for sn in range(self.n)])
                unary = np.array([self.w @ self._features(X, sn, None, t+1) for sn in range(self.n)])
                beta[t, s] = np.sum(np.exp(trans + unary) * beta[t+1])
            beta[t] /= beta[t].sum() + 1e-300
        return alpha, beta

    def fit(self, X_list, y_list):
        for iteration in range(self.max_iter):
            grad = np.zeros_like(self.w)
            for X, y in zip(X_list, y_list):
                T = len(X)
                alpha, beta = self._forward_backward(X)
                gamma = alpha * beta
                gamma /= gamma.sum(axis=1, keepdims=True) + 1e-300
                for t in range(T):
                    for s in range(self.n):
                        grad[s*self.d:(s+1)*self.d] -= gamma[t, s] * X[t]
                for t in range(T-1):
                    for s in range(self.n):
                        for sn in range(self.n):
                            grad[self.n*self.d + s*self.n + sn] -= alpha[t, s] * np.exp(self.w[self.n*self.d + s*self.n + sn]) * beta[t+1, sn]
                for t in range(T):
                    prev = y[t-1] if t > 0 else None
                    grad += self._features(X, y[t], prev, t)
            self.w += self.lr * grad / len(X_list)
            if np.linalg.norm(grad) < 1e-3:
                print(f"CRF converged in {iteration+1} iterations")
                break

    def predict(self, X):
        T = len(X)
        delta = np.zeros((T, self.n))
        psi = np.zeros((T, self.n), dtype=int)
        delta[0] = np.array([self.w @ self._features(X, s, None, 0) for s in range(self.n)])
        for t in range(1, T):
            for s in range(self.n):
                unary = self.w @ self._features(X, s, None, t)
                trans = delta[t-1] + np.array([self.w[self.n*self.d + prev*self.n + s] for prev in range(self.n)])
                psi[t, s] = np.argmax(trans)
                delta[t, s] = trans[psi[t, s]] + unary
        path = [np.argmax(delta[T-1])]
        for t in range(T-1, 0, -1):
            path.insert(0, psi[t, path[0]])
        return path

if __name__ == "__main__":
    X_list = [np.random.randn(20, 5) for _ in range(50)]
    y_list = [np.random.choice(3, size=20) for _ in range(50)]

    crf = CRF(n_states=3, n_features=5, max_iter=20)
    crf.fit(X_list[:40], y_list[:40])
    pred = crf.predict(X_list[0])
    acc = np.mean(pred == y_list[0])
    print(f"CRF prediction accuracy on first sequence: {acc:.3f}")
