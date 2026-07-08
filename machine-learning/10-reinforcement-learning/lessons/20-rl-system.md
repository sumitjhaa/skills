# Lesson 10.20: RL System Design

## Learning Objectives
- Understand end-to-end RL system architecture
- Implement scalable training pipelines
- Apply monitoring and evaluation infrastructure

## System Architecture

### Components
```
Environment (sim/real) → Agent (policy/value) → Training loop → Monitoring
```

### Training Loop
```python
class RLTrainer:
    def __init__(self, agent, env, config):
        self.agent = agent
        self.env = env
        self.config = config
        self.metrics = defaultdict(list)

    def train_episode(self):
        state = self.env.reset()
        episode_data = []
        done = False
        while not done:
            action = self.agent.act(state)
            next_state, reward, done = self.env.step(action)
            episode_data.append((state, action, reward, next_state, done))
            state = next_state
        return episode_data

    def run(self):
        for episode in range(self.config.episodes):
            data = self.train_episode()
            self.agent.update(data)
            total_reward = sum(d[2] for d in data)
            self.metrics['reward'].append(total_reward)
            if episode % 100 == 0:
                self.evaluate()
        return self.metrics
```

## Distributed RL

### A3C Architecture
```
Worker 1 ─┐
Worker 2 ─┤
Worker 3 ─┤── Global network (shared parameters)
Worker 4 ─┤
Worker 5 ─┘
```

### IMPALA
- Distributed actors + centralized learner
- V-trace off-policy correction

## Monitoring

### Key Metrics
| Metric | What it Measures | Target |
|--------|-----------------|--------|
| Episode reward | Task performance | Higher = better |
| Episode length | Efficiency | Variable |
| Loss | Learning signal | Decreasing |
| Q-values | Value estimates | Stable |
| Entropy | Exploration | > 0 |
| KL divergence | Policy change | < threshold |

## Code: RL Training Infrastructure

```python
import wandb
import torch
from collections import deque

class RLSystem:
    def __init__(self, agent, env_fn, config):
        self.agent = agent
        self.env_fn = env_fn
        self.config = config
        self.replay_buffer = deque(maxlen=config.buffer_size)
        self.best_reward = -float('inf')

    def evaluate(self, num_episodes=10):
        env = self.env_fn()
        eval_rewards = []
        for _ in range(num_episodes):
            state = env.reset()
            total_reward = 0
            done = False
            while not done:
                action = self.agent.act(state, deterministic=True)
                state, reward, done = env.step(action)
                total_reward += reward
            eval_rewards.append(total_reward)
        return np.mean(eval_rewards)

    def train(self):
        env = self.env_fn()
        state = env.reset()
        episode_reward = 0
        episode_length = 0
        episode = 0
        
        for step in range(self.config.total_steps):
            # Collect experience
            action = self.agent.act(state)
            next_state, reward, done = env.step(action)
            self.replay_buffer.append((state, action, reward, next_state, done))
            state = next_state
            episode_reward += reward
            episode_length += 1

            # Train
            if len(self.replay_buffer) > self.config.batch_size:
                batch = random.sample(self.replay_buffer, self.config.batch_size)
                loss = self.agent.update(batch)

                if self.config.use_wandb:
                    wandb.log({
                        "loss": loss,
                        "buffer_size": len(self.replay_buffer),
                        "steps": step,
                    })

            # End of episode
            if done:
                self.metrics['train_reward'].append(episode_reward)
                state = env.reset()
                episode_reward = 0
                episode_length = 0
                episode += 1

            # Evaluation
            if step % self.config.eval_interval == 0:
                eval_reward = self.evaluate()
                if eval_reward > self.best_reward:
                    self.best_reward = eval_reward
                    torch.save(self.agent.state_dict(), "best_model.pt")
                print(f"Step {step}: Eval reward = {eval_reward:.2f}")

                if self.config.use_wandb:
                    wandb.log({
                        "eval_reward": eval_reward,
                        "best_reward": self.best_reward,
                        "episode": episode,
                    })
```

## Training Configuration

```yaml
# config.yaml
agent: "PPO"
environment: "HalfCheetah-v2"
total_steps: 1000000
batch_size: 256
learning_rate: 3e-4
gamma: 0.99
lambda: 0.95
clip_epsilon: 0.2
entropy_coef: 0.01
value_coef: 0.5
max_grad_norm: 0.5
num_envs: 8
eval_interval: 10000
buffer_size: 1000000
use_wandb: true
```

## Infrastructure Considerations

| Component | Implementation | Purpose |
|-----------|---------------|---------|
| Environment | Gym/Bullet/Isaac | Simulation |
| Agent | PyTorch/TF | Policy + value |
| Buffer | Replay buffer | Experience storage |
| Logger | Wandb/MLflow | Metrics |
| Checkpoint | Torch save | Model persistence |
| Config | YAML/JSON | Hyperparameters |
| CI/CD | GitHub Actions | Testing |

## References
- Mnih, Badia, et al., "Asynchronous Methods for Deep Reinforcement Learning (A3C)", ICML 2016
- Espeholt, Soyer, et al., "IMPALA: Scalable Distributed Deep-RL with Importance Weighted Actor-Learner Architectures", ICML 2018
- Nair, Srinivasan, et al., "Massively Parallel Methods for Deep Reinforcement Learning", 2015
- Cobbe, Hilton, et al., "Leveraging Procedural Generation to Benchmark Reinforcement Learning (Procgen)", ICML 2020
- Kostrikov, "PyTorch Implementation of Reinforcement Learning Algorithms", 2018
