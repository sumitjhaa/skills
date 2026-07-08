# Lesson 10.16: RLHF (Reinforcement Learning from Human Feedback)

## Learning Objectives
- Understand the RLHF pipeline for LLM alignment
- Implement reward modelling from human preferences
- Apply PPO for fine-tuning with learned reward

## RLHF Pipeline

### Three Stages
1. **SFT (Supervised Fine-Tuning)**: Train on high-quality demonstrations
2. **Reward Modelling**: Train reward model from human preferences
3. **PPO Fine-Tuning**: Optimise policy against reward with KL constraint

## Reward Model Training

### Bradley-Terry Preference Model
$$p(y_1 \succ y_2 \mid x) = \frac{\exp(r(x, y_1))}{\exp(r(x, y_1)) + \exp(r(x, y_2))}$$

### Loss
$$\mathcal{L}_R = -\mathbb{E}_{(x, y_w, y_l)} [\log \sigma(r(x, y_w) - r(x, y_l))]$$

## PPO for RLHF

### PPO Objective
$$\pi = \arg\max_\pi \mathbb{E}_{x \sim D, y \sim \pi(y|x)} [r(x, y) - \beta \cdot \text{KL}(\pi \| \pi_{\text{ref}})]$$

### KL Penalty
Controls deviation from reference model:
- Prevents reward hacking
- Maintains generation quality

## Code: Reward Model

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class RewardModel(nn.Module):
    def __init__(self, base_model, dropout=0.1):
        super().__init__()
        self.base = base_model
        self.reward_head = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(base_model.config.hidden_size, 1),
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.base(input_ids, attention_mask=attention_mask)
        hidden = outputs.last_hidden_state[:, 0, :]  # [CLS] token
        return self.reward_head(hidden).squeeze(-1)

    def preference_loss(self, chosen_ids, chosen_mask, rejected_ids, rejected_mask):
        r_chosen = self(chosen_ids, chosen_mask)
        r_rejected = self(rejected_ids, rejected_mask)
        loss = -F.logsigmoid(r_chosen - r_rejected).mean()
        acc = (r_chosen > r_rejected).float().mean()
        return loss, acc


class PPOForRLHF:
    def __init__(self, policy, ref_policy, reward_model, kl_coef=0.1):
        self.policy = policy
        self.ref_policy = ref_policy
        self.reward = reward_model
        self.kl_coef = kl_coef
        self.optim = torch.optim.AdamW(policy.parameters(), lr=1e-5)

    def compute_kl(self, input_ids, attention_mask):
        with torch.no_grad():
            ref_logits = self.ref_policy(input_ids, attention_mask).logits
        policy_logits = self.policy(input_ids, attention_mask).logits
        kl = (policy_logits.softmax(-1) * 
              (policy_logits.log_softmax(-1) - ref_logits.log_softmax(-1))
             ).sum(-1).mean()
        return kl

    def update(self, input_ids, attention_mask):
        # Compute rewards
        rewards = self.reward(input_ids, attention_mask)
        kl = self.compute_kl(input_ids, attention_mask)
        augmented_rewards = rewards - self.kl_coef * kl
        
        # PPO update
        logits = self.policy(input_ids, attention_mask).logits
        log_probs = logits.log_softmax(-1)
        loss = -(log_probs.mean() * augmented_rewards.detach()).mean()
        
        self.optim.zero_grad()
        loss.backward()
        self.optim.step()
        return loss.item()
```

## Human Feedback Data

### Collection
- Pairwise comparisons: $N$ annotators rank $K$ responses
- Quality criteria: Helpfulness, honesty, harmlessness
- Cost: $1-10 per label

### Dataset Sizes
| Model | Comparison Pairs |
|-------|-----------------|
| InstructGPT | 33K |
| LLaMA-2 | 1M |
| Claude | 100K+ |

## References
- Christiano, Leike, et al., "Deep Reinforcement Learning from Human Preferences", NeurIPS 2017
- Stiennon, Ouyang, et al., "Learning to Summarize with Human Feedback", NeurIPS 2020
- Ouyang, Wu, et al., "Training Language Models to Follow Instructions with Human Feedback (InstructGPT)", NeurIPS 2022
- Bai, Kadavath, et al., "Constitutional AI: Harmlessness from AI Feedback", 2022
- Rafailov, Sharma, et al., "Direct Preference Optimization: Your Language Model is Secretly a Reward Model", NeurIPS 2023
