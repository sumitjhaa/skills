"""10.19 Robotics: manipulation, locomotion, sim-to-real."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

np.random.seed(42)

n_dof = 7
n_timesteps = 200

target_pos = np.random.randn(n_dof) * 0.5
joint_pos = np.zeros((n_timesteps, n_dof))
joint_vel = np.zeros((n_timesteps, n_dof))

Kp, Kd = 5.0, 1.0
for t in range(1, n_timesteps):
    error = target_pos - joint_pos[t-1]
    acc = Kp * error - Kd * joint_vel[t-1]
    joint_vel[t] = joint_vel[t-1] + acc * 0.01
    joint_pos[t] = joint_pos[t-1] + joint_vel[t] * 0.01

torques = Kp * (target_pos[None, :] - joint_pos) - Kd * joint_vel

sim_params = np.array([0.5, 0.8, 0.2])
real_params = sim_params + np.random.randn(3) * 0.1
domain_randomized = []
for _ in range(20):
    randomized = sim_params + np.random.randn(3) * 0.15
    domain_randomized.append(randomized)

n_contacts = 4
contact_forces = np.random.rand(n_contacts, n_timesteps) * 5
gripper_pos = 0.5 * (1 + np.sin(np.linspace(0, 4*np.pi, n_timesteps)))

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

for i in range(min(3, n_dof)):
    axes[0, 0].plot(joint_pos[:, i], lw=2, label=f"Joint {i}")
axes[0, 0].axhline(target_pos[0], color="k", ls="--", alpha=0.5, label="Target")
axes[0, 0].set_xlabel("Time step")
axes[0, 0].set_ylabel("Joint position (rad)")
axes[0, 0].set_title("PD Control: Joint Position\nTrajectory Tracking")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

for i in range(min(3, n_dof)):
    axes[0, 1].plot(torques[:, i], lw=2, label=f"Joint {i}")
axes[0, 1].set_xlabel("Time step")
axes[0, 1].set_ylabel("Torque (Nm)")
axes[0, 1].set_title("Control Torques")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

dr_array = np.array(domain_randomized)
for i in range(dr_array.shape[1]):
    axes[0, 2].hist(dr_array[:, i], bins=10, alpha=0.5, label=f"Param {i}")
axes[0, 2].set_xlabel("Parameter value")
axes[0, 2].set_ylabel("Count")
axes[0, 2].set_title("Domain Randomization\nDistribution")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

axes[1, 0].plot(contact_forces.T, lw=1.5)
axes[1, 0].set_xlabel("Time step")
axes[1, 0].set_ylabel("Contact force (N)")
axes[1, 0].set_title("Contact Forces\n(during manipulation)")
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(gripper_pos, "b-", lw=2)
axes[1, 1].axhline(0.5, color="gray", ls="--", alpha=0.5)
axes[1, 1].set_xlabel("Time step")
axes[1, 1].set_ylabel("Gripper opening")
axes[1, 1].set_title("Gripper Control\n(open/close)")
axes[1, 1].grid(True, alpha=0.3)

sim_real_gap = np.abs(np.array([0.5, 0.8, 0.2]) - real_params)
axes[1, 2].bar(range(3), [0.5, 0.8, 0.2], alpha=0.7, label="Sim")
axes[1, 2].bar(range(3), real_params, alpha=0.5, label="Real")
axes[1, 2].set_xlabel("Parameter")
axes[1, 2].set_ylabel("Value")
axes[1, 2].set_title("Sim-to-Real Gap\n(Domain Randomization helps)")
axes[1, 2].legend()
axes[1, 2].grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase10/19-robotics.png")
plt.close()

print("=" * 60)
print("ROBOTICS")
print("=" * 60)
print(f"\nRobot arm: {n_dof} DOF, PD control")
print(f"  Target: {np.round(target_pos, 2)}")
final_error = np.linalg.norm(joint_pos[-1] - target_pos)
print(f"  Final joint error: {final_error:.4f} rad")
max_torque = np.max(np.abs(torques))
print(f"  Max torque: {max_torque:.2f} Nm")

print(f"\nContact forces:")
for i in range(n_contacts):
    print(f"  Contact {i}: max {contact_forces[i].max():.2f} N")

print(f"\nSim-to-Real gap:")
for i in range(3):
    print(f"  Param {i}: sim={[0.5, 0.8, 0.2][i]:.2f}, "
          f"real={real_params[i]:.2f}, gap={sim_real_gap[i]:.4f}")

print(f"\nKey concepts:")
print(f"  • Manipulation: grasping, in-hand dexterity")
print(f"  • Locomotion: walking, running (legged robots)")
print(f"  • Control: PD, computed torque, impedance")
print(f"  • Domain randomization: sim params → real robust")
print(f"  • Sim-to-Real: bridge the reality gap")
print(f"  • RL for robotics: PPO, SAC, DRL-based control")
