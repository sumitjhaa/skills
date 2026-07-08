"""Hidden Markov Model (Forward, Viterbi, Baum-Welch) from scratch."""
import numpy as np

class HMM:
    def __init__(self, n_states, n_obs):
        self.n = n_states
        self.m = n_obs
        self.A = np.ones((n_states, n_states)) / n_states
        self.B = np.ones((n_states, n_obs)) / n_obs
        self.pi = np.ones(n_states) / n_states

    def forward(self, obs):
        T = len(obs)
        alpha = np.zeros((T, self.n))
        alpha[0] = self.pi * self.B[:, obs[0]]
        alpha[0] /= alpha[0].sum()
        for t in range(1, T):
            alpha[t] = (alpha[t-1] @ self.A) * self.B[:, obs[t]]
            alpha[t] /= alpha[t].sum() + 1e-300
        return alpha

    def backward(self, obs):
        T = len(obs)
        beta = np.zeros((T, self.n))
        beta[-1] = 1
        for t in range(T-2, -1, -1):
            beta[t] = (self.A @ (self.B[:, obs[t+1]] * beta[t+1]))
            beta[t] /= beta[t].sum() + 1e-300
        return beta

    def viterbi(self, obs):
        T = len(obs)
        delta = np.zeros((T, self.n))
        psi = np.zeros((T, self.n), dtype=int)
        delta[0] = np.log(self.pi + 1e-300) + np.log(self.B[:, obs[0]] + 1e-300)
        for t in range(1, T):
            for j in range(self.n):
                probs = delta[t-1] + np.log(self.A[:, j] + 1e-300)
                psi[t, j] = np.argmax(probs)
                delta[t, j] = probs[psi[t, j]] + np.log(self.B[j, obs[t]] + 1e-300)
        path = [np.argmax(delta[T-1])]
        for t in range(T-1, 0, -1):
            path.insert(0, psi[t, path[0]])
        return path

    def baum_welch(self, obs, max_iter=100):
        T = len(obs)
        for iteration in range(max_iter):
            alpha = self.forward(obs)
            beta = self.backward(obs)
            gamma = alpha * beta
            gamma /= gamma.sum(axis=1, keepdims=True) + 1e-300

            xi = np.zeros((T-1, self.n, self.n))
            for t in range(T-1):
                xi[t] = alpha[t][:, None] * self.A * self.B[:, obs[t+1]][None, :] * beta[t+1][None, :]
                xi[t] /= xi[t].sum() + 1e-300

            self.pi = gamma[0]
            self.A = xi.sum(axis=0) / gamma[:-1].sum(axis=0)[:, None]
            for k in range(self.m):
                mask = obs == k
                self.B[:, k] = gamma[mask].sum(axis=0) / gamma.sum(axis=0)
            self.A /= self.A.sum(axis=1, keepdims=True) + 1e-300
            self.B /= self.B.sum(axis=1, keepdims=True) + 1e-300

    def log_likelihood(self, obs):
        alpha = self.forward(obs)
        return np.log(alpha[-1].sum() + 1e-300)

if __name__ == "__main__":
    np.random.seed(42)
    hmm = HMM(n_states=2, n_obs=3)
    obs = np.random.choice(3, size=50, p=[0.3, 0.4, 0.3])

    hmm.baum_welch(obs, max_iter=50)
    print(f"Transition matrix:\n{hmm.A}")
    print(f"Emission matrix:\n{hmm.B}")

    path = hmm.viterbi(obs)
    print(f"Most likely path length: {len(path)}")
    print(f"Viterbi path (first 10): {path[:10]}")

    print(f"Log-likelihood: {hmm.log_likelihood(obs):.2f}")
