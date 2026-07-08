# Lesson 10.03: Monte Carlo Methods

## Learning Objectives
- Understand Monte Carlo prediction and control
- Implement first-visit and every-visit MC
- Apply exploring starts and epsilon-soft policies

## Monte Carlo Prediction

### First-Visit MC
Average returns only for first visit to each state in an episode:

$$V(s) \leftarrow V(s) + \alpha (G_t - V(s))$$

### Every-Visit MC
Average returns for every visit to each state.

### Return
$$G_t = \sum_{k=0}^{T-t-1} \gamma^k R_{t+k+1}$$

## Monte Carlo Control

### MC Exploring Starts
```
Initialize π, Q arbitrarily
Repeat:
    Generate episode with exploring starts
    For each (s, a) in episode:
        G = return following first visit to (s, a)
        Q(s, a) = average of returns
    π(s) = argmax_a Q(s, a)
```

### On-Policy MC Control (ε-soft)
Use ε-greedy policy for both behaviour and target.

## Code: First-Visit MC Prediction

```python
import numpy as np
from collections import defaultdict

def mc_prediction(env, policy, num_episodes=5000, gamma=0.9):
    returns = defaultdict(list)
    V = defaultdict(float)
    
    for _ in range(num_episodes):
        episode = []
        state = env.reset()
        done = False
        while not done:
            action = policy(state)
            next_state, reward, done = env.step(action)
            episode.append((state, action, reward))
            state = next_state
        
        # First-visit MC
        visited = set()
        G = 0
        for t in range(len(episode) - 1, -1, -1):
            state, _, reward = episode[t]
            G = gamma * G + reward
            if state not in visited:
                visited.add(state)
                returns[state].append(G)
                V[state] = np.mean(returns[state])
    
    return V

def mc_control_epsilon_soft(env, num_episodes=10000, gamma=0.9, epsilon=0.1):
    nA = env.action_space.n
    nS = env.observation_space.n
    Q = np.zeros((nS, nA))
    returns = defaultdict(list)
    policy = np.ones((nS, nA)) / nA
    
    for _ in range(num_episodes):
        episode = []
        state = env.reset()
        done = False
        while not done:
            action = np.random.choice(nA, p=policy[state])
            next_state, reward, done = env.step(action)
            episode.append((state, action, reward))
            state = next_state
        
        visited = set()
        G = 0
        for t in range(len(episode) - 1, -1, -1):
            state, action, reward = episode[t]
            G = gamma * G + reward
            if (state, action) not in visited:
                visited.add((state, action))
                returns[(state, action)].append(G)
                Q[state, action] = np.mean(returns[(state, action)])
                # ε-greedy update
                best_action = np.argmax(Q[state])
                policy[state] = np.ones(nA) * epsilon / nA
                policy[state, best_action] += 1 - epsilon
    
    return Q, policy
```

## Properties

| Aspect | First-Visit MC | Every-Visit MC |
|--------|---------------|----------------|
| Bias | Unbiased | Biased |
| Variance | Lower | Higher |
| Convergence | Almost surely | Almost surely |

## Advantages over DP
- No model required (learn from experience)
- Can focus on relevant states
- Unbiased estimates

## References
- Sutton & Barto, "Reinforcement Learning: An Introduction", 2018 (Ch. 5)
- Rubinstein, "Simulation and the Monte Carlo Method", 1981
- Metropolis & Ulam, "The Monte Carlo Method", 1949
