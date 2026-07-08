"""10.03 Monte Carlo: First-visit MC control (Blackjack)."""
import numpy as np

ACTIONS = [0, 1]  # 0=stick, 1=hit


def draw():
    return min(np.random.randint(1, 14), 10)


def hand_value(hand):
    s = sum(hand)
    if 1 in hand and s + 10 <= 21:
        s += 10
    return s


def step(state, action):
    ps, pd = state
    if action == 1:
        card = draw()
        val = ps + card
        if val > 21:
            return None, -1, True
        return (val, pd), 0, False
    else:
        dh = [pd]
        while hand_value(dh) < 17:
            dh.append(draw())
        dv = hand_value(dh)
        if dv > 21 or ps > dv:
            return None, 1, True
        elif ps == dv:
            return None, 0, True
        else:
            return None, -1, True


n_states = 18 * 10
Q = np.zeros((n_states, 2))
returns = [[[] for _ in range(2)] for _ in range(n_states)]


def sidx(ps, pd):
    return (ps - 4) * 10 + (pd - 2)


for ep in range(20000):
    ps = np.random.randint(4, 22)
    pd = np.random.randint(2, 12)
    s = (ps, pd)
    traj = []
    for _ in range(50):
        idx = sidx(s[0], s[1])
        a = np.argmax(Q[idx]) if np.random.rand() > 0.1 else np.random.choice(ACTIONS)
        ns, r, done = step(s, a)
        traj.append((idx, a, r))
        if done:
            break
        s = ns
    G = 0
    seen = set()
    for idx, a, r in reversed(traj):
        G = 0.9 * G + r
        if (idx, a) not in seen:
            seen.add((idx, a))
            returns[idx][a].append(G)
            Q[idx][a] = np.mean(returns[idx][a])
    if ep % 5000 == 0:
        print(f"Episode {ep}")

print("MC Control done.")
for ps in [18, 20]:
    for pd in [2, 6, 10]:
        idx = sidx(ps, pd)
        print(f"Player={ps}, Dealer={pd}: stick={Q[idx,0]:.3f}, hit={Q[idx,1]:.3f}")
