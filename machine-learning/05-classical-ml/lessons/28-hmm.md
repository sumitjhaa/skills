# Lesson 05.28: Hidden Markov Models

## Learning Objectives
- Understand the three canonical HMM problems
- Implement Forward-Backward and Viterbi algorithms
- Derive Baum-Welch (EM) for parameter estimation
- Apply scaling for numerical stability in long sequences

## Components
An HMM is defined by:
- **States**: $S = \{s_1, \dots, s_m\}$, hidden state sequence $q_1, \dots, q_T$
- **Observations**: $O = \{o_1, \dots, o_T\}$
- **Initial distribution**: $\pi_i = P(q_1 = s_i)$
- **Transition matrix**: $a_{ij} = P(q_t = s_j \mid q_{t-1} = s_i)$
- **Emission distribution**: $b_i(o) = P(o_t = o \mid q_t = s_i)$

Parameters: $\lambda = (\pi, A, B)$

## Three Fundamental Problems

### 1. Likelihood: Forward Algorithm
Compute $P(O|\lambda)$ efficiently using dynamic programming.

**Forward variable $\alpha_t(j) = P(o_1, \dots, o_t, q_t = s_j)$:**

1. Initialize: $\alpha_1(j) = \pi_j b_j(o_1)$
2. Recursion: $\alpha_{t+1}(j) = \left[ \sum_{i=1}^m \alpha_t(i) a_{ij} \right] b_j(o_{t+1})$
3. Terminate: $P(O|\lambda) = \sum_{j=1}^m \alpha_T(j)$

**Complexity**: $O(T m^2)$ vs naive $O(m^T)$.

**Backward variable $\beta_t(i) = P(o_{t+1}, \dots, o_T \mid q_t = s_i)$:**

1. Initialize: $\beta_T(i) = 1$
2. Recursion: $\beta_t(i) = \sum_{j=1}^m a_{ij} b_j(o_{t+1}) \beta_{t+1}(j)$

### 2. Decoding: Viterbi Algorithm
Find most likely state sequence $Q^* = \arg\max_Q P(Q|O, \lambda)$.

**Viterbi variable $\delta_t(j) = \max_{q_1, \dots, q_{t-1}} P(q_1, \dots, q_t = s_j, O|\lambda)$:**

1. Initialize: $\delta_1(j) = \pi_j b_j(o_1)$, $\psi_1(j) = 0$
2. Recursion: $\delta_t(j) = \max_i [\delta_{t-1}(i) a_{ij}] b_j(o_t)$, $\psi_t(j) = \arg\max_i [\delta_{t-1}(i) a_{ij}]$
3. Terminate: $P^* = \max_j \delta_T(j)$, $q^*_T = \arg\max_j \delta_T(j)$
4. Backtrack: $q^*_t = \psi_{t+1}(q^*_{t+1})$

### 3. Learning: Baum-Welch (EM)

**E-step**: Compute expected sufficient statistics:

$$\gamma_t(i) = P(q_t = s_i \mid O, \lambda) = \frac{\alpha_t(i) \beta_t(i)}{\sum_j \alpha_t(j) \beta_t(j)}$$

$$\xi_t(i,j) = P(q_t = s_i, q_{t+1} = s_j \mid O, \lambda) = \frac{\alpha_t(i) a_{ij} b_j(o_{t+1}) \beta_{t+1}(j)}{\sum_i \sum_j \alpha_t(i) a_{ij} b_j(o_{t+1}) \beta_{t+1}(j)}$$

**M-step**: Update parameters:

$$\hat{\pi}_i = \gamma_1(i)$$

$$\hat{a}_{ij} = \frac{\sum_{t=1}^{T-1} \xi_t(i,j)}{\sum_{t=1}^{T-1} \gamma_t(i)}$$

$$\hat{b}_j(k) = \frac{\sum_{t=1}^T \gamma_t(j) \cdot [o_t = k]}{\sum_{t=1}^T \gamma_t(j)} \quad \text{(discrete)}$$

## Scaling
Forward and backward variables underflow for long sequences. Use scaling coefficients $c_t$:

$$c_t = \frac{1}{\sum_i \alpha_t(i)}, \quad \hat{\alpha}_t(i) = c_t \alpha_t(i)$$

$$P(O|\lambda) = \frac{1}{\prod_{t=1}^T c_t}$$

## Code: Forward-Backward Algorithm

```python
import numpy as np

def forward(A, B, pi, obs):
    m, T = A.shape[0], len(obs)
    alpha = np.zeros((T, m))
    alpha[0] = pi * B[:, obs[0]]
    c = np.zeros(T)
    c[0] = 1.0 / np.sum(alpha[0])
    alpha[0] *= c[0]
    for t in range(1, T):
        alpha[t] = (alpha[t-1] @ A) * B[:, obs[t]]
        c[t] = 1.0 / np.sum(alpha[t])
        alpha[t] *= c[t]
    log_likelihood = -np.sum(np.log(c))
    return alpha, c, log_likelihood

def viterbi(A, B, pi, obs):
    m, T = A.shape[0], len(obs)
    delta = np.zeros((T, m))
    psi = np.zeros((T, m), dtype=int)
    delta[0] = np.log(pi) + np.log(B[:, obs[0]])
    for t in range(1, T):
        for j in range(m):
            scores = delta[t-1] + np.log(A[:, j]) + np.log(B[j, obs[t]])
            delta[t, j] = np.max(scores)
            psi[t, j] = np.argmax(scores)
    states = np.zeros(T, dtype=int)
    states[-1] = np.argmax(delta[-1])
    for t in range(T-2, -1, -1):
        states[t] = psi[t+1, states[t+1]]
    return states
```

## Practical Considerations
- **Numerical underflow**: Always use scaling or log-space for long sequences
- **Local maxima**: EM converges to local optimum — use multiple random restarts
- **Model selection**: BIC/AIC or cross-validated likelihood for choosing $m$
- **Sparse transitions**: Regularize $A$ with Dirichlet prior (add pseudocounts)
- **Non-stationary data**: Use input-output HMM or time-varying transitions

## Variants
- **Gaussian HMM**: $b_i(o) = \mathcal{N}(o; \mu_i, \Sigma_i)$
- **GMM-HMM**: Each state's emission is a GMM (common in speech recognition)
- **Autoregressive HMM (AR-HMM)**: $o_t$ depends on $o_{t-1}$ within a state
- **Factorial HMM**: Multiple state chains interact
- **Segmental HMM**: State duration modeled explicitly (explicit duration HMM)

## References
- Rabiner, "A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition" (IEEE Proc., 1989)
- Baum et al., "A Maximization Technique Occurring in the Statistical Analysis of Probabilistic Functions of Markov Chains" (Ann. Math. Stat., 1970)
- Viterbi, "Error Bounds for Convolutional Codes and an Asymptotically Optimum Decoding Algorithm" (IEEE Trans. Info. Theory, 1967)
- Bishop, "Pattern Recognition and Machine Learning", Ch. 13
