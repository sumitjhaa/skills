# Lesson 10.04: Temporal-Difference Learning

## Learning Objectives
- Understand TD learning and TD(0)
- Implement SARSA (on-policy) and Q-learning (off-policy)
- Apply eligibility traces and TD(λ)

## TD(0)

### Update Rule
$$V(s_t) \leftarrow V(s_t) + \alpha [r_{t+1} + \gamma V(s_{t+1}) - V(s_t)]$$

- Bootstraps from current estimate (like DP)
- Samples reward and transition (like MC)
- Lower variance than MC, some bias

## SARSA (On-Policy TD Control)

### Update
$$Q(s, a) \leftarrow Q(s, a) + \alpha [r + \gamma Q(s', a') - Q(s, a)]$$

- Uses next action $a'$ from current policy
- Learns action-value for behaviour policy

## Q-Learning (Off-Policy TD Control)

### Update
$$Q(s, a) \leftarrow Q(s, a) + \alpha [r + \gamma \max_{a'} Q(s', a') - Q(s, a)]$$

- Uses max over next actions (greedy, not behaviour)
- Learns optimal Q* regardless of behaviour policy
- More sample-efficient than SARSA

## TD(λ) with Eligibility Traces

### Eligibility Trace
$$e_t(s) = \begin{cases} 1 & \text{if } s = s_t \\ \gamma \lambda e_{t-1}(s) & \text{otherwise} \end{cases}$$

### Update (Backward View)
$$\Delta V(s) = \alpha \delta_t e_t(s)$$

- $\delta_t = r_{t+1} + \gamma V(s_{t+1}) - V(s_t)$
- $\lambda = 0$: TD(0), $\lambda = 1$: MC

## Code: Q-Learning Agent

```python
import numpy as np

class QLearningAgent:
    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.Q = np.zeros((n_states, n_actions))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def act(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.Q.shape[1])
        return np.argmax(self.Q[state])

    def update(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target += self.gamma * np.max(self.Q[next_state])
        self.Q[state, action] += self.alpha * (target - self.Q[state, action])

    def train(self, env, episodes=1000):
        rewards = []
        for _ in range(episodes):
            state = env.reset()
            total_reward = 0
            done = False
            while not done:
                action = self.act(state)
                next_state, reward, done = env.step(action)
                self.update(state, action, reward, next_state, done)
                total_reward += reward
                state = next_state
            rewards.append(total_reward)
        return rewards


class SarsaAgent(QLearningAgent):
    def update(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            next_action = self.act(next_state)  # on-policy: use epsilon-greedy
            target += self.gamma * self.Q[next_state, next_action]
        self.Q[state, action] += self.alpha * (target - self.Q[state, action])
```

## Algorithm Comparison

| Algorithm | Type | Update Target | Bias | Variance |
|-----------|------|--------------|------|----------|
| MC | Offline | $G_t$ | Low | High |
| TD(0) | Online | $r + \gamma V(s')$ | Some | Low |
| TD(λ) | Online | λ-return | Moderate | Moderate |
| SARSA | On-policy | $r + \gamma Q(s', a')$ | Some | Low |
| Q-learning | Off-policy | $r + \gamma \max Q(s', a')$ | Some | Low |

## Cliff Walking Example
- Q-learning learns optimal path (along cliff edge)
- SARSA learns safe path (away from cliff)
- Q-learning takes more risk during exploration

## References
- Sutton, "Learning to Predict by the Methods of Temporal Differences", 1988
- Watkins & Dayan, "Q-Learning", 1992
- Rummery & Niranjan, "On-Line Q-Learning Using Connectionist Systems (SARSA)", 1994
- Sutton & Barto, "Reinforcement Learning: An Introduction", 2018 (Ch. 6-7)
