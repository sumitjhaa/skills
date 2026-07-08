# Lesson 10.01: Markov Decision Process (MDP)

## Learning Objectives
- Understand MDP formalism for sequential decisions
- Implement value functions and Bellman equations
- Apply Markov property and state representations

## MDP Definition

### 5-Tuple
$$\langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$$

- $\mathcal{S}$: state space (finite or continuous)
- $\mathcal{A}$: action space
- $\mathcal{P}(s' \mid s, a)$: transition probability
- $\mathcal{R}(s, a)$: reward function
- $\gamma \in [0, 1)$: discount factor

### Markov Property
$$P(s_{t+1} \mid s_t, a_t) = P(s_{t+1} \mid s_0, a_0, \dots, s_t, a_t)$$

Future depends only on present, not past.

## Value Functions

### State-Value Function
$$V^\pi(s) = \mathbb{E}_\pi \left[ \sum_{k=0}^\infty \gamma^k R_{t+k+1} \mid S_t = s \right]$$

Expected discounted return starting from state $s$ following policy $\pi$.

### Action-Value Function
$$Q^\pi(s, a) = \mathbb{E}_\pi \left[ \sum_{k=0}^\infty \gamma^k R_{t+k+1} \mid S_t = s, A_t = a \right]$$

## Bellman Equations

### Bellman Expectation Equation
$$V^\pi(s) = \sum_{a} \pi(a \mid s) \sum_{s', r} p(s', r \mid s, a) [r + \gamma V^\pi(s')]$$

### Bellman Optimality Equation
$$V^*(s) = \max_{a} \sum_{s', r} p(s', r \mid s, a) [r + \gamma V^*(s')]$$

### Bellman Operator
$$(T^\pi V)(s) = \sum_{a} \pi(a \mid s) \sum_{s'} P(s' \mid s, a) [R(s, a) + \gamma V(s')]$$

Contraction mapping: $\|T^\pi V_1 - T^\pi V_2\|_\infty \leq \gamma \|V_1 - V_2\|_\infty$

## Code: MDP Transition

```python
import numpy as np

class MDP:
    def __init__(self, states, actions, transition, rewards, gamma=0.9):
        self.states = states
        self.actions = actions
        self.P = transition  # dict: (s, a) → [(prob, s', reward)]
        self.gamma = gamma

    def compute_value(self, policy, tol=1e-6):
        V = np.zeros(len(self.states))
        while True:
            delta = 0
            for s in self.states:
                v = V[s]
                V[s] = sum(policy[s][a] * sum(p * (r + self.gamma * V[s_next])
                            for p, s_next, r in self.P[s][a])
                           for a in self.actions)
                delta = max(delta, abs(v - V[s]))
            if delta < tol:
                break
        return V

    def bellman_optimality(self, tol=1e-6):
        V = np.zeros(len(self.states))
        while True:
            delta = 0
            for s in self.states:
                v = V[s]
                V[s] = max(sum(p * (r + self.gamma * V[s_next])
                            for p, s_next, r in self.P[s][a])
                           for a in self.actions)
                delta = max(delta, abs(v - V[s]))
            if delta < tol:
                break
        return V
```

## Types of RL Problems

| Type | MDP Known? | Approach |
|------|-----------|----------|
| Planning | Yes | DP, value iteration |
| Model-based RL | No (learn model) | Learn P, R then plan |
| Model-free RL | No | Directly learn V/Q/π |

## References
- Bellman, "A Markovian Decision Process", 1957
- Sutton & Barto, "Reinforcement Learning: An Introduction", 2018 (Ch. 3)
- Puterman, "Markov Decision Processes: Discrete Stochastic Dynamic Programming", 1994
