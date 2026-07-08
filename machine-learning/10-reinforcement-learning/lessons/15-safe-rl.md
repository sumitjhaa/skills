# Lesson 10.15: Safe RL

## Learning Objectives
- Understand constrained MDPs and safety constraints
- Implement Lagrangian methods for safe RL
- Apply shielding and safety critics

## Constrained MDP (CMDP)

### Formulation
$$\max_\pi \mathbb{E}\left[ \sum_{t} \gamma^t R(s_t, a_t) \right]$$
$$\text{s.t. } \mathbb{E}\left[ \sum_{t} \gamma^t C_i(s_t, a_t) \right] \leq d_i$$

- $C_i$: cost functions (safety constraints)
- $d_i$: cost thresholds

### Safety Gym
Safe RL benchmark with constraints (e.g., keep robot velocity below threshold).

## Lagrangian Methods

### Augmented Objective
$$\min_\pi \max_{\lambda \geq 0} \mathbb{E}[R] - \lambda (\mathbb{E}[C] - d)$$

- $\lambda$: Lagrange multiplier (learned)
- If constraint violated: increase $\lambda$
- PPO-Lagrangian: PPO with cost penalty

## CPO (Constrained Policy Optimization)

### Trust Region + Constraints
$$\pi_{k+1} = \arg\max_\pi \mathbb{E}[A_\pi(s, a)]$$
$$\text{s.t. } \mathbb{E}[A_{C, \pi}(s, a)] + d \geq 0 \quad \text{(cost)}$$
$$\text{KL}(\pi \| \pi_k) \leq \delta$$

- Extension of TRPO for safety constraints

## Safety Critics

### Learned Cost Function
$$Q_C(s, a) = \mathbb{E}[C_t + \gamma_C C_{t+1} + \dots]$$

- Train safety critic alongside reward critic
- Use to filter actions: only choose actions with safe Q-value < threshold

## Shielding

### Formal Verification
- Use formal methods (model checking) for safety
- Shielding: override RL actions when they violate safety

```python
def shielded_action(state, rl_action, safety_policy):
    if safety_policy.is_safe(state, rl_action):
        return rl_action
    else:
        return safety_policy.safe_action(state)
```

## Code: PPO-Lagrangian

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class PPOLagrangian:
    def __init__(self, state_dim, action_dim, cost_limit=25.0, hidden=256):
        self.actor = nn.Sequential(
            nn.Linear(state_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
            nn.Linear(hidden, action_dim),
        )
        self.critic = nn.Sequential(
            nn.Linear(state_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
            nn.Linear(hidden, 1),
        )
        self.cost_critic = nn.Sequential(
            nn.Linear(state_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
            nn.Linear(hidden, 1),
        )
        self.actor_optim = torch.optim.Adam(self.actor.parameters(), lr=3e-4)
        self.critic_optim = torch.optim.Adam(self.critic.parameters(), lr=3e-4)
        self.cost_optim = torch.optim.Adam(self.cost_critic.parameters(), lr=3e-4)
        self.log_lagrange = nn.Parameter(torch.zeros(1))
        self.cost_limit = cost_limit
        self.gamma = 0.99

    def update(self, buffer):
        states, actions, rewards, costs, next_states, dones, old_logprobs = buffer
        
        # Compute advantages
        values = self.critic(states).squeeze()
        next_values = self.critic(next_states).squeeze()
        td_targets = rewards + self.gamma * next_values * (1 - dones)
        advantages = td_targets - values.detach()
        
        # Critic update
        critic_loss = F.mse_loss(values, td_targets.detach())
        self.critic_optim.zero_grad()
        critic_loss.backward()
        self.critic_optim.step()
        
        # Cost critic update
        cost_values = self.cost_critic(states).squeeze()
        next_cost_values = self.cost_critic(next_states).squeeze()
        cost_targets = costs + self.gamma * next_cost_values * (1 - dones)
        cost_loss = F.mse_loss(cost_values, cost_targets.detach())
        self.cost_optim.zero_grad()
        cost_loss.backward()
        self.cost_optim.step()
        
        # Actor update with Lagrangian
        new_logprobs = self.actor(states)
        ratio = (new_logprobs - old_logprobs.detach()).exp()
        lagrange_penalty = torch.exp(self.log_lagrange) * (
            cost_values.detach() - self.cost_limit
        )
        actor_loss = -(ratio * (advantages - lagrange_penalty)).mean()
        self.actor_optim.zero_grad()
        actor_loss.backward()
        self.actor_optim.step()
        
        # Update Lagrange multiplier
        cost_penalty = (cost_values.mean() - self.cost_limit).detach()
        self.log_lagrange.data += 0.01 * cost_penalty
```

## Safe RL Benchmarks

| Algorithm | Safety Gym (cost) | Reward | Cost Violation |
|-----------|------------------|--------|---------------|
| PPO (unconstrained) | 200 | 750 | 50+ |
| PPO-Lagrangian | 25 | 700 | 25 |
| CPO | 30 | 680 | 28 |
| TRPO-Lagrangian | 28 | 720 | 27 |
| FOCOPS | 22 | 710 | 20 |

## Practical Considerations
- **Cost threshold**: Set based on domain requirements
- **Conservative vs risk-seeking**: Trade-off between performance and safety
- **Warm-up**: Use safe expert for initial training
- **Monitoring**: Track cost violations in real-time during training

## References
- Altman, "Constrained Markov Decision Processes", 1999
- Achiam, Held, et al., "Constrained Policy Optimization", ICML 2017
- Ray, Achiam, Amodei, "Benchmarking Safe Exploration in Deep Reinforcement Learning (Safety Gym)", 2019
- Tessler, Mankowitz, Mannor, "Reward Constrained Policy Optimization", ICLR 2019
- Chow, Ghavamzadeh, et al., "Risk-Sensitive and Robust Decision-Making: a CVaR Optimization Approach", NeurIPS 2015
