# Lesson 10.07: Advanced Actor-Critic

## Learning Objectives
- Understand PPO (Proximal Policy Optimization)
- Implement TRPO (Trust Region Policy Optimization)
- Apply SAC (Soft Actor-Critic) for maximum entropy RL

## PPO (Proximal Policy Optimization)

### Clipped Objective
$$\mathcal{L}^{\text{CLIP}}(\theta) = \mathbb{E}_t \left[ \min\left( r_t(\theta) A_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) A_t \right) \right]$$

- $r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\text{old}}}(a_t \mid s_t)}$
- $\epsilon = 0.2$: clipping hyperparameter

### Combined Loss
$$\mathcal{L}^{\text{PPO}}(\theta) = \mathbb{E}_t \left[ \mathcal{L}^{\text{CLIP}} - c_1 \mathcal{L}^{\text{VF}} + c_2 S[\pi_\theta](s_t) \right]$$

- $\mathcal{L}^{\text{VF}}$: value function loss (MSE)
- $S$: entropy bonus for exploration

## TRPO (Trust Region Policy Optimization)

### Constraint
$$\max_\theta \mathbb{E}_t \left[ \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\text{old}}}(a_t \mid s_t)} A_t \right]$$
$$\text{s.t. } \mathbb{E}_t [\text{KL}(\pi_{\theta_{\text{old}}}(\cdot \mid s_t) \| \pi_\theta(\cdot \mid s_t))] \leq \delta$$

- Natural gradient: $F^{-1} g$
- $\delta$: trust region size

## SAC (Soft Actor-Critic)

### Maximum Entropy Objective
$$J(\pi) = \sum_t \mathbb{E}_{(s_t, a_t) \sim \rho_\pi} [r(s_t, a_t) + \alpha \mathcal{H}(\pi(\cdot \mid s_t))]$$

- Entropy bonus $\alpha \mathcal{H}(\pi(\cdot \mid s))$ encourages exploration
- Soft policy iteration with temperature $\alpha$

### Critic Update (Soft Q)
$$Q(s, a) = r + \gamma (Q(s', a') - \alpha \log \pi(a' \mid s'))$$

### Policy Update
$$\pi^* = \arg\max_\pi \mathbb{E}_{a \sim \pi} [Q(s, a) - \alpha \log \pi(a \mid s)]$$

## Code: PPO Agent

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Normal

class PPOAgent:
    def __init__(self, state_dim, action_dim, lr=3e-4, gamma=0.99, clip=0.2):
        self.actor = nn.Sequential(
            nn.Linear(state_dim, 256), nn.Tanh(),
            nn.Linear(256, 256), nn.Tanh(),
            nn.Linear(256, action_dim),
        )
        self.critic = nn.Sequential(
            nn.Linear(state_dim, 256), nn.Tanh(),
            nn.Linear(256, 256), nn.Tanh(),
            nn.Linear(256, 1),
        )
        self.optim = torch.optim.Adam(
            list(self.actor.parameters()) + list(self.critic.parameters()), lr=lr
        )
        self.gamma = gamma
        self.clip = clip

    def act(self, state):
        state = torch.FloatTensor(state).unsqueeze(0)
        mean = self.actor(state)
        action = torch.tanh(mean).detach().numpy()[0]
        return action

    def compute_gae(self, rewards, values, dones):
        gae = 0
        returns = []
        for t in reversed(range(len(rewards))):
            if t == len(rewards) - 1:
                next_value = 0 if dones[t] else values[t + 1]
            else:
                next_value = 0 if dones[t] else values[t + 1]
            delta = rewards[t] + self.gamma * next_value - values[t]
            gae = delta + self.gamma * 0.95 * gae * (1 - dones[t])
            returns.insert(0, gae + values[t])
        return returns

    def update(self, states, actions, old_probs, advantages, returns):
        states = torch.FloatTensor(states)
        actions = torch.FloatTensor(actions)
        old_probs = torch.FloatTensor(old_probs)
        advantages = torch.FloatTensor(advantages)
        returns = torch.FloatTensor(returns)
        
        new_means = self.actor(states)
        new_probs = torch.tanh(new_means)
        ratio = (new_probs - old_probs).abs() + 1
        
        # Clipped PG
        pg_loss1 = -ratio * advantages
        pg_loss2 = -torch.clamp(ratio, 1 - self.clip, 1 + self.clip) * advantages
        pg_loss = torch.max(pg_loss1, pg_loss2).mean()
        
        # Value loss
        values = self.critic(states).squeeze()
        vf_loss = F.mse_loss(values, returns)
        
        loss = pg_loss + 0.5 * vf_loss
        self.optim.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(
            list(self.actor.parameters()) + list(self.critic.parameters()), 0.5
        )
        self.optim.step()
```

## Algorithm Properties

| Algorithm | Trust Region | Entropy | Sample Efficient | Continuous Action |
|-----------|-------------|---------|-----------------|-------------------|
| TRPO | Yes (KL) | No | High | Yes |
| PPO | Yes (clip) | Optional | High | Yes |
| SAC | No | Yes (tuned) | Very high | Yes |
| DDPG | No | No | Medium | Yes |
| TD3 | No | No | High | Yes |

## References
- Schulman, Levine, et al., "Trust Region Policy Optimization", ICML 2015
- Schulman, Wolski, et al., "Proximal Policy Optimization Algorithms", 2017
- Haarnoja, Zhou, et al., "Soft Actor-Critic: Off-Policy Maximum Entropy Deep RL with a Stochastic Actor", ICML 2018
- Fujimoto, van Hoof, Meger, "Addressing Function Approximation Error in Actor-Critic Methods (TD3)", ICML 2018
