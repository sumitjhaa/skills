#!/usr/bin/env python3
"""03.28 State Space / Kalman Filter: 1D tracking with Kalman filter."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# True trajectory
n_steps = 100
dt = 1.0
true_pos = np.cumsum(np.random.normal(0, 0.5, n_steps))
obs = true_pos + np.random.normal(0, 1.0, n_steps)  # noisy observations

# Kalman filter (position-velocity model)
F = np.array([[1, dt], [0, 1]])  # state transition
H = np.array([[1, 0]])  # observation matrix
Q = np.array([[0.1, 0], [0, 0.1]])  # process noise
R = np.array([[1.0]])  # observation noise

x = np.zeros((2, 1))  # [pos, vel]
P = np.eye(2) * 10  # initial uncertainty

positions = np.zeros(n_steps)
velocities = np.zeros(n_steps)
P_hist = np.zeros(n_steps)

for t in range(n_steps):
    # Predict
    x = F @ x
    P = F @ P @ F.T + Q
    
    # Update
    y = obs[t] - H @ x
    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)
    x = x + K @ y
    P = (np.eye(2) - K @ H) @ P
    
    positions[t] = x[0, 0]
    velocities[t] = x[1, 0]
    P_hist[t] = P[0, 0]

plt.figure(figsize=(12, 6))
plt.plot(true_pos, 'g-', lw=2, label="True position")
plt.plot(obs, 'ko', alpha=0.3, label="Observations")
plt.plot(positions, 'r-', lw=2, label="Kalman estimate")
# Confidence band
plt.fill_between(range(n_steps), positions - 2*np.sqrt(P_hist), 
                  positions + 2*np.sqrt(P_hist), alpha=0.2, color='r', label="95% CI")
plt.xlabel("Time step")
plt.ylabel("Position")
plt.title("Kalman Filter: 1D Tracking")
plt.legend()
plt.grid(True)
plt.savefig("../../assets/phase03/28-state-space-kalman.png")
plt.close()

print(f"Position MSE: {np.mean((positions - true_pos)**2):.3f}")
print(f"Observation MSE: {np.mean((obs - true_pos)**2):.3f}")
print("Kalman filter reduces noise by", 
      f"{100*(1 - np.mean((positions - true_pos)**2)/np.mean((obs - true_pos)**2)):.0f}%")
