# Lesson 10.18: Planning

## Learning Objectives
- Understand planning with learned world models
- Implement Monte Carlo Tree Search (MCTS)
- Apply planning in MuZero and Dreamer

## Monte Carlo Tree Search (MCTS)

### Four Steps
1. **Selection**: Traverse tree using UCB:
   $$a^* = \arg\max_a Q(s, a) + c \sqrt{\frac{\ln N(s)}{N(s, a)}}$$
2. **Expansion**: Add new child node
3. **Simulation**: Rollout (using default or learned policy)
4. **Backup**: Update Q-values up the tree:
   $$N(s, a) \leftarrow N(s, a) + 1$$
   $$Q(s, a) \leftarrow Q(s, a) + \frac{G - Q(s, a)}{N(s, a)}$$

## MuZero Planning

### Learned Model Components
```
Representation: h: O → z (encode observation)
Dynamics: g: (z, a) → z', r (predict next state + reward)
Prediction: f: z → (π, v) (policy + value)
```

### MCTS with Learned Model
1. Use representation function at root
2. Use dynamics function for transitions
3. Use prediction function for leaf evaluation
4. Select action from search policy

## Dreamer

### World Model
```python
# Recurrent state-space model
z_t ∼ q(z_t | z_{t-1}, a_{t-1}, x_t)     # Posterior
ẑ_t ∼ p(ẑ_t | z_{t-1}, a_{t-1})          # Prior
x̂_t ∼ p(x̂_t | z_t)                        # Reconstruction
r̂_t ∼ p(r̂_t | z_t)                        # Reward prediction
```

### Planning in Latent Space
1. Sample trajectories in latent space using learned dynamics
2. Evaluate with learned reward/value function
3. Select action that maximises predicted return

## Code: MCTS for Planning

```python
import numpy as np
import math

class MCTSNode:
    def __init__(self, state, parent=None, action_idx=None):
        self.state = state
        self.parent = parent
        self.action_idx = action_idx
        self.children = {}
        self.visits = 0
        self.value = 0.0
        self.prior = 0.0

    def is_expanded(self):
        return len(self.children) > 0

    def ucb_score(self, c_puct=1.0):
        if self.visits == 0:
            return float('inf')
        return self.value / self.visits + c_puct * self.prior * math.sqrt(
            self.parent.visits) / (1 + self.visits)


def mcts(root, model, n_simulations=100):
    for _ in range(n_simulations):
        node = root
        # Selection
        while node.is_expanded():
            if len(node.children) == 0:
                break
            node = max(node.children.values(), key=lambda n: n.ucb_score())
        
        # Expansion
        if not node.is_expanded():
            policy, value = model.predict(node.state)
            for a, prob in enumerate(policy):
                if prob > 0.01:
                    next_state = model.simulate(node.state, a)
                    child = MCTSNode(next_state, parent=node, action_idx=a)
                    child.prior = prob
                    node.children[a] = child
            node.value = value
        else:
            # Simulation (rollout with learned value)
            g = 0
            state = node.state
            for _ in range(10):
                action = model.sample_action(state)
                state, reward = model.simulate(state, action)
                g = reward + 0.99 * g
            node.value = g
        
        # Backup
        while node is not None:
            node.visits += 1
            if node.parent:
                parent_value = node.parent.value
                node.parent.value += (node.value - parent_value) / node.parent.visits
            node = node.parent

    # Select best action
    best_child = max(root.children.values(), key=lambda n: n.visits)
    return best_child.action_idx
```

## Planning Algorithms Comparison

| Algorithm | Model | Planning Method | Use Case |
|-----------|-------|----------------|----------|
| MCTS | Learned/simulator | Tree search | Discrete actions (Go, Chess) |
| MuZero | Learned | MCTS | Model-free + planning |
| Dreamer | Learned | Latent imagination | Continuous control |
| Planning w/ learned model | Learned | Cross-entropy method | MPC for robotics |
| Tree Search | Given rules | BFS/DFS | Deterministic environments |

## References
- Coulom, "Efficient Selectivity and Backpropagation in Monte-Carlo Tree Search", 2006
- Kocsis & Szepesvári, "Bandit Based Monte-Carlo Planning", ECML 2006
- Silver, Schrittwieser, et al., "Mastering the Game of Go without Human Knowledge (AlphaGo Zero)", Nature 2017
- Schrittwieser, Antonoglou, et al., "Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model (MuZero)", Nature 2020
- Hafner, Lillicrap, et al., "Dream to Control: Learning Behaviors by Latent Imagination (Dreamer)", ICLR 2020
