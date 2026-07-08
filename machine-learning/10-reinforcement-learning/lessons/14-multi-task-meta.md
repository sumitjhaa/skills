# Lesson 10.14: Multi-Task & Meta RL

## Learning Objectives
- Understand multi-task RL and shared representations
- Implement MAML (Model-Agnostic Meta-Learning) for RL
- Apply context-based meta-RL and RL2

## Multi-Task RL

### Shared Policy
$$\pi_\theta(a \mid s, z) \quad z = \text{task embedding}$$

- Single policy across multiple tasks
- Task inference: infer $z$ from experience

## Meta-RL

### Problem
$$\max_\theta \mathbb{E}_{T \sim p(T)} [ \mathbb{E}_{\pi_\theta} [ \sum \gamma^t R_T(s_t, a_t) ]]$$

- Learn to learn: adapt to new tasks from few trials
- Inner loop: adapt to task; Outer loop: meta-learn

## MAML (Model-Agnostic Meta-Learning)

### Algorithm
```
For each task T_i:
    Sample K trajectories
    θ_i' = θ - α ∇_θ L_T_i(π_θ)  // Inner loop
θ = θ - β ∇_θ ∑_i L_T_i(π_θ_i')   // Outer loop (meta-gradient)
```

### MAML for RL
- Policy gradient in inner loop
- Hessian-vector products in outer loop

## RL2

### Recurrent Architecture
- RNN takes (s_t, a_t, r_t, done_t) as input
- Hidden state encodes learning algorithm
- Meta-train on distribution of MDPs

### Inference
At test time, RNN hidden state adapts to new task automatically.

## PEARL (Probabilistic Embeddings for RL)

### Task Inference via Probabilistic Embedding
```python
q(z | c) = encoder(c)  // Infer task from context
π(a | s, z)            // Policy conditioned on task embedding
```

- Sample task embedding z from posterior
- Train with SAC + variational inference

## Code: MAML for RL

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Normal

class MAMLRL:
    def __init__(self, state_dim, action_dim, hidden=128, inner_lr=0.01, outer_lr=0.001):
        self.policy = nn.Sequential(
            nn.Linear(state_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, action_dim),
        )
        self.inner_lr = inner_lr
        self.optim = torch.optim.Adam(self.policy.parameters(), lr=outer_lr)

    def forward(self, state):
        return self.policy(state)

    def clone_policy(self):
        clone = type(self.policy)()
        clone.load_state_dict(self.policy.state_dict())
        return clone

    def inner_update(self, policy, trajectories, gamma=0.99):
        loss = 0
        G = 0
        for t in reversed(range(len(trajectories['rewards']))):
            state = torch.FloatTensor(trajectories['states'][t])
            action = torch.FloatTensor(trajectories['actions'][t])
            reward = trajectories['rewards'][t]
            G = reward + gamma * G
            log_prob = Normal(policy(state), 1.0).log_prob(action).sum()
            loss -= log_prob * G
        
        grads = torch.autograd.grad(loss, policy.parameters())
        new_policy = self.clone_policy()
        for param, grad in zip(new_policy.parameters(), grads):
            param.data -= self.inner_lr * grad
        return new_policy

    def meta_update(self, tasks_data):
        meta_loss = 0
        for task_data in tasks_data:
            adapted_policy = self.inner_update(self.policy, task_data['train'])
            task_loss = self.inner_update(adapted_policy, task_data['test'], gamma=0.99)
            meta_loss += task_loss
        
        self.optim.zero_grad()
        meta_loss.backward()
        self.optim.step()
        return meta_loss.item()
```

## Meta-RL Benchmarks

| Algorithm | Cheetah-Dir (adapt) | Ant-Dir (adapt) | ML1 (score) |
|-----------|-------------------|----------------|-------------|
| MAML | 80% | 60% | 0.40 |
| RL2 | 85% | 65% | 0.45 |
| PEARL | 90% | 80% | 0.52 |
| VariBAD | 88% | 75% | 0.48 |
| Dreamer (no meta) | 75% | 55% | 0.35 |

## Practical Considerations
- **Task distribution**: Too narrow = overfitting; too broad = hard to meta-learn
- **Inner loop length**: 1-5 gradient steps typical (short = fast adaptation)
- **Outer loop**: Use second-order gradients or first-order approximation (FOMAML)
- **On-policy vs off-policy**: PEARL is off-policy (more sample efficient)

## References
- Finn, Abbeel, Levine, "Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks (MAML)", ICML 2017
- Duan, Schulman, et al., "RL2: Fast Reinforcement Learning via Slow Reinforcement Learning", 2016
- Rakelly, Zhou, et al., "Efficient Off-Policy Meta-Reinforcement Learning via Probabilistic Context Variables (PEARL)", ICML 2019
- Zintgraf, Shiarlis, et al., "VariBAD: A Very Good Method for Bayes-Adaptive Deep RL via Meta-Learning", ICLR 2020
- Yu, Quillen, et al., "Meta-World: A Benchmark and Evaluation for Multi-Task and Meta Reinforcement Learning", CoRL 2020
