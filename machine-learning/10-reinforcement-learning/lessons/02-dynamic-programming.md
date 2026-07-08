# Lesson 10.02: Dynamic Programming

## Learning Objectives
- Understand policy evaluation and policy iteration
- Implement value iteration for MDPs
- Apply generalized policy iteration (GPI)

## Policy Evaluation

### Iterative Policy Evaluation
$$V_{k+1}(s) = \sum_a \pi(a \mid s) \sum_{s', r} p(s', r \mid s, a)[r + \gamma V_k(s')]$$

- Repeated application of Bellman expectation operator
- Converges to $V^\pi$ as $k \to \infty$

## Policy Improvement

### Policy Improvement Theorem
$$\pi'(s) = \arg\max_a Q^\pi(s, a)$$

If $\pi'$ is greedy w.r.t. $V^\pi$, then $\pi' \geq \pi$.

## Policy Iteration

### Algorithm
```
1. Initialize π arbitrarily
2. Repeat:
   a. Evaluate V^π (policy evaluation)
   b. Improve π' = greedy(V^π)
   c. If π' == π: return π
   d. Else: π = π'
```

## Value Iteration

### Algorithm
$$V_{k+1}(s) = \max_a \sum_{s', r} p(s', r \mid s, a)[r + \gamma V_k(s')]$$

- Combines policy evaluation + improvement into one step
- Truncated policy evaluation (one sweep)
- Converges to $V^*$ (Bellman optimality operator is contraction)

## Code: Value Iteration

```python
import numpy as np

def value_iteration(mdp, tol=1e-6, max_iter=1000):
    V = np.zeros(mdp.n_states)
    for _ in range(max_iter):
        delta = 0
        for s in range(mdp.n_states):
            v = V[s]
            V[s] = max(sum(p * (r + mdp.gamma * V[s_next])
                         for p, s_next, r in mdp.P[s][a])
                      for a in range(mdp.n_actions))
            delta = max(delta, abs(v - V[s]))
        if delta < tol:
            break
    # Extract greedy policy
    policy = np.zeros(mdp.n_states, dtype=int)
    for s in range(mdp.n_states):
        policy[s] = np.argmax([sum(p * (r + mdp.gamma * V[s_next])
                                   for p, s_next, r in mdp.P[s][a])
                               for a in range(mdp.n_actions)])
    return V, policy

def generalized_policy_iteration(mdp, eval_tol=1e-4, max_iter=100):
    V = np.zeros(mdp.n_states)
    policy = np.zeros(mdp.n_states, dtype=int)
    for _ in range(max_iter):
        # Partial policy evaluation
        for _ in range(3):
            for s in range(mdp.n_states):
                a = policy[s]
                V[s] = sum(p * (r + mdp.gamma * V[s_next])
                          for p, s_next, r in mdp.P[s][a])
        # Policy improvement
        policy_stable = True
        for s in range(mdp.n_states):
            old_a = policy[s]
            policy[s] = np.argmax([sum(p * (r + mdp.gamma * V[s_next])
                                       for p, s_next, r in mdp.P[s][a])
                                   for a in range(mdp.n_actions)])
            if old_a != policy[s]:
                policy_stable = False
        if policy_stable:
            break
    return V, policy
```

## Comparison

| Method | Complexity | Convergence | Use Case |
|--------|-----------|-------------|----------|
| Policy evaluation | $O(|\mathcal{S}|^2 |\mathcal{A}|)$ per iteration | Linear | Large MDPs |
| Value iteration | $O(|\mathcal{S}|^2 |\mathcal{A}|)$ per iteration | Linear | Small MDPs |
| Policy iteration | $O(|\mathcal{S}|^3)$ per evaluation | Quadratic | Medium MDPs |
| Modified PI | $O(|\mathcal{S}|^2 |\mathcal{A}|)$ per sweep | Linear | Large MDPs |

## References
- Bellman, "Dynamic Programming", 1957
- Howard, "Dynamic Programming and Markov Processes", 1960
- Sutton & Barto, "Reinforcement Learning: An Introduction", 2018 (Ch. 4)
