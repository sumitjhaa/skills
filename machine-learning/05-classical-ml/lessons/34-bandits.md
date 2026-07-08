# Lesson 05.34: Bandit Algorithms

## Learning Objectives
- Understand the exploration-exploitation dilemma
- Implement UCB, Thompson Sampling, and EXP3
- Analyze regret bounds for stochastic and adversarial settings
- Apply contextual bandits to personalization

## Multi-Armed Bandit
At each round $t = 1, \dots, T$:
1. Choose arm $a_t \in \{1, \dots, K\}$
2. Observe reward $r_t \in [0, 1]$
3. Goal: maximize cumulative reward $\sum_{t=1}^T r_t$

**Regret**: $\text{Regret}_T = \sum_{t=1}^T (\mu^* - \mu_{a_t})$, where $\mu^* = \max_i \mu_i$

## Algorithms

### $\varepsilon$-Greedy
- With probability $\varepsilon$: explore (random arm)
- With probability $1-\varepsilon$: exploit (current best arm)
- Decay: $\varepsilon_t = \min(1, cK / (d^2 t))$

Simple baseline. Optimal decay gives $O(T^{2/3})$ regret (not optimal for stationary data).

### UCB (Upper Confidence Bound)
Select arm with highest optimistic estimate:

$$a_t = \arg\max_i \left[ \hat{\mu}_i + \sqrt{\frac{2 \log t}{n_i}} \right]$$

- $\hat{\mu}_i$: empirical mean of arm $i$
- $n_i$: number of times arm $i$ pulled
- $\sqrt{2 \log t / n_i}$: confidence bonus (exploration bonus)

**Regret**: $O(\log T)$ — optimal up to constant factors.

**Intuition**: Arms are tried less often → wider confidence intervals → chosen more often until they prove suboptimal.

### Thompson Sampling (TS)
Bayesian approach:
1. Maintain posterior $P(\mu_i | \text{data})$ — typically $\text{Beta}(\alpha_i, \beta_i)$ for Bernoulli rewards
2. Sample $\tilde{\mu}_i \sim P(\mu_i | \text{data})$
3. Choose $a_t = \arg\max_i \tilde{\mu}_i$

**Properties**:
- Asymptotically optimal ($O(\log T)$ regret)
- Excellent empirical performance
- Naturally trades off exploration vs exploitation
- Generalizes to complex models (Bayesian linear regression)

### EXP3 (Exponential-weight for Exploration and Exploitation)
For adversarial bandits (no stochastic assumption):

$$p_i(t) = (1-\gamma) \frac{w_i(t)}{\sum_j w_j(t)} + \frac{\gamma}{K}$$

- $w_i(t+1) = w_i(t) \exp(\gamma \hat{r}_i(t) / K)$, $\hat{r}_i(t) = r_t / p_{a_t}(t)$ if $i = a_t$, else 0
- $\gamma \in (0,1)$ controls exploration

**Regret**: $O(\sqrt{TK \log K})$ — optimal for adversarial setting.

## Contextual Bandits
Reward depends on context $x_t$:

$$r_t = f(x_t, a_t) + \varepsilon_t$$

- **LinUCB**: Assume linear reward $r_t = x_t^\top \theta_a + \varepsilon_t$, UCB-style selection
- **Bayesian linear regression TS**: Sample $\tilde{\theta}_a$ from posterior, choose $a_t = \arg\max x_t^\top \tilde{\theta}_a$

**Widely used**: News article recommendation (choosing which article to show based on user features).

## Code: Thompson Sampling

```python
import numpy as np

class ThompsonSampling:
    def __init__(self, n_arms):
        self.n_arms = n_arms
        self.alpha = np.ones(n_arms)
        self.beta = np.ones(n_arms)

    def select_arm(self):
        samples = np.random.beta(self.alpha, self.beta)
        return np.argmax(samples)

    def update(self, arm, reward):
        if reward == 1:
            self.alpha[arm] += 1
        else:
            self.beta[arm] += 1
```

## Regret Bounds Summary

| Setting | Algorithm | Regret | Optimal? |
|---------|-----------|--------|----------|
| Stochastic, $K$ arms | UCB | $O(\log T)$ | Yes |
| Stochastic, $K$ arms | Thompson Sampling | $O(\log T)$ | Yes |
| Adversarial, $K$ arms | EXP3 | $O(\sqrt{TK \log K})$ | Yes |
| Stochastic, contextual | LinUCB | $O(d \sqrt{T})$ | Yes (minimax) |
| Adversarial, contextual | EXP4 | $O(\sqrt{T K \log K})$ | Yes |

## Practical Considerations
- **Non-stationary rewards**: Use sliding window or discount factor
- **Large arm sets**: Use hierarchical or tree-based approaches
- **Batch bandits**: Thompson sampling with delayed batch updates
- **Evaluation**: Use offline policy evaluation (inverse propensity scoring, doubly robust)
- **Metadata**: Store arm features for warm-starting new arms
- **Fairness**: Ensure exploration doesn't disproportionately affect certain groups

## Applications
- A/B testing (minimize cost of bad variants)
- Ad placement (which ad to show)
- Recommendation (which article/product to recommend)
- Clinical trials (adaptive patient assignment)
- Hyperparameter tuning (learning rate, architecture choices)

## References
- Thompson, "On the Likelihood that One Unknown Probability Exceeds Another" (Biometrika, 1933)
- Auer, Cesa-Bianchi, Fischer, "Finite-time Analysis of the Multiarmed Bandit Problem" (Machine Learning, 2002)
- Li et al., "A Contextual-Bandit Approach to Personalized News Article Recommendation" (WWW 2010)
- Chapelle & Li, "An Empirical Evaluation of Thompson Sampling" (NIPS 2011)
- Bubeck & Cesa-Bianchi, "Regret Analysis of Stochastic and Nonstochastic Multi-armed Bandit Problems" (Foundations and Trends in ML, 2012)
