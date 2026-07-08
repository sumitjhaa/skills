# Phase 10: Reinforcement Learning

Reinforcement Learning from foundational MDP theory to full-system design. Each lesson includes a markdown explanation and a standalone runnable Python implementation.

| # | Lesson | Code | Topic |
|---|--------|------|-------|
| 1 | [MDP](lessons/01-mdp.md) | [MDP](code/01-mdp.py) | Markov Decision Processes, Bellman equations, optimality |
| 2 | [Dynamic Programming](lessons/02-dynamic-programming.md) | [DP](code/02-dynamic-programming.py) | Policy iteration, value iteration, policy evaluation |
| 3 | [Monte Carlo](lessons/03-monte-carlo.md) | [MC](code/03-monte-carlo.py) | MC prediction, MC control with exploring starts |
| 4 | [TD Learning](lessons/04-td-learning.md) | [TD](code/04-td-learning.py) | SARSA, Q-Learning, Expected SARSA on Grid World |
| 5 | [Function Approximation](lessons/05-function-approximation.md) | [DQN](code/05-function-approximation.py) | DQN, Rainbow, neural network Q-functions |
| 6 | [Policy Gradient](lessons/06-policy-gradient.md) | [PG](code/06-policy-gradient.py) | REINFORCE, PPO, TRPO |
| 7 | [Advanced Actor-Critic](lessons/07-advanced-actor-critic.md) | [SAC](code/07-advanced-actor-critic.py) | SAC, TD3, soft actor-critic with entropy |
| 8 | [Model-Based](lessons/08-model-based.md) | [Dreamer](code/08-model-based.py) | Dreamer, world models, planning in latent space |
| 9 | [Exploration](lessons/09-exploration.md) | [Explore](code/09-exploration.py) | Epsilon-greedy, UCB, Thompson sampling, intrinsic motivation |
| 10 | [Offline RL](lessons/10-offline-rl.md) | [Offline](code/10-offline-rl.py) | CQL, IQL, Decision Transformer |
| 11 | [Multi-Agent](lessons/11-multi-agent.md) | [MultiAgent](code/11-multi-agent.py) | MADDPG, QMIX, VDN |
| 12 | [Imitation Learning](lessons/12-imitation-learning.md) | [Imitation](code/12-imitation-learning.py) | BC, GAIL, IRL |
| 13 | [Hierarchical RL](lessons/13-hierarchical-rl.md) | [HiRL](code/13-hierarchical-rl.py) | Options, feudal networks, HIRO |
| 14 | [Multi-Task & Meta-RL](lessons/14-multi-task-meta.md) | [MetaRL](code/14-multi-task-meta.py) | MAML, context-based, task inference |
| 15 | [Safe RL](lessons/15-safe-rl.md) | [SafeRL](code/15-safe-rl.py) | Constrained MDPs, Lagrangian methods, shielding |
| 16 | [RLHF](lessons/16-rlhf.md) | [RLHF](code/16-rlhf.py) | Reward modelling, PPO with KL penalty, DPO |
| 17 | [Continuous Control](lessons/17-continuous-control.md) | [ContControl](code/17-continuous-control.py) | Robotics control, DDPG, PPO for continuous actions |
| 18 | [Planning](lessons/18-planning.md) | [Planning](code/18-planning.py) | MCTS, MuZero, AlphaZero |
| 19 | [Robotics](lessons/19-robotics.md) | [Robotics](code/19-robotics.py) | Sim-to-real, domain randomisation, manipulation |
| 20 | [Full RL System](lessons/20-rl-system.md) | [RLSystem](code/20-rl-system.py) | Complete RL system architecture, deployment, monitoring |

## Getting Started

```bash
# Run any lesson's code
python code/01-mdp.py

# Read a lesson
cat lessons/01-mdp.md

# Practice exercises
code practice/phase10-exercises.md
```

**Dependencies:** `numpy`, `scipy`, `matplotlib`
