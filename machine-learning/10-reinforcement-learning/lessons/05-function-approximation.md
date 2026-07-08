# Lesson 10.05: Function Approximation

## Learning Objectives
- Understand value function approximation with neural nets
- Implement DQN with experience replay and target network
- Apply double DQN, dueling DQN, and prioritized replay

## Linear Function Approximation

### Features
$$V(s; w) = w^\top x(s)$$

### Update
$$w \leftarrow w + \alpha [G_t - V(s; w)] \nabla V(s; w)$$
$$w \leftarrow w + \alpha \delta_t x(s)$$

## Neural Network Approximation

### DQN Architecture
```
State (84×84×4) → Conv(32,8,4) → Conv(64,4,2) → Conv(64,3,1) → FC(512) → FC(|A|)
```

## Experience Replay

### Buffer
```python
class ReplayBuffer:
    def __init__(self, capacity=100000):
        self.buffer = deque(maxlen=capacity)

    def add(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        return map(np.array, zip(*batch))
```

### Benefits
- Breaks temporal correlations in data
- Reuses experiences (sample efficiency)
- Smooths learning

## Target Network

### Fixed Target
$$Q(s, a; \theta) \leftarrow Q(s, a; \theta) + \alpha [r + \gamma \max_{a'} Q(s', a'; \theta^-) - Q(s, a; \theta)]$$

- $\theta^-$: target network (copied from $\theta$ every C=10K steps)
- Stabilizes training by reducing moving target problem

## Double DQN

### Decouple Action Selection and Evaluation
$$y = r + \gamma Q(s', \arg\max_{a'} Q(s', a'; \theta); \theta^-)$$

- Reduces overestimation bias of Q-learning

## Dueling DQN

### Architecture
$$Q(s, a) = V(s) + A(s, a) - \frac{1}{|A|} \sum_{a'} A(s, a')$$

- $V(s)$: state value stream
- $A(s, a)$: advantage stream
- Shared convolutional feature extractor

## Code: DQN Agent

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import deque
import random

class DQN(nn.Module):
    def __init__(self, n_obs, n_actions):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_obs, 256), nn.ReLU(),
            nn.Linear(256, 256), nn.ReLU(),
            nn.Linear(256, n_actions),
        )

    def forward(self, x):
        return self.net(x)

class DQNAgent:
    def __init__(self, state_dim, action_dim, lr=1e-4, gamma=0.99):
        self.q = DQN(state_dim, action_dim)
        self.target = DQN(state_dim, action_dim)
        self.target.load_state_dict(self.q.state_dict())
        self.optim = torch.optim.Adam(self.q.parameters(), lr=lr)
        self.gamma = gamma
        self.memory = deque(maxlen=100000)
        self.action_dim = action_dim

    def act(self, state, epsilon=0.1):
        if random.random() < epsilon:
            return random.randrange(self.action_dim)
        with torch.no_grad():
            q_values = self.q(torch.FloatTensor(state))
            return q_values.argmax().item()

    def update(self, batch_size=64):
        if len(self.memory) < batch_size:
            return
        batch = random.sample(self.memory, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)
        
        # Double DQN
        next_actions = self.q(next_states).argmax(1)
        next_q = self.target(next_states).gather(1, next_actions.unsqueeze(1)).squeeze()
        target = rewards + self.gamma * next_q * (1 - dones)
        current_q = self.q(states).gather(1, actions.unsqueeze(1)).squeeze()
        
        loss = F.mse_loss(current_q, target.detach())
        self.optim.zero_grad()
        loss.backward()
        self.optim.step()
```

## Rainbow DQN

### Integration of 6 Extensions
| Technique | Purpose |
|-----------|---------|
| Double DQN | Reduce overestimation |
| Prioritized Replay | Focus on important transitions |
| Dueling Network | Separate value and advantage |
| Multi-step Learning | N-step returns |
| Distributional RL | Learn return distribution |
| Noisy Nets | Exploration via noise |

## References
- Mnih, Kavukcuoglu, et al., "Human-level control through deep reinforcement learning (DQN)", Nature 2015
- Van Hasselt, Guez, Silver, "Deep Reinforcement Learning with Double Q-learning", AAAI 2016
- Wang, Schaul, et al., "Dueling Network Architectures for Deep Reinforcement Learning", ICML 2016
- Schaul, Quan, et al., "Prioritized Experience Replay", ICLR 2016
- Hessel, Modayil, et al., "Rainbow: Combining Improvements in Deep Reinforcement Learning", AAAI 2018
