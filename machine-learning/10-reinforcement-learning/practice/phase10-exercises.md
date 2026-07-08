# Phase 10: Reinforcement Learning — Practice Exercises

## 1. MDP Value Iteration

**Theory:** Derive the Bellman optimality equation for a finite MDP. Explain why value iteration converges to the optimal value function and how the contraction property of the Bellman operator guarantees this.

**Coding:** Implement value iteration for a 5×5 grid world with four actions and a terminal state at (4,4). Report the optimal value of the start state (0,0). Plot the value function as a heatmap.

## 2. Q-Learning vs SARSA

**Theory:** Explain the difference between on-policy (SARSA) and off-policy (Q-Learning) learning. Why does SARSA learn a safer path in the cliff-walking environment? What is the role of the exploration policy in each case?

**Coding:** Run Q-Learning and SARSA on the cliff-walking environment. Plot the average cumulative reward per episode over 500 episodes. Discuss which algorithm converges to a safer policy and why.

## 3. DQN with Experience Replay

**Theory:** Explain the two key innovations in DQN: experience replay and target networks. Why does experience replay break the correlation between consecutive transitions? How does the target network stabilise training?

**Coding:** Implement a minimal DQN (numpy neural network) with a replay buffer for a 2D navigation task with 4 discrete actions. Compare training with and without a target network over 300 episodes. Plot the loss curves.

## 4. Policy Gradient (REINFORCE)

**Theory:** Derive the REINFORCE gradient estimator from the policy gradient theorem. Why does subtracting a baseline reduce the variance of the gradient estimate without introducing bias?

**Coding:** Implement REINFORCE with a baseline on a continuous CartPole-like environment. Plot the episode length over training. Experiment with different learning rates (1e-4, 1e-3, 1e-2) and report which works best.

## 5. Exploration Comparison

**Theory:** Compare ε-greedy, UCB, and Thompson sampling from a Bayesian perspective. How does Thompson sampling automatically balance exploration and exploitation through posterior sampling?

**Coding:** Compare ε-greedy (ε=0.1), UCB (c=2), and Thompson sampling on a 20-armed Bernoulli bandit with 5000 trials. Run 100 seeds and plot the average cumulative regret. Which algorithm minimizes regret?

## 6. Offline RL with CQL

**Theory:** Explain the distributional shift problem in offline RL. How does the CQL regularization term penalize out-of-distribution actions while preserving the ability to learn from the dataset?

**Coding:** Generate a suboptimal dataset for a 10-state MDP. Train Q-Learning and CQL on this dataset. Report the performance gap between the learned policy and the behaviour policy. Show that CQL mitigates overestimation.

## 7. MCTS for Connect Four

**Theory:** Explain the four phases of Monte Carlo Tree Search: selection, expansion, simulation, backpropagation. How does the UCT formula balance exploration and exploitation during tree search?

**Coding:** Implement MCTS (100 simulations per move) for a simplified 4×4 Connect Four. Play 10 games against a random opponent and report win rate. Visualize the search tree for the first move.

## 8. RLHF Reward Modelling

**Theory:** Derive the Bradley-Terry preference model used in RLHF. Explain how the reward model is trained from pairwise preferences and why the log-likelihood objective is appropriate.

**Coding:** Generate pairwise preferences from a known reward function R(s) = -||s||₂ for random 4D states. Train a reward model and compare its predictions to the true reward on a held-out test set. Compute the Spearman rank correlation.

## 9. Safe RL with Constraints

**Theory:** Formulate the constrained MDP (CMDP) and the Lagrangian relaxation approach. Explain how the Lagrange multiplier automatically adjusts the trade-off between reward and safety violation.

**Coding:** Implement a constrained MDP where states {2, 5, 7} are unsafe. Train with a Lagrangian multiplier and plot the constraint violation rate over training. Compare with a penalty-based baseline (fixed penalty weight).

## 10. Continuous Control with DDPG

**Theory:** Explain why DDPG uses a deterministic policy with an off-policy actor-critic framework. Why does the Ornstein-Uhlenbeck process provide temporally correlated exploration noise?

**Coding:** Implement DDPG for a 2D point robot navigating to a goal. Use Ornstein-Uhlenbeck noise for exploration. Plot the distance to goal over training steps. Compare performance with and without the target network.

## 11. Imitation Learning via Behavioural Cloning

**Theory:** Explain the compounding error problem in behavioural cloning. How does DAgger (Dataset Aggregation) address the distributional shift between the expert's state distribution and the learned policy's state distribution?

**Coding:** Generate expert demonstrations from a pre-trained policy for the CartPole environment. Train a behavioural cloning policy on varying dataset sizes (10, 50, 200, 1000 episodes). Plot the performance gap.

## 12. Multi-Agent RL with MADDPG

**Theory:** Explain the centralized training with decentralized execution (CTDE) paradigm. Why does MADDPG use a centralized critic that observes all agents' actions? What problems arise from non-stationarity in multi-agent environments?

**Coding:** Implement a simplified 2-agent cooperative navigation task (2 agents must cover 2 landmarks). Train with independent DDPG and MADDPG. Compare the success rates and the emergence of coordinated behaviour.
