# Lesson 10.10: Offline RL

## Learning Objectives
- Understand offline (batch) RL challenges
- Implement Conservative Q-Learning (CQL)
- Apply Implicit Q-Learning (IQL)

## Offline RL Problem

### Distribution Shift
- Learning policy $\pi$ produces different state-action distribution than behaviour policy $\pi_\beta$
- OOD actions have overestimated Q-values
- Policy exploits Q-function errors

### Challenges
- No environment interaction
- Cannot correct OOD errors
- Extrapolation error in Q-values

## Conservative Q-Learning (CQL)

### Conservative Objective
$$\mathcal{L}_{\text{CQL}} = \alpha \mathbb{E}_{s \sim D} \left[ \log \sum_a \exp(Q(s, a)) - \mathbb{E}_{a \sim D} [Q(s, a)] \right]$$

- Minimise Q for OOD actions (first term)
- Maximise Q for in-distribution actions (second term)

### Total Loss
$$\mathcal{L} = \mathcal{L}_{\text{TD}} + \mathcal{L}_{\text{CQL}}$$

## IQL (Implicit Q-Learning)

### Approach
- Avoid querying OOD actions entirely
- Use expectile regression for value function:
  $$L(\tau, u) = |\tau - \mathbb{1}(u < 0)| \cdot u^2$$
- $\tau > 0.5$: quantile regression learns upper expectile

### Value Function
$$V(s) = \arg\min_V \mathbb{E}_{(s, a) \sim D} [L(\tau, Q_{\hat{\theta}}(s, a) - V(s))]$$

### Policy
$$\pi(s) = \arg\max_\pi \mathbb{E}_{a \sim \pi} [Q(s, a)]$$

## BCQ (Batch-Constrained Q-Learning)

### Perturbation Model
$$a = G(s) + \xi(s, \Phi)$$

- $G$: conditional VAE (generates actions)
- $\xi$: perturbation network (small adjustment)
- Clamp perturbation to stay near behaviour

## Code: CQL Agent

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class CQLAgent(nn.Module):
    def __init__(self, state_dim, action_dim, hidden=256, alpha=1.0):
        super().__init__()
        self.q1 = nn.Sequential(
            nn.Linear(state_dim + action_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, 1),
        )
        self.q2 = nn.Sequential(
            nn.Linear(state_dim + action_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, 1),
        )
        self.alpha = alpha

    def cql_loss(self, q_pred, states, actions):
        # Log-sum-exp for all actions (approximate)
        random_actions = torch.randn_like(actions)
        q_random = self.q1(torch.cat([states, random_actions], dim=-1))
        logsumexp = torch.logsumexp(q_random, dim=0)
        
        # In-distribution Q
        q_in = q_pred.mean()
        
        return self.alpha * (logsumexp - q_in)

    def td_loss(self, states, actions, rewards, next_states, dones, gamma=0.99):
        q_pred = self.q1(torch.cat([states, actions], dim=-1))
        with torch.no_grad():
            next_actions = self.sample_actions(next_states)
            next_q = torch.min(
                self.q1(torch.cat([next_states, next_actions], dim=-1)),
                self.q2(torch.cat([next_states, next_actions], dim=-1)),
            )
            td_target = rewards + gamma * next_q * (1 - dones)
        return F.mse_loss(q_pred, td_target)
```

## Offline RL Benchmarks

| Algorithm | D4RL Gym-MuJoCo (average) | D4RL AntMaze | Atari |
|-----------|--------------------------|-------------|-------|
| BC | 28.0 | 0.0 | 0.10 |
| CQL | 53.0 | 0.62 | 0.58 |
| IQL | 54.0 | 0.65 | 0.45 |
| DT (Decision Transformer) | 42.0 | 0.53 | — |
| TD3+BC | 48.0 | 0.43 | — |

## Practical Considerations
- **Dataset quality**: Mix of good and bad trajectories matters
- **α tuning**: CQL α = 0.5-5.0 typical (higher = more conservative)
- **Normalisation**: Normalise states/rewards for stable training
- **Evaluation**: Cannot trust Q-values for policy selection (use offline evaluation)

## References
- Kumar, Zhou, et al., "Conservative Q-Learning for Offline Reinforcement Learning", NeurIPS 2020
- Kostrikov, Nair, Levine, "Offline Reinforcement Learning with Implicit Q-Learning", ICLR 2022
- Fujimoto, Meger, Precup, "Off-Policy Deep Reinforcement Learning without Exploration (BCQ)", ICML 2019
- Fu, Kumar, et al., "D4RL: Datasets for Deep Data-Driven Reinforcement Learning", 2020
- Chen, Lu, et al., "Decision Transformer: Reinforcement Learning via Sequence Modeling", NeurIPS 2021
