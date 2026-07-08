# 08.29 Visual Reinforcement Learning

## Learning Objectives
- Understand DQN with CNN for vision-based RL
- Implement RT-1 for real-world robotic manipulation
- Apply RT-2 for vision-language-action models
- Analyze challenges in visual generalisation and sample efficiency

## Deep Q-Network (DQN) with Vision

### Architecture
```
CNN(84×84×4 frames → Conv → ReLU → Conv → ReLU → FC) → Q-values (18 actions)
```

### Key Components
- **Experience replay**: Store $(s, a, r, s')$ in buffer, sample batches
- **Target network**: Fixed Q-network for stable targets
- **Frame stacking**: 4 consecutive frames as state (captures motion)

### DQN Loss
$$\mathcal{L} = \mathbb{E}_{(s,a,r,s') \sim \mathcal{D}} \left[ \left( r + \gamma \max_{a'} Q_{\theta^-}(s', a') - Q_\theta(s, a) \right)^2 \right]$$

- $\theta^-$: target network (updated every $C$ steps)
- $\theta$: online network

### Rainbow DQN
Combines 6 improvements: Double DQN, Dueling DQN, Prioritised Replay, Multi-step, Distributional DQN, Noisy Nets.

## RT-1 (Robotics Transformer)

### Architecture
```
Images (6×320×256) → EfficientNet → Tokenised → Transformer encoder (8×64 tokens)
Task instruction → T5 text encoder → Tokenised → Transformer encoder
Decoder → 256 bin action tokens → 11 DOF action
```

### Action Representation
Discretised into 256 bins per dimension:
- Arm: 6-DoF pose (x, y, z, roll, pitch, yaw) + gripper open/close
- Base: Linear + angular velocity
- Mode: Arm control, base control, terminate

### Data Mixing
- 130K+ episodes across 700+ tasks
- 13 robot embodiments (but most data from one robot type)

### Training
- ImageNet-pretrained EfficientNet
- Language-conditioned with T5-small text encoder
- Behaviour cloning (no RL)

## RT-2 (Vision-Language-Action)

### Approach
Fine-tune web-scale VLM (PaLI-X, PaLM-E) on robot data:

1. **Pretrain**: VLM on web-scale (images + text)
2. **Fine-tune**: Add robot action tokens, co-train on VQA + robotics
3. **Action output**: Discrete tokens representing robot actions

### Emergent Generalisation
- **Semantic understanding**: Can manipulate novel objects (e.g., "pick up the extinct animal")
- **Symbolic reasoning**: "Move the apple to the same colour plate"
- **Scene understanding**: "Push the red object to the right and the blue object to the left"

## Challenges

### Visual Generalisation
- Sim-to-real: Render differences (lighting, texture, physics)
- Object appearance: Same object looks different under new lighting
- Background: Cluttered environments confuse policy

### Sample Efficiency
- DQN on Atari: 50M frames (~925 hours of gameplay)
- Robotics: Each episode is expensive (robot time, human supervision)
- Solutions: Data augmentation, sim-to-real, pretrained representations

### Temporal Consistency
- Frame-to-frame action jitter → smooth with action averaging
- Latency: Camera → model → robot must complete within control cycle (100-200ms)

## Code: DQN CNN for Atari

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    def __init__(self, num_actions=18):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(4, 32, 8, stride=4), nn.ReLU(),
            nn.Conv2d(32, 64, 4, stride=2), nn.ReLU(),
            nn.Conv2d(64, 64, 3, stride=1), nn.ReLU(),
        )
        self.fc = nn.Sequential(
            nn.Linear(64 * 7 * 7, 512), nn.ReLU(),
            nn.Linear(512, num_actions),
        )

    def forward(self, x):
        # x: (B, 4, 84, 84) — 4 stacked grayscale frames
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)

    @torch.no_grad()
    def act(self, state, epsilon=0.05):
        if torch.rand(1) < epsilon:
            return torch.randint(0, self.fc[-1].out_features, (1,))
        q_values = self.forward(state)
        return q_values.argmax(dim=1, keepdim=True)
```

## Visual RL Benchmarks

| Benchmark | Domain | Tasks | Success Metric | Notes |
|-----------|--------|-------|---------------|-------|
| Atari (ALE) | Games | 57 | Human-normalised score | 84×84 pixels, discrete actions |
| DM Control Suite | Robotics | 30 | Episode return | Proprioceptive + vision |
| Meta-World | Robotic arm | 50 | Success rate | MT10, MT50 |
| RLBench | Robotic arm | 100 | Success rate | 6-DoF, perception-based |
| Bridge Data | Real robot | 13 | Success rate | Diverse kitchen tasks |
| RT-1 Eval | Real robot | 700 | Success rate | Real kitchen manipulation |

## Practical Considerations
- **Frame skip**: Repeat action for 4 frames to reduce computation
- **Reward normalisation**: Clip rewards to [-1, 1] for stability
- **Data augmentation**: Shift, crop, color jitter for visual generalisation
- **HIL (Human-in-the-loop)**: Use human demonstrations for warm-starting

## References
- Mnih, Kavukcuoglu, et al., "Human-level control through deep reinforcement learning", Nature 2015
- Hessel, Modayil, et al., "Rainbow: Combining Improvements in Deep Reinforcement Learning", AAAI 2018
- Brohan, Brown, et al., "RT-1: Robotics Transformer for Real-World Control at Scale", RSS 2023
- Brohan, Brown, et al., "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control", 2023
- Kalashnikov, Irpan, et al., "QT-Opt: Scalable Deep Reinforcement Learning for Vision-Based Robotic Manipulation", CoRL 2018
