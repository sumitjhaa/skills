"""10.13 Hierarchical RL: Options framework on a two-room grid."""
import numpy as np

GRID = 5
GAMMA = 0.9
ALPHA = 0.1
EPS = 0.1
EPISODES = 200

# Two rooms: left room (cols 0-1), right room (cols 2-4)
# Door at (2, 2), goal at (4, 4)
N_STATES = GRID * GRID
N_OPTIONS = 2  # 0: go-left-room, 1: go-right-room


def state_to_room(s):
    c = s % GRID
    return 0 if c <= 1 else 1


class Option:
    def __init__(self, target_room):
        self.target_room = target_room
        self.Q = np.zeros((N_STATES, 4))
        self.termination = np.zeros(N_STATES)

    def act(self, s, eps):
        if np.random.rand() < eps:
            return np.random.randint(4)
        return np.argmax(self.Q[s])

    def update(self, s, a, r, ns, done):
        self.Q[s, a] += ALPHA * (r + GAMMA * np.max(self.Q[ns]) * (1 - done) - self.Q[s, a])


options = [Option(0), Option(1)]

# Meta-controller
meta_Q = np.zeros((N_STATES, N_OPTIONS))

for ep in range(EPISODES):
    s = np.random.randint(N_STATES)
    total_r = 0
    for _ in range(50):
        if np.random.rand() < EPS:
            o = np.random.randint(N_OPTIONS)
        else:
            o = np.argmax(meta_Q[s])
        option = options[o]
        # Execute option for up to 5 steps
        step_in_option = 0
        while step_in_option < 5:
            a = option.act(s, 0.05)
            r, c = s // GRID, s % GRID
            dr, dc = [(0, -1), (0, 1), (1, 0), (-1, 0)][a]
            nr, nc = r + dr, c + dc
            if 0 <= nr < GRID and 0 <= nc < GRID:
                ns = nr * GRID + nc
            else:
                ns = s
            reward = 0
            if ns == GRID * GRID - 1:
                reward = 10
            option.update(s, a, reward, ns, reward > 0)
            if reward > 0:
                meta_Q[s, o] += 0.1 * (reward - meta_Q[s, o])
                s = ns
                total_r += reward
                break
            s = ns
            step_in_option += 1
            total_r += reward
            if reward > 0:
                break
        else:
            meta_Q[s, o] += 0.1 * (total_r - meta_Q[s, o])
    if ep % 50 == 0:
        print(f"Ep {ep}, return: {total_r}")

print("HRL options framework complete.")
