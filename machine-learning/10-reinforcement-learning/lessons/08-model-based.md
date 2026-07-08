# Lesson 10.08: Model-Based RL

## Learning Objectives
- Understand model learning and planning with learned models
- Implement Dyna-Q (model-based + model-free)
- Apply MuZero (learned model without reward)

## Model Learning

### Learn Transition and Reward
$$\hat{P}(s' \mid s, a) \quad \text{and} \quad \hat{R}(s, a)$$

### Model Architecture
$s_{t+1} = f_\theta(s_t, a_t)$ — neural network predicting next state and reward.

## Dyna-Q

### Algorithm
```
Initialize Q(s, a), Model(s, a)
Repeat:
    s = current state
    a = policy from Q (ε-greedy)
    Execute a, observe r, s'
    Q(s, a) ← Q(s, a) + α[r + γ max Q(s', a') - Q(s, a)]
    Model(s, a) ← (r, s')  # Store in model
    Repeat N times:
        s_rand = random past state
        a_rand = random past action
        (r_pred, s'_pred) = Model(s_rand, a_rand)
        Q(s_rand, a_rand) ← update with (r_pred, s'_pred)
```

## MuZero

### Learned Model Without Reward
MuZero learns three functions:
1. **Representation**: $h(s_t) \to z_t$ (encode observation to hidden state)
2. **Dynamics**: $g(z_t, a_t) \to z_{t+1}, r_t$ (predict next state and reward)
3. **Prediction**: $f(z_t) \to \pi_t, v_t$ (policy and value from hidden state)

### Monte Carlo Tree Search (MCTS)
Use learned model for tree search:
1. Select leaf using UCB
2. Expand leaf using dynamics function
3. Backup values
4. Sample action from search policy

## Code: Dyna-Q

```python
import numpy as np
from collections import defaultdict

class DynaQ:
    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.95, epsilon=0.1, n_plan=5):
        self.Q = np.zeros((n_states, n_actions))
        self.model = {}  # (s, a) → (r, s')
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.n_plan = n_plan

    def act(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.Q.shape[1])
        return np.argmax(self.Q[state])

    def update(self, state, action, reward, next_state):
        # Q-learning update
        td_target = reward + self.gamma * np.max(self.Q[next_state])
        self.Q[state, action] += self.alpha * (td_target - self.Q[state, action])

        # Update model
        self.model[(state, action)] = (reward, next_state)

        # Planning
        for _ in range(self.n_plan):
            (s, a), (r, s_next) = self.sample_from_model()
            td_target = r + self.gamma * np.max(self.Q[s_next])
            self.Q[s, a] += self.alpha * (td_target - self.Q[s, a])

    def sample_from_model(self):
        idx = np.random.randint(len(self.model))
        return list(self.model.items())[idx]

    def train(self, env, episodes=100):
        rewards = []
        for _ in range(episodes):
            state = env.reset()
            total = 0
            done = False
            while not done:
                action = self.act(state)
                next_state, reward, done = env.step(action)
                self.update(state, action, reward, next_state)
                total += reward
                state = next_state
            rewards.append(total)
        return rewards
```

## Planning vs Learning

| Aspect | Dyna-Q | MuZero | Dreamer |
|--------|-------|--------|---------|
| Model | Tabular | Neural network | World model |
| Planning | Q-planning | MCTS | Latent imagination |
| Sample efficiency | Good | Excellent | Excellent |
| Scalability | Discrete | Discrete/cont. | Continuous |

## References
- Sutton, "Integrated Architectures for Learning, Planning, and Reacting Based on Approximating Dynamic Programming", ICML 1990
- Schrittwieser, Antonoglou, et al., "Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model (MuZero)", Nature 2020
- Hafner, Lillicrap, et al., "Dream to Control: Learning Behaviors by Latent Imagination (Dreamer)", ICLR 2020
- Silver, Schrittwieser, et al., "Mastering the Game of Go without Human Knowledge", Nature 2017
