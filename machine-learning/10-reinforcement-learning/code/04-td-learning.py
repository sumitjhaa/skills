"""10.04 TD Learning: Q-Learning and SARSA on Cliff Walking."""
import numpy as np

H, W = 4, 12
START = (3, 0)
GOAL = (3, 11)
ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # U, D, L, R
GAMMA = 0.99
ALPHA = 0.5
EPS = 0.1
EPISODES = 500


def is_cliff(r, c):
    return r == 3 and 1 <= c <= 10


def step(state, action):
    r, c = state
    dr, dc = ACTIONS[action]
    nr, nc = r + dr, c + dc
    if nr < 0 or nr >= H or nc < 0 or nc >= W:
        nr, nc = r, c
    if is_cliff(nr, nc):
        return START, -100, True
    if (nr, nc) == GOAL:
        return GOAL, -1, True
    return (nr, nc), -1, False


def run_q_learning():
    Q = np.zeros((H, W, 4))
    steps = 0
    for ep in range(EPISODES):
        s = START
        while True:
            if np.random.rand() < EPS:
                a = np.random.choice(4)
            else:
                a = np.argmax(Q[s[0], s[1]])
            ns, r, done = step(s, a)
            Q[s[0], s[1], a] += ALPHA * (r + GAMMA * np.max(Q[ns[0], ns[1]]) - Q[s[0], s[1], a])
            s = ns
            steps += 1
            if done:
                break
    return steps / EPISODES


def run_sarsa():
    Q = np.zeros((H, W, 4))
    steps = 0
    for ep in range(EPISODES):
        s = START
        a = np.random.choice(4) if np.random.rand() < EPS else np.argmax(Q[s[0], s[1]])
        while True:
            ns, r, done = step(s, a)
            na = np.random.choice(4) if np.random.rand() < EPS else np.argmax(Q[ns[0], ns[1]])
            Q[s[0], s[1], a] += ALPHA * (r + GAMMA * Q[ns[0], ns[1], na] - Q[s[0], s[1], a])
            s, a = ns, na
            steps += 1
            if done:
                break
    return steps / EPISODES


print(f"Q-Learning avg steps/ep: {run_q_learning():.1f}")
print(f"SARSA      avg steps/ep: {run_sarsa():.1f}")
