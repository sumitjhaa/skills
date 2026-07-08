# Lesson 10.11: Multi-Agent RL

## Learning Objectives
- Understand challenges in multi-agent RL (MARL)
- Implement independent Q-learning (IQL) and MADDPG
- Apply mean-field RL for large agent populations

## MARL Challenges

### Non-Stationarity
- Other agents' policies change → environment dynamics change
- Each agent's MDP is non-stationary

### Credit Assignment
- Which agent's actions contributed to the reward?
- Global reward vs individual reward

## Independent Q-Learning (IQL)

### Approach
Each agent learns its own Q-function independently, treating others as part of environment:

$$Q_i(s, a_i) \leftarrow Q_i(s, a_i) + \alpha [r_i + \gamma \max_{a'_i} Q_i(s', a'_i) - Q_i(s, a_i)]$$

## MADDPG (Multi-Agent DDPG)

### Centralized Critic, Decentralized Actors
- **Critic**: Uses all agents' observations and actions (centralized)
- **Actor**: Uses only local observation (decentralized)

### Critic Update
$$Q_i^\mu(X, a_1, \dots, a_N) = r_i + \gamma Q_i^{\mu'}(X', a'_1, \dots, a'_N)$$

### Actor Update
$$\nabla_{\theta_i} J(\mu_i) = \mathbb{E} \left[ \nabla_{\theta_i} \mu_i(a_i \mid o_i) \nabla_{a_i} Q_i^\mu(X, a_1, \dots, a_N) \right]$$

## Mean-Field RL

### Idea
For large populations, approximate joint action with mean action $\bar{a}$:

$$Q(s, a_i, \bar{a}_{-i}) \approx \mathbb{E}_{a_{-i} \sim \pi_{-i}} Q(s, a_i, a_{-i})$$

Mean action: $\bar{a} = \frac{1}{N-1} \sum_{j \neq i} a_j$

## Code: MADDPG Agent

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class MADDPGAgent:
    def __init__(self, obs_dim, act_dim, n_agents, agent_id, hidden=256):
        self.agent_id = agent_id
        self.actor = nn.Sequential(
            nn.Linear(obs_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, act_dim), nn.Tanh(),
        )
        # Critic takes all observations and actions
        self.critic = nn.Sequential(
            nn.Linear(obs_dim * n_agents + act_dim * n_agents, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, 1),
        )
        self.target_actor = self._copy(self.actor)
        self.target_critic = self._copy(self.critic)
        self.actor_optim = torch.optim.Adam(self.actor.parameters(), lr=1e-3)
        self.critic_optim = torch.optim.Adam(self.critic.parameters(), lr=1e-3)

    def _copy(self, net):
        copy = type(net)()
        copy.load_state_dict(net.state_dict())
        return copy

    def act(self, obs):
        obs = torch.FloatTensor(obs).unsqueeze(0)
        return self.actor(obs).detach().numpy()[0]

    def update_critic(self, all_obs, all_actions, rewards, next_all_obs, done, gamma=0.95):
        with torch.no_grad():
            next_actions = [self.target_actor(next_all_obs[:, i])
                           for i in range(len(next_all_obs[0]))]
            next_actions = torch.stack(next_actions, dim=1)
            next_q = self.target_critic(
                torch.cat([next_all_obs.view(1, -1), next_actions.view(1, -1)], dim=-1)
            )
            target = rewards + gamma * next_q * (1 - done)
        
        current_q = self.critic(
            torch.cat([all_obs.view(1, -1), all_actions.view(1, -1)], dim=-1)
        )
        critic_loss = F.mse_loss(current_q, target)
        self.critic_optim.zero_grad()
        critic_loss.backward()
        self.critic_optim.step()

    def update_actor(self, all_obs):
        actions = [self.actor(all_obs[:, i]) for i in range(len(all_obs[0]))]
        actions = torch.stack(actions, dim=1)
        actor_loss = -self.critic(
            torch.cat([all_obs.view(1, -1), actions.view(1, -1)], dim=-1)
        ).mean()
        self.actor_optim.zero_grad()
        actor_loss.backward()
        self.actor_optim.step()
```

## MARL Environments

| Environment | Agents | Action Space | Challenge |
|------------|--------|-------------|-----------|
| Multi-Agent Particle | 2-3 | Discrete | Simple coordination |
| StarCraft II (SMAC) | 5-27 | Discrete | Micro-management |
| Hanabi | 2-4 | Discrete | Cooperation |
| RoboCup | 2-11 | Continuous | Team coordination |
| MPE (Spread/Predator) | 2-3 | Continuous | Mixed cooperative-competitive |

## References
- Tan, "Multi-Agent Reinforcement Learning: Independent vs. Cooperative Agents", ICML 1993
- Lowe, Wu, et al., "Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments (MADDPG)", NeurIPS 2017
- Yang, Luo, et al., "Mean Field Multi-Agent Reinforcement Learning", ICML 2018
- Rashid, Samvelyan, et al., "QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning", ICML 2018
- Samvelyan, Rashid, et al., "The StarCraft Multi-Agent Challenge (SMAC)", 2019
