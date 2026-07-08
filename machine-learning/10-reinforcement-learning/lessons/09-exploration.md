# Lesson 10.09: Exploration

## Learning Objectives
- Understand exploration vs exploitation dilemma
- Implement UCB (Upper Confidence Bound) and Thompson sampling
- Apply intrinsic motivation and curiosity-driven exploration

## Exploration vs Exploitation

### Dilemma
- **Exploitation**: Choose best-known action (greedy)
- **Exploration**: Try unknown actions to gather information

## ε-Greedy

### Policy
$$\pi(a \mid s) = \begin{cases} 1 - \epsilon + \frac{\epsilon}{|\mathcal{A}|} & \text{if } a = \arg\max Q(s, a) \\ \frac{\epsilon}{|\mathcal{A}|} & \text{otherwise} \end{cases}$$

- Decay $\epsilon$ over time (e.g., 1.0 → 0.01)
- Simple but inefficient

## UCB (Upper Confidence Bound)

### Action Selection
$$a^* = \arg\max_a \left[ Q(a) + c \sqrt{\frac{\ln N}{n(a)}} \right]$$

- $Q(a)$: estimated value
- $N$: total plays, $n(a)$: plays of action $a$
- $c$: exploration coefficient

## Thompson Sampling

### Bayesian Approach
$$a^* \sim P(a \text{ is optimal} \mid \text{data})$$

- Maintain posterior distribution over Q-values
- Sample from posterior, choose max
- Natural exploration vs exploitation

## Intrinsic Motivation

### Curiosity
$$r^{\text{int}}(s, a) = \| \hat{\phi}(s') - \phi(s') \|_2^2$$

- Prediction error as intrinsic reward
- Visit novel states (high prediction error)
- Declining over training

### Random Network Distillation (RND)
$$r^{\text{int}}(s) = \| f_{\text{fixed}}(s) - f_\theta(s) \|_2^2$$

- Train predictor $f_\theta$ to match randomly initialized $f_{\text{fixed}}$
- Novel states have high prediction error

## Code: Exploration Strategies

```python
import numpy as np

class UCB1:
    def __init__(self, n_actions, c=2.0):
        self.counts = np.zeros(n_actions)
        self.values = np.zeros(n_actions)
        self.c = c
        self.total_plays = 0

    def select_action(self):
        self.total_plays += 1
        if len(self.counts) == 0:
            return np.random.randint(len(self.counts))
        # Select action with UCB
        ucb_values = self.values + self.c * np.sqrt(
            np.log(self.total_plays) / (self.counts + 1e-6)
        )
        return np.argmax(ucb_values)

    def update(self, action, reward):
        self.counts[action] += 1
        n = self.counts[action]
        self.values[action] += (reward - self.values[action]) / n


class ThompsonSampling:
    def __init__(self, n_actions):
        # Beta prior (alpha=1, beta=1)
        self.alphas = np.ones(n_actions)
        self.betas = np.ones(n_actions)

    def select_action(self):
        # Sample from posterior
        samples = np.random.beta(self.alphas, self.betas)
        return np.argmax(samples)

    def update(self, action, reward):
        if reward >= 0.5:  # Success
            self.alphas[action] += 1
        else:              # Failure
            self.betas[action] += 1
```

## Exploration Benchmarks

| Method | Regret (Bernoulli bandit, 1000 steps) | Parameters |
|--------|--------------------------------------|------------|
| ε-greedy (ε=0.1) | ~50 | ε |
| UCB (c=2) | ~30 | c |
| Thompson sampling | ~25 | Prior |
| Policy entropy bonus | — | β |
| RND | — | Predictor network |

## Practical Considerations
- **For deep RL**: Combine intrinsic + extrinsic rewards
- **Burn-in**: Use random actions for first N steps
- **Count-based**: Pseudo-counts for continuous state spaces
- **Population-based training**: Tune exploration hyperparameters automatically

## References
- Auer, Cesa-Bianchi, Fischer, "Finite-time Analysis of the Multiarmed Bandit Problem", 2002
- Thompson, "On the Likelihood that One Unknown Probability Exceeds Another in View of the Evidence of Two Samples", 1933
- Pathak, Agrawal, et al., "Curiosity-driven Exploration by Self-Supervised Prediction", ICML 2017
- Burda, Edwards, et al., "Exploration by Random Network Distillation", ICLR 2019
- Bellemare, Srinivasan, et al., "Unifying Count-Based Exploration and Intrinsic Motivation", NeurIPS 2016
