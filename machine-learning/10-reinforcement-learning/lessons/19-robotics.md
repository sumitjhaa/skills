# Lesson 10.19: Robotics

## Learning Objectives
- Understand RL for robotic manipulation and locomotion
- Implement sim-to-real transfer techniques
- Apply domain randomisation for robust policy transfer

## Challenges in Robot RL

### Real-World Constraints
- Sample efficiency: Robot time is expensive
- Safety: Damaging hardware during exploration
- Sim-to-real gap: Simulation ≠ reality

## Sim-to-Real Transfer

### Domain Randomisation
Randomise simulation parameters during training:

```python
def randomise_sim_params():
    return {
        "friction": uniform(0.5, 2.0),
        "mass": uniform(0.8, 1.2),
        "motor_strength": uniform(0.8, 1.5),
        "observation_noise": uniform(0.0, 0.05),
        "delay": uniform(0, 3),  # action delay in frames
        "gravity": uniform(9.0, 10.0),
    }
```

## Manipulation

### Grasping Pipeline
```
Camera → Object detection → Pose estimation → Grasp planning → Control
```

### RL for Grasping
- State: Joint angles + object pose + camera image
- Action: End-effector velocity + gripper command
- Reward: Distance to object + grasp success

## Locomotion

### Reward Design
$$r = v_{\text{forward}} - c_1 \cdot \text{energy} - c_2 \cdot \text{jerk}$$

- Forward velocity: Encourages movement
- Energy penalty: Discourages wasted effort
- Smoothness: Reduces mechanical wear

## Code: Robot Policy with Domain Randomisation

```python
import numpy as np

class SimToRealPolicy:
    def __init__(self, policy, env):
        self.policy = policy
        self.env = env
        self.domain_params = {}

    def randomise_dynamics(self):
        self.domain_params = {
            "friction": np.random.uniform(0.5, 2.0),
            "mass_scale": np.random.uniform(0.8, 1.2),
            "motor_noise": np.random.uniform(0.0, 0.1),
            "latency": np.random.randint(0, 3),
        }
        self.env.set_params(**self.domain_params)

    def train_step(self, batch_size=1024):
        self.randomise_dynamics()
        states, actions, rewards, dones = [], [], [], []
        state = self.env.reset()
        for _ in range(1000):
            action = self.policy(state) + np.random.normal(0, 0.1, size=state.shape[:1])
            next_state, reward, done = self.env.step(action)
            states.append(state)
            actions.append(action)
            rewards.append(reward)
            dones.append(done)
            state = next_state
            if done:
                break
        return states, actions, rewards

    def deploy_real(self, state, history=None):
        # Zero-shot transfer to real robot
        action = self.policy(state)
        return action


class RobotEnv:
    def __init__(self, sim=True):
        self.sim = sim

    def set_params(self, friction=1.0, mass_scale=1.0, motor_noise=0.0, latency=0):
        if self.sim:
            self.physics_client.changeDynamics(
                self.robot_id, -1, lateralFriction=friction
            )
            with self.physics_client:
                for joint in self.joints:
                    self.physics_client.changeDynamics(
                        self.robot_id, joint, mass=mass_scale * self.base_mass
                    )

    def step(self, action):
        if self.sim:
            # Add motor noise
            noisy_action = action + np.random.normal(0, 0.01, size=action.shape)
            self.physics_client.setJointMotorControlArray(
                self.robot_id, self.joints,
                controlMode=self.physics_client.POSITION_CONTROL,
                targetPositions=noisy_action,
            )
            for _ in range(50):  # Run physics
                self.physics_client.stepSimulation()
        return self.get_observation(), self.get_reward(), self.is_done()
```

## Key Techniques

| Technique | Purpose | Example |
|-----------|---------|---------|
| Domain randomisation | Robustness to sim-to-real | Friction, mass, delay |
| System identification | Match sim to real | Calibrate dynamics |
| Randomise dynamics | Range of environments | Vary all parameters |
| Noise injection | Sensor noise tolerance | Gaussian observation noise |
| Action delays | Communication latency | Random frame delay |
| Asymmetric actor-critic | Real-world deployment | State noise only |

## Robot RL Benchmarks

| Benchmark | Tasks | Simulator | Metric |
|-----------|-------|-----------|--------|
| D4RL | 40+ tasks | MuJoCo | Normalised score |
| Meta-World | 50 tasks | MuJoCo | Success rate |
| RLBench | 100 tasks | PyBullet | Success rate |
| Isaac Gym | 100+ tasks | Isaac Sim | Reward |
| ManiSkill | Manipulation | SAPIEN | Success rate |

## References
- Tobin, Fong, et al., "Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World", IROS 2017
- Levine, Pastor, et al., "Learning Hand-Eye Coordination for Robotic Grasping with Deep Learning", ICRA 2016
- Kumar, Todorov, Levine, "Sim-to-Real Transfer of Robotic Control with Dynamics Randomization", ICLR 2016
- Andrychowicz, Baker, et al., "Learning Dexterous In-Hand Manipulation (Dactyl)", RSS 2018
- Peng, Andrychowicz, et al., "Sim-to-Real Transfer of Robotic Control with Simulation-Based Inference", CoRL 2018
