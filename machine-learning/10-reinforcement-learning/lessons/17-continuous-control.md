# Lesson 10.17: Continuous Control

## Learning Objectives
- Understand continuous action spaces in RL
- Implement DDPG (Deep Deterministic Policy Gradient)
- Apply TD3 (Twin Delayed DDPG)

## Continuous Action Spaces

### Challenge
- Action $a \in \mathbb{R}^n$ (not discrete)
- Cannot take max over Q-values
- Need actor-critic approach

## DDPG (Deep Deterministic Policy Gradient)

### Actor-Critic for Continuous Actions
- **Actor**: $\mu(s) \to a \in \mathbb{R}^n$ (deterministic policy)
- **Critic**: $Q(s, a) \to \mathbb{R}$ (action-value function)

### Critic Update
$$y = r + \gamma Q_{\theta^-}(s', \mu_{\phi^-}(s'))$$
$$\mathcal{L}_Q = (Q_\theta(s, a) - y)^2$$

### Actor Update
$$\nabla_\phi J = \mathbb{E}[\nabla_a Q_\theta(s, a) \nabla_\phi \mu_\phi(s)]$$

### Exploration
Add noise to actions during training: $a_t = \mu(s_t) + \mathcal{N}_t$

## TD3 (Twin Delayed DDPG)

### Three Improvements
1. **Clipped double Q-learning**: Two critics, take min
2. **Delayed policy updates**: Update actor every 2 critic steps
3. **Target policy smoothing**: Add noise to target actions

### Target Policy Smoothing
$$a' = \mu_{\phi^-}(s') + \text{clip}(\mathcal{N}(0, \sigma), -c, c)$$

## Code: TD3 Agent

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class TD3:
    def __init__(self, state_dim, action_dim, max_action, hidden=256):
        self.actor = nn.Sequential(
            nn.Linear(state_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, action_dim), nn.Tanh(),
        )
        self.actor_target = self._copy(self.actor)
        self.actor_optim = torch.optim.Adam(self.actor.parameters(), lr=3e-4)

        self.critic1 = nn.Sequential(
            nn.Linear(state_dim + action_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, 1),
        )
        self.critic2 = nn.Sequential(
            nn.Linear(state_dim + action_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, 1),
        )
        self.critic1_target = self._copy(self.critic1)
        self.critic2_target = self._copy(self.critic2)
        self.critic_optim = torch.optim.Adam(
            list(self.critic1.parameters()) + list(self.critic2.parameters()), lr=3e-4
        )
        self.max_action = max_action
        self.total_it = 0

    def _copy(self, net):
        copy = type(net)()
        copy.load_state_dict(net.state_dict())
        return copy

    def act(self, state):
        state = torch.FloatTensor(state).unsqueeze(0)
        return self.actor(state).detach().numpy()[0]

    def update(self, replay_buffer, batch_size=256, gamma=0.99, tau=0.005, policy_noise=0.2, noise_clip=0.5, policy_delay=2):
        self.total_it += 1
        states, actions, rewards, next_states, dones = replay_buffer.sample(batch_size)
        states = torch.FloatTensor(states)
        actions = torch.FloatTensor(actions)
        rewards = torch.FloatTensor(rewards).unsqueeze(1)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones).unsqueeze(1)

        with torch.no_grad():
            noise = (torch.randn_like(actions) * policy_noise).clamp(-noise_clip, noise_clip)
            next_actions = (self.actor_target(next_states) + noise).clamp(-1, 1)
            target_q1 = self.critic1_target(torch.cat([next_states, next_actions], 1))
            target_q2 = self.critic2_target(torch.cat([next_states, next_actions], 1))
            target_q = torch.min(target_q1, target_q2)
            target = rewards + gamma * target_q * (1 - dones)

        current_q1 = self.critic1(torch.cat([states, actions], 1))
        current_q2 = self.critic2(torch.cat([states, actions], 1))
        critic_loss = F.mse_loss(current_q1, target) + F.mse_loss(current_q2, target)

        self.critic_optim.zero_grad()
        critic_loss.backward()
        self.critic_optim.step()

        if self.total_it % policy_delay == 0:
            actor_loss = -self.critic1(torch.cat([states, self.actor(states)], 1)).mean()
            self.actor_optim.zero_grad()
            actor_loss.backward()
            self.actor_optim.step()

            for param, target_param in zip(self.actor.parameters(), self.actor_target.parameters()):
                target_param.data.copy_(tau * param.data + (1 - tau) * target_param.data)
            for param, target_param in zip(self.critic1.parameters(), self.critic1_target.parameters()):
                target_param.data.copy_(tau * param.data + (1 - tau) * target_param.data)
            for param, target_param in zip(self.critic2.parameters(), self.critic2_target.parameters()):
                target_param.data.copy_(tau * param.data + (1 - tau) * target_param.data)
```

## Continuous Control Benchmarks

| Algorithm | HalfCheetah-v2 | Hopper-v2 | Walker2d-v2 | Ant-v2 | Humanoid-v2 |
|-----------|---------------|-----------|-------------|--------|-------------|
| DDPG | 4679 | 1913 | 1637 | 1640 | 463 |
| TD3 | 9637 | 3378 | 4356 | 4752 | 1448 |
| SAC | 10886 | 3528 | 4920 | 5557 | 3371 |
| PPO | 4208 | 2369 | 2997 | 3147 | 980 |

## Practical Considerations
- **Action scaling**: Normalise action space to [-1, 1] for tanh output
- **Observation normalisation**: Running mean/std for state inputs
- **Replay buffer size**: 1M transitions typical
- **Exploration noise**: Gaussian noise, decay over training

## References
- Lillicrap, Hunt, et al., "Continuous Control with Deep Reinforcement Learning (DDPG)", ICLR 2016
- Fujimoto, van Hoof, Meger, "Addressing Function Approximation Error in Actor-Critic Methods (TD3)", ICML 2018
- Haarnoja, Zhou, et al., "Soft Actor-Critic: Off-Policy Maximum Entropy Deep RL with a Stochastic Actor", ICML 2018
- Schulman, Wolski, et al., "Proximal Policy Optimization Algorithms", 2017
