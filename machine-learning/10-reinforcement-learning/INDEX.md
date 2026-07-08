# Phase 10 — Reinforcement Learning

## 1. Phase Overview

| Field | Value |
|---|---|
| **Phase** | 10 — Reinforcement Learning |
| **Lessons** | 20 |
| **Core topics** | MDPs, dynamic programming, Monte Carlo methods, TD learning, function approximation, policy gradient, advanced actor-critic (A2C, PPO, SAC, DDPG), model-based RL, exploration, offline RL, multi-agent, imitation learning, hierarchical RL, multi-task/meta-RL, safe RL, RLHF, continuous control, planning, robotics, RL system |

## 2. Prerequisites

- **Prior phases:** [Phase 01](../01-linear-algebra/INDEX.md) (linear value functions), [Phase 02](../02-calculus-optimization/INDEX.md) (policy gradients as optimization), [Phase 03](../03-probability-statistics/INDEX.md) (expected return, MC sampling), [Phase 06](../06-deep-learning/INDEX.md) (deep Q-networks, policy networks, training pipelines)
- **Python frameworks:** [`../../python-frameworks/pytorch/`](../../python-frameworks/pytorch/) (NN implementations), [`../../python-frameworks/numpy-pandas/`](../../python-frameworks/numpy-pandas/) (experience replay, data handling)

## 3. Lesson Table

| # | Title | What You'll Learn | Lesson | Code | Cross-References |
|---|---|---|---|---|---|
| 01 | MDP | Markov decision processes, Bellman equations | [lesson](lessons/01-mdp.md) | [code](code/01-mdp.py) | Used in: Phase 04 (Markov chains) |
| 02 | Dynamic Programming | Policy iteration, value iteration | [lesson](lessons/02-dynamic-programming.md) | [code](code/02-dynamic-programming.py) | Used in: Phase 05 (DP for HMM) |
| 03 | Monte Carlo Methods | MC prediction, control, exploring starts | [lesson](lessons/03-monte-carlo.md) | [code](code/03-monte-carlo.py) | Used in: Phase 04 (Monte Carlo) |
| 04 | TD Learning | TD(0), SARSA, Q-learning, expected SARSA | [lesson](lessons/04-td-learning.md) | [code](code/04-td-learning.py) | Used in: Phase 05 (online learning) |
| 05 | Function Approximation | Linear, neural network value functions | [lesson](lessons/05-function-approximation.md) | [code](code/05-function-approximation.py) | Used in: Phase 06 (MLPs) |
| 06 | Policy Gradient | REINFORCE, baseline, advantage | [lesson](lessons/06-policy-gradient.md) | [code](code/06-policy-gradient.py) | Used in: Phase 02 (policy gradient as optimization) |
| 07 | Advanced Actor-Critic | A2C, A3C, PPO, SAC, DDPG, TD3 | [lesson](lessons/07-advanced-actor-critic.md) | [code](code/07-advanced-actor-critic.py) | Used in: Phase 12 (RLHF capstone) |
| 08 | Model-Based RL | Dyna, learned models, planning | [lesson](lessons/08-model-based.md) | [code](code/08-model-based.py) | Used in: Phase 08 (visual RL) |
| 09 | Exploration | Epsilon-greedy, UCB, Thompson, curiosity | [lesson](lessons/09-exploration.md) | [code](code/09-exploration.py) | Used in: Phase 05 (bandits) |
| 10 | Offline RL | CQL, IQL, BCQ, conservative methods | [lesson](lessons/10-offline-rl.md) | [code](code/10-offline-rl.py) | Used in: Phase 11 (RL from logs) |
| 11 | Multi-Agent | MARL, QMIX, MADDPG, CTDE | [lesson](lessons/11-multi-agent.md) | [code](code/11-multi-agent.py) | Used in: Phase 04 (game theory) |
| 12 | Imitation Learning | Behavioral cloning, inverse RL, GAIL | [lesson](lessons/12-imitation-learning.md) | [code](code/12-imitation-learning.py) | Used in: Phase 08 (human pose) |
| 13 | Hierarchical RL | Options, HAM, feudal, HRL | [lesson](lessons/13-hierarchical-rl.md) | [code](code/13-hierarchical-rl.py) | Used in: Phase 09 (agents) |
| 14 | Multi-Task / Meta-RL | Context-based, gradient-based meta-RL | [lesson](lessons/14-multi-task-meta.md) | [code](code/14-multi-task-meta.py) | Used in: Phase 06 (meta-learning) |
| 15 | Safe RL | Constrained MDPs, safety layers, shielding | [lesson](lessons/15-safe-rl.md) | [code](code/15-safe-rl.py) | Used in: Phase 11 (responsible AI) |
| 16 | RLHF | Reward modeling, PPO for language | [lesson](lessons/16-rlhf.md) | [code](code/16-rlhf.py) | Used in: Phase 09 (alignment), Phase 12 (RLHF capstone) |
| 17 | Continuous Control | MuJoCo, PyBullet, locomotion | [lesson](lessons/17-continuous-control.md) | [code](code/17-continuous-control.py) | Used in: Phase 08 (visual RL) |
| 18 | Planning | MCTS, AlphaZero, search | [lesson](lessons/18-planning.md) | [code](code/18-planning.py) | Used in: Phase 09 (tree-of-thought) |
| 19 | Robotics | Robotic manipulation, pick-and-place, grasping | [lesson](lessons/19-robotics.md) | [code](code/19-robotics.py) | Used in: Phase 08 (3D vision) |
| 20 | RL System | Full reinforcement learning system design | [lesson](lessons/20-rl-system.md) | [code](code/20-rl-system.py) | Used in: Phase 11 (system design) |

## 4. Builds Toward

- **Phase 11** (RLHF integration with MLOps, model monitoring for RL systems)
- **Phase 12** (RLHF capstone, novel contribution, distributed training)

## 5. Quick Start

```bash
python3 code/01-mdp.py
```
