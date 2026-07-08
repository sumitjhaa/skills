"""GMM with EM algorithm from scratch."""
import numpy as np
from sklearn.datasets import make_blobs

class GMM:
    def __init__(self, n_components=3, max_iter=200, tol=1e-4, cov_type='full'):
        self.n_components = n_components
        self.max_iter = max_iter
        self.tol = tol
        self.cov_type = cov_type

    def fit(self, X):
        n, d = X.shape
        idx = np.random.choice(n, self.n_components, replace=False)
        self.means_ = X[idx].copy()
        self.weights_ = np.ones(self.n_components) / self.n_components
        self.covs_ = np.array([np.eye(d) * np.var(X) for _ in range(self.n_components)])

        log_likelihood = -np.inf
        for iteration in range(self.max_iter):
            self.resp_ = self._e_step(X)
            self._m_step(X)

            new_ll = self._log_likelihood(X)
            if abs(new_ll - log_likelihood) < self.tol:
                print(f"EM converged in {iteration+1} iterations")
                break
            log_likelihood = new_ll

        return self

    def _e_step(self, X):
        n = X.shape[0]
        resp = np.zeros((n, self.n_components))
        for k in range(self.n_components):
            diff = X - self.means_[k]
            if self.cov_type == 'diag':
                cov_inv = np.diag(1.0 / (np.diag(self.covs_[k]) + 1e-6))
            else:
                cov_inv = np.linalg.inv(self.covs_[k] + 1e-6 * np.eye(X.shape[1]))
            det = np.linalg.det(self.covs_[k] + 1e-6 * np.eye(X.shape[1]))
            norm_const = 1.0 / np.sqrt((2*np.pi)**X.shape[1] * det + 1e-300)
            resp[:, k] = self.weights_[k] * norm_const * np.exp(-0.5 * np.sum(diff @ cov_inv * diff, axis=1))
        resp_sum = resp.sum(axis=1, keepdims=True)
        resp = resp / (resp_sum + 1e-300)
        return resp

    def _m_step(self, X):
        Nk = self.resp_.sum(axis=0)
        self.weights_ = Nk / X.shape[0]
        self.means_ = (self.resp_.T @ X) / Nk[:, None]
        for k in range(self.n_components):
            diff = X - self.means_[k]
            if self.cov_type == 'diag':
                self.covs_[k] = np.diag((self.resp_[:, k, None] * diff).T @ diff / Nk[k])
            else:
                self.covs_[k] = (self.resp_[:, k, None] * diff).T @ diff / Nk[k]

    def _log_likelihood(self, X):
        n = X.shape[0]
        ll = np.zeros(n)
        for k in range(self.n_components):
            diff = X - self.means_[k]
            cov_inv = np.linalg.inv(self.covs_[k] + 1e-6 * np.eye(X.shape[1]))
            det = np.linalg.det(self.covs_[k] + 1e-6 * np.eye(X.shape[1]))
            norm_const = 1.0 / np.sqrt((2*np.pi)**X.shape[1] * det + 1e-300)
            ll += self.weights_[k] * norm_const * np.exp(-0.5 * np.sum(diff @ cov_inv * diff, axis=1))
        return np.sum(np.log(ll + 1e-300))

    def predict(self, X):
        resp = self._e_step(X)
        return np.argmax(resp, axis=1)

if __name__ == "__main__":
    X, y = make_blobs(n_samples=300, centers=3, n_features=2, random_state=42)

    gmm = GMM(n_components=3)
    gmm.fit(X)
    print(f"GMM converged. Cluster means:\n{gmm.means_}")

    from sklearn.mixture import GaussianMixture
    sk = GaussianMixture(n_components=3, random_state=42).fit(X)
    print(f"sklearn GMM means:\n{sk.means_}")
