# Lesson 10.12: Imitation Learning

## Learning Objectives
- Understand behavioural cloning and its limitations
- Implement inverse reinforcement learning (IRL)
- Apply generative adversarial imitation learning (GAIL)

## Behavioural Cloning (BC)

### Supervised Learning Approach
$$\pi^* = \arg\max_\pi \mathbb{E}_{(s, a) \sim \mathcal{D}} [\log \pi(a \mid s)]$$

### Limitations
- **Distribution mismatch**: Errors compound at test time (causative)
- **Requires expert demonstrations**: Not always available

### DAgger (Dataset Aggregation)
1. Train policy π on expert data D
2. Run π to collect new trajectories
3. Ask expert to label visited states with correct actions
4. Add to D and retrain

## Inverse Reinforcement Learning (IRL)

### Problem
Learn reward function $R(s, a)$ from expert demonstrations.

### MaxEnt IRL
$$\max_R \mathbb{E}_\pi [\sum \gamma^t R(s_t, a_t)] - \mathbb{E}_{\pi_{\text{expert}}} [\sum \gamma^t R(s_t, a_t)] - \mathcal{H}(\pi)$$

- Maximise entropy of policy matching expert feature counts

## GAIL (Generative Adversarial Imitation Learning)

### GAN Formulation
```python
Discriminator D: distinguish expert from policy
Generator π: produce trajectories that fool D
```

### Objective
$$\min_\pi \max_D \mathbb{E}_{\pi_{\text{expert}}} [\log D(s, a)] + \mathbb{E}_{\pi} [\log(1 - D(s, a))] - \lambda \mathcal{H}(\pi)$$

- D: learns to discriminate expert vs policy
- π: trained to maximise D's mistake (via policy gradient)

## Code: Behavioral Cloning

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class BehavioralClone:
    def __init__(self, state_dim, action_dim, hidden=256):
        self.policy = nn.Sequential(
            nn.Linear(state_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
            nn.Linear(hidden, action_dim),
        )
        self.optim = torch.optim.Adam(self.policy.parameters(), lr=1e-3)

    def train(self, expert_states, expert_actions, epochs=100, batch_size=64):
        dataset = torch.utils.data.TensorDataset(
            torch.FloatTensor(expert_states),
            torch.FloatTensor(expert_actions),
        )
        loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        for epoch in range(epochs):
            epoch_loss = 0
            for states, actions in loader:
                pred_actions = self.policy(states)
                loss = F.mse_loss(pred_actions, actions)
                self.optim.zero_grad()
                loss.backward()
                self.optim.step()
                epoch_loss += loss.item()
            print(f"Epoch {epoch}: loss = {epoch_loss:.4f}")

    def act(self, state):
        with torch.no_grad():
            state = torch.FloatTensor(state).unsqueeze(0)
            return self.policy(state).numpy()[0]


class GAIL:
    def __init__(self, state_dim, action_dim):
        self.policy = nn.Sequential(
            nn.Linear(state_dim + action_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
            nn.Linear(hidden, 1),
        )
        self.discriminator = nn.Sequential(
            nn.Linear(state_dim + action_dim, 100), nn.ReLU(),
            nn.Linear(100, 100), nn.ReLU(),
            nn.Linear(100, 1),
        )
        self.policy_optim = torch.optim.Adam(self.policy.parameters(), lr=1e-3)
        self.disc_optim = torch.optim.Adam(self.discriminator.parameters(), lr=1e-3)

    def update_discriminator(self, expert_sa, policy_sa):
        expert_score = self.discriminator(expert_sa)
        policy_score = self.discriminator(policy_sa)
        loss = -torch.mean(torch.log(torch.sigmoid(expert_score) + 1e-8)
                          + torch.log(1 - torch.sigmoid(policy_score) + 1e-8))
        self.disc_optim.zero_grad()
        loss.backward()
        self.disc_optim.step()
        return loss.item()

    def get_reward(self, states, actions):
        sa = torch.cat([states, actions], dim=-1)
        return -torch.log(1 - torch.sigmoid(self.discriminator(sa)) + 1e-8)
```

## Imitation Learning Comparison

| Method | Expert Required | Model Free | Reward Learning | Performance |
|--------|----------------|-----------|----------------|-------------|
| Behavioral Cloning | Yes | Yes | No | Fair (compounding errors) |
| DAgger | Yes (online) | Yes | No | Good |
| MaxEnt IRL | Yes | No | Yes | Good |
| GAIL | Yes | Yes | Implicit | Very good |
| Inverse RL from observations | Yes (state only) | Yes | Yes | Moderate |

## References
- Pomerleau, "ALVINN: An Autonomous Land Vehicle in a Neural Network", NeurIPS 1988
- Ross, Gordon, Bagnell, "A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning (DAgger)", AISTATS 2011
- Abbeel & Ng, "Apprenticeship Learning via Inverse Reinforcement Learning", ICML 2004
- Ho & Ermon, "Generative Adversarial Imitation Learning", NeurIPS 2016
- Ziebart, Maas, et al., "Maximum Entropy Inverse Reinforcement Learning", AAAI 2008
