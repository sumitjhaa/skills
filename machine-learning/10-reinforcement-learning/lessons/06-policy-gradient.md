# Lesson 10.06: Policy Gradient

## Learning Objectives
- Understand policy gradient theorem
- Implement REINFORCE (Monte Carlo policy gradient)
- Apply actor-critic methods (A2C, A3C)

## Policy Gradient Theorem

### Objective
$$J(\theta) = \mathbb{E}_{\pi_\theta} \left[ \sum_{t} \gamma^t R_t \right]$$

### Gradient
$$\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta} \left[ \nabla_\theta \log \pi_\theta(a \mid s) Q^\pi(s, a) \right]$$

- No derivative of state distribution needed
- Use $Q^\pi$ or return $G_t$ as estimate

## REINFORCE (Monte Carlo PG)

### Update
$$\theta \leftarrow \theta + \alpha \gamma^t G_t \nabla_\theta \log \pi_\theta(a_t \mid s_t)$$

- $G_t$: Monte Carlo return from step $t$
- High variance (uses full episode return)

## Actor-Critic

### Architecture
- **Actor**: Policy $\pi_\theta(a \mid s)$ — updates using critic's feedback
- **Critic**: Value function $V_\phi(s)$ — estimates expected return

### Advantage Actor-Critic (A2C)
$$\nabla_\theta J(\theta) = \mathbb{E} \left[ \nabla_\theta \log \pi_\theta(a \mid s) A(s, a) \right]$$

- $A(s, a) = Q(s, a) - V(s)$: advantage
- $A(s, a) \approx r + \gamma V(s') - V(s)$: TD error as advantage estimate

## A3C (Asynchronous Advantage Actor-Critic)

### Parallel Workers
- Multiple agents collect experience in parallel
- Each worker asynchronously updates shared parameters
- Workers communicate with global network via gradients

## Code: REINFORCE and A2C

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class PolicyNetwork(nn.Module):
    def __init__(self, state_dim, action_dim, hidden=128):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
        )
        self.action_head = nn.Linear(hidden, action_dim)
        self.value_head = nn.Linear(hidden, 1)

    def forward(self, x):
        x = self.fc(x)
        action_probs = F.softmax(self.action_head(x), dim=-1)
        value = self.value_head(x)
        return action_probs, value

class REINFORCE:
    def __init__(self, state_dim, action_dim, lr=1e-3, gamma=0.99):
        self.policy = PolicyNetwork(state_dim, action_dim)
        self.optim = torch.optim.Adam(self.policy.parameters(), lr=lr)
        self.gamma = gamma

    def act(self, state):
        state = torch.FloatTensor(state).unsqueeze(0)
        probs, _ = self.policy(state)
        action = torch.multinomial(probs, 1).item()
        return action, probs[0, action]

    def update(self, episode):
        returns = []
        G = 0
        for _, _, reward in reversed(episode):
            G = reward + self.gamma * G
            returns.insert(0, G)
        returns = torch.FloatTensor(returns)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)
        
        loss = 0
        for (state, action, _), G in zip(episode, returns):
            state = torch.FloatTensor(state).unsqueeze(0)
            probs, _ = self.policy(state)
            loss -= torch.log(probs[0, action] + 1e-10) * G
        
        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

class A2CAgent:
    def __init__(self, state_dim, action_dim, lr=1e-3, gamma=0.99):
        self.net = PolicyNetwork(state_dim, action_dim)
        self.optim = torch.optim.Adam(self.net.parameters(), lr=lr)
        self.gamma = gamma

    def update(self, state, action, reward, next_state, done):
        state = torch.FloatTensor(state).unsqueeze(0)
        next_state = torch.FloatTensor(next_state).unsqueeze(0)
        action = torch.LongTensor([action])
        reward = torch.FloatTensor([reward])
        done = torch.FloatTensor([done])
        
        probs, value = self.net(state)
        _, next_value = self.net(next_state)
        
        # TD target
        td_target = reward + self.gamma * next_value * (1 - done)
        advantage = (td_target - value).detach()
        
        # Actor loss: -log π(a|s) * A
        actor_loss = -torch.log(probs.gather(1, action.unsqueeze(1)) + 1e-10) * advantage
        # Critic loss: MSE(V - target)
        critic_loss = F.mse_loss(value, td_target.detach())
        
        loss = actor_loss + 0.5 * critic_loss
        self.optim.zero_grad()
        loss.backward()
        self.optim.step()
```

## Algorithm Properties

| Algorithm | Type | Variance | Bias | Use |
|-----------|------|----------|------|-----|
| REINFORCE | Monte Carlo PG | High | Low | Episodic tasks |
| A2C | Actor-critic | Medium | Some | Continuous control |
| A3C | Async A2C | Medium | Some | Parallel environments |
| PPO | Trust region PG | Low | Some | Stabilised training |

## References
- Williams, "Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning (REINFORCE)", 1992
- Sutton, McAllester, et al., "Policy Gradient Methods for Reinforcement Learning with Function Approximation", NeurIPS 1999
- Mnih, Badia, et al., "Asynchronous Methods for Deep Reinforcement Learning (A3C)", ICML 2016
- Schulman, Wolski, et al., "Proximal Policy Optimization Algorithms", 2017
