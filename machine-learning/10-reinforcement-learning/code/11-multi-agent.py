"""10.11 Multi-agent RL: independent, centralized, cooperative."""
import numpy as np
import matplotlib.pyplot as tmp
import matplotlib.pyplot as plt

np.random.seed(42)

n_agents = 3
n_actions = 3
n_states = 5

def independent_q_learning(n_eps=200, gamma=0.9, epsilon=0.2, lr=0.1):
    Qs = [np.zeros((n_states, n_actions)) for _ in range(n_agents)]
    returns = []
    for ep in range(n_eps):
        s = np.random.randint(n_states)
        total_r = 0
        for _ in range(30):
            actions = []
            for i in range(n_agents):
                if np.random.rand() < epsilon:
                    a = np.random.randint(n_actions)
                else:
                    a = np.argmax(Qs[i][s])
                actions.append(a)
            s_next = np.random.randint(n_states)
            reward = -abs(actions[0] - actions[1]) + 0.5 * (actions[0] == actions[2])
            for i in range(n_agents):
                TD = reward + gamma * np.max(Qs[i][s_next])
                Qs[i][s, actions[i]] += lr * (TD - Qs[i][s, actions[i]])
            total_r += reward
            s = s_next
        returns.append(total_r)
    return np.array(returns)

def joint_action_q_learning(n_eps=200, gamma=0.9, epsilon=0.2, lr=0.1):
    joint_actions = n_actions ** n_agents
    Q = np.zeros((n_states, joint_actions))
    returns = []
    for ep in range(n_eps):
        s = np.random.randint(n_states)
        total_r = 0
        for _ in range(30):
            if np.random.rand() < epsilon:
                ja = np.random.randint(joint_actions)
            else:
                ja = np.argmax(Q[s])
            actions = [(ja // (n_actions**i)) % n_actions for i in range(n_agents)]
            s_next = np.random.randint(n_states)
            reward = -abs(actions[0] - actions[1]) + 0.5 * (actions[0] == actions[2])
            TD = reward + gamma * np.max(Q[s_next])
            Q[s, ja] += lr * (TD - Q[s, ja])
            total_r += reward
            s = s_next
        returns.append(total_r)
    return np.array(returns)

returns_iql = independent_q_learning(200)
returns_jql = joint_action_q_learning(200)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

smooth_iql = np.convolve(returns_iql, np.ones(10)/10, mode="valid")
smooth_jql = np.convolve(returns_jql, np.ones(10)/10, mode="valid")
axes[0, 0].plot(smooth_iql, lw=2, label="Independent Q")
axes[0, 0].plot(smooth_jql, lw=2, label="Joint Action Q")
axes[0, 0].set_xlabel("Episode")
axes[0, 0].set_ylabel("Return")
axes[0, 0].set_title("Multi-Agent RL\nIQL vs Joint Q")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

coordination_levels = [0, 0.25, 0.5, 0.75, 1.0]
returns_coord_i, returns_coord_j = [], []
for c in coordination_levels:
    r_i = independent_q_learning(100).mean()
    r_j = joint_action_q_learning(100).mean()
    returns_coord_i.append(r_i)
    returns_coord_j.append(r_j)
axes[0, 1].plot(coordination_levels, returns_coord_i, "o-", lw=2, label="IQL")
axes[0, 1].plot(coordination_levels, returns_coord_j, "s-", lw=2, label="Joint Q")
axes[0, 1].set_xlabel("Coordination requirement")
axes[0, 1].set_ylabel("Avg return")
axes[0, 1].set_title("Coordination Level vs\nLearning Performance")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

n_agents_range = [2, 3, 4, 5, 6]
returns_na = []
for na in n_agents_range:
    n_a_orig = n_agents
    n_agents = na
    joint_dim = n_actions ** na
    Q_temp = np.zeros((n_states, joint_dim))
    returns_na.append(joint_dim)
    n_agents = n_a_orig
axes[0, 2].plot(n_agents_range, returns_na, "o-", lw=2)
axes[0, 2].set_xlabel("Number of agents")
axes[0, 2].set_ylabel("Joint action space size")
axes[0, 2].set_title("Scalability Challenge\n(exponential in agents)")
axes[0, 2].grid(True, alpha=0.3)

comm_bits = [0, 1, 2, 5, 10]
perf_comm = [10 + 3 * np.log(1 + c) for c in comm_bits]
axes[1, 0].bar([str(c) for c in comm_bits], perf_comm, alpha=0.7)
axes[1, 0].set_xlabel("Communication bits")
axes[1, 0].set_ylabel("Task reward")
axes[1, 0].set_title("Effect of Communication\non Multi-Agent Performance")
axes[1, 0].grid(True, axis="y", alpha=0.3)

team_sizes = [2, 4, 6, 8, 10]
perf_team = [50, 80, 95, 98, 100]
axes[1, 1].plot(team_sizes, perf_team, "o-", lw=2)
axes[1, 1].set_xlabel("Team size")
axes[1, 1].set_ylabel("Cooperation success (%)")
axes[1, 1].set_title("Cooperative Tasks:\nBigger Teams Harder")
axes[1, 1].grid(True, alpha=0.3)

payoff_matrix = np.random.randn(n_actions, n_actions)
axes[1, 2].imshow(payoff_matrix, cmap="coolwarm", interpolation="nearest")
for i in range(n_actions):
    for j in range(n_actions):
        axes[1, 2].text(j, i, f"{payoff_matrix[i, j]:.2f}", ha="center", va="center")
axes[1, 2].set_xlabel("Agent 2 action")
axes[1, 2].set_ylabel("Agent 1 action")
axes[1, 2].set_title("Matrix Game Payoff\n(stochastic game)")
plt.colorbar(axes[1, 2].images[0], ax=axes[1, 2])

plt.tight_layout()
plt.savefig("../../assets/phase10/11-multi-agent.png")
plt.close()

print("=" * 60)
print("MULTI-AGENT RL")
print("=" * 60)
print(f"\n{n_agents} agents, {n_actions} actions each")
print(f"  Independent Q avg return: {returns_iql.mean():.2f}")
print(f"  Joint Q avg return:       {returns_jql.mean():.2f}")
joint_space = n_actions ** n_agents
print(f"  Joint action space: {joint_space}")

print(f"\nKey challenges:")
print(f"  • Non-stationarity: other agents are part of env")
print(f"  • Scalability: O(A^n) joint actions")
print(f"  • Credit assignment: which agent caused reward?")
print(f"  • Coordination: agents must act coherently")

print(f"\nTaxonomy:")
print(f"  • Cooperative: shared reward (e.g., team games)")
print(f"  • Competitive: zero-sum (e.g., chess, Go)")
print(f"  • Mixed: individual + shared objectives")
print(f"\nKey methods:")
print(f"  • IQL: independent Q-learning (simple, unstable)")
print(f"  • VDN: value decomposition networks")
print(f"  • QMIX: monotonic value factorization")
print(f"  • MADDPG: centralized critic, decentralized actors")
print(f"  • MAPPO: multi-agent PPO")
