# Lesson 10.13: Hierarchical RL

## Learning Objectives
- Understand hierarchical RL with temporal abstraction
- Implement options framework (Sutton, Precup, Singh)
- Apply feudal RL and HAC (Hierarchical Actor-Critic)

## Temporal Abstraction

### Options Framework
An option is a temporally-extended action with:
- **Initiation set**: $I \subseteq \mathcal{S}$
- **Policy**: $\pi : \mathcal{S} \times \mathcal{A} \to [0, 1]$
- **Termination condition**: $\beta : \mathcal{S} \to [0, 1]$

### Option-Critic Architecture
Learn options end-to-end:
1. **Intra-option policy**: $\pi_\theta(a \mid s, \omega)$
2. **Termination function**: $\beta_\theta(s, \omega)$

$$Q(s, \omega) = \sum_a \pi(a \mid s, \omega) [R(s, a) + \gamma \sum_{s'} P(s' \mid s, a) U(s', \omega)]$$

$$U(s', \omega) = (1 - \beta(s', \omega)) Q(s', \omega) + \beta(s', \omega) \max_{\omega'} Q(s', \omega')$$

## Feudal RL

### Manager-Worker Hierarchy
- **Manager**: Sets subgoals at lower temporal resolution
- **Worker**: Achieves subgoals via low-level actions

$$g_t = f_{\text{manager}}(s_t) \quad \text{(subgoal)}$$
$$a_t = f_{\text{worker}}(s_t, g_t) \quad \text{(primitive action)}$$

## HAC (Hierarchical Actor-Critic)

### Multi-Level Hierarchy
Each level learns:
1. A policy to achieve subgoals from level above
2. A subgoal generation function for level below
3. A value function with subgoal-conditioned rewards

## Code: Options Framework

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class OptionCritic(nn.Module):
    def __init__(self, state_dim, action_dim, n_options=4, hidden=128):
        super().__init__()
        self.n_options = n_options
        self.shared = nn.Sequential(
            nn.Linear(state_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
        )
        # Intra-option Q for each option
        self.q_options = nn.Linear(hidden, n_options * action_dim)
        # Termination probabilities
        self.termination = nn.Linear(hidden, n_options)
        # Option-value function
        self.q_option = nn.Linear(hidden, n_options)

    def forward(self, state):
        features = self.shared(state)
        q_options = self.q_options(features).view(-1, self.n_options, None)
        term_probs = torch.sigmoid(self.termination(features))
        q_option = self.q_option(features)
        return q_options, term_probs, q_option

class HierarchicalAgent:
    def __init__(self, state_dim, action_dim, n_subgoals=10):
        self.manager = nn.Sequential(
            nn.Linear(state_dim, 128), nn.ReLU(),
            nn.Linear(128, 128), nn.ReLU(),
            nn.Linear(128, n_subgoals), nn.Tanh(),
        )
        self.worker = nn.Sequential(
            nn.Linear(state_dim + n_subgoals, 128), nn.ReLU(),
            nn.Linear(128, 128), nn.ReLU(),
            nn.Linear(128, action_dim), nn.Tanh(),
        )
        self.man_optim = torch.optim.Adam(self.manager.parameters(), lr=1e-4)
        self.wor_optim = torch.optim.Adam(self.worker.parameters(), lr=1e-3)

    def get_subgoal(self, state):
        state = torch.FloatTensor(state)
        return self.manager(state).detach().numpy()

    def act(self, state, subgoal):
        state = torch.FloatTensor(state)
        sg = torch.FloatTensor(subgoal)
        action = self.worker(torch.cat([state, sg]))
        return action.detach().numpy()

    def intrinsic_reward(self, state, subgoal, next_state):
        # How well is worker achieving subgoal
        sg = torch.FloatTensor(subgoal)
        ns = torch.FloatTensor(next_state)
        return -F.mse_loss(ns, sg).item()
```

## HRL Benchmarks

| Method | AntMaze | Kitchen | Montezuma's Revenge |
|--------|---------|---------|-------------------|
| Flat SAC | 10% | 30% | 0% |
| Option-Critic | 20% | 40% | — |
| HIRO | 80% | 60% | — |
| Feudal Networks | 50% | 35% | 15% |
| HAC | 75% | 55% | — |
| Go-Explore | — | — | 85% |

## Practical Considerations
- **Subgoal design**: States make better subgoals than arbitrary vectors
- **Temporal resolution**: Higher-level = slower updates = more stable
- **Credit assignment**: Harder in hierarchical setups
- **Termination frequency**: Too frequent = no hierarchy; too rare = no temporal abstraction

## References
- Sutton, Precup, Singh, "Between MDPs and semi-MDPs: A Framework for Temporal Abstraction in Reinforcement Learning", AIJ 1999
- Dayan & Hinton, "Feudal Reinforcement Learning", NeurIPS 1992
- Vezhnevets, Osindero, et al., "FeUdal Networks for Hierarchical Reinforcement Learning", ICML 2017
- Nachum, Gu, et al., "Data-Efficient Hierarchical Reinforcement Learning (HIRO)", NeurIPS 2018
- Levy, Platt, Saenko, "Hierarchical Actor-Critic (HAC)", NeurIPS 2019
