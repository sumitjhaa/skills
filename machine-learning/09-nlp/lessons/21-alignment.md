# 09.21 Alignment

## Learning Objectives
- Understand RLHF (Reinforcement Learning from Human Feedback)
- Implement PPO and DPO for language model alignment
- Apply reward modelling and KL regularisation
- Analyze alignment tax and capabilities trade-offs

## RLHF Pipeline

### Three Stages
1. **SFT (Supervised Fine-Tuning)**: Train on high-quality demonstrations
2. **Reward Modelling**: Train reward model from human preferences
3. **RL Fine-Tuning**: Optimise policy with PPO using learned reward

### Preference Data
$$y_w \succ y_l \mid x$$

- $y_w$: preferred (chosen) response
- $y_l$: dispreferred (rejected) response

## Reward Modelling

### Bradley-Terry Model
$$p(y_w \succ y_l \mid x) = \frac{\exp(r(x, y_w))}{\exp(r(x, y_w)) + \exp(r(x, y_l))}$$

### Training Loss
$$\mathcal{L}_R = -\mathbb{E}_{(x, y_w, y_l) \sim D} \left[ \log \sigma(r(x, y_w) - r(x, y_l)) \right]$$

### Architecture
- Initialised from SFT model (same size or smaller)
- Remove final unembedding layer → single scalar output

## PPO (Proximal Policy Optimization)

### Objective
$$\mathcal{L}_{\text{PPO}} = \mathbb{E}_{(x, y) \sim \pi_{\theta_{\text{old}}}} \left[ \min\left( \frac{\pi_\theta(y \mid x)}{\pi_{\theta_{\text{old}}}(y \mid x)} A(x, y), \text{clip}(r, 1-\epsilon, 1+\epsilon) A(x, y) \right) \right]$$

### Advantage
$$A(x, y) = r(x, y) - \beta \cdot \text{KL}(\pi_\theta \| \pi_{\text{ref}})$$

- $\beta$: KL penalty coefficient (controls deviation from SFT model)
- $\pi_{\text{ref}}$: frozen SFT model

### Reward Modelling + KL Penalty
$$R(x, y) = r(x, y) - \beta \cdot \text{KL}(\pi_\theta(y \mid x) \| \pi_{\text{SFT}}(y \mid x))$$

## DPO (Direct Preference Optimization)

### Without Explicit Reward Model
$$\mathcal{L}_{\text{DPO}} = -\mathbb{E}_{(x, y_w, y_l) \sim D} \left[ \log \sigma\left( \beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)} \right) \right]$$

### Advantages
- No reward model training
- No PPO training instability
- Simpler, faster, more stable

## Code: DPO Loss

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class DPOLoss(nn.Module):
    def __init__(self, beta=0.1):
        super().__init__()
        self.beta = beta

    def forward(self, policy_chosen_logps, policy_rejected_logps,
                ref_chosen_logps, ref_rejected_logps):
        # Log probabilities for chosen and rejected
        pi_logratios = policy_chosen_logps - policy_rejected_logps
        ref_logratios = ref_chosen_logps - ref_rejected_logps
        logits = pi_logratios - ref_logratios
        loss = -F.logsigmoid(self.beta * logits).mean()
        return loss

def compute_logprobs(model, input_ids, attention_mask):
    logits = model(input_ids, attention_mask=attention_mask).logits
    log_probs = F.log_softmax(logits, dim=-1)
    selected_log_probs = log_probs[:, :-1].gather(
        2, input_ids[:, 1:].unsqueeze(-1)
    ).squeeze(-1)
    return selected_log_probs.sum(dim=-1)
```

## Alignment Tax

### Definition
Reduction in capabilities (MMLU, math, code) from alignment.

| Model | SFT MMLU | RLHF MMLU | Δ |
|-------|---------|-----------|-----|
| LLaMA-2 7B | 45.3 | 44.9 | -0.4 |
| LLaMA-2 13B | 54.8 | 54.0 | -0.8 |
| LLaMA-2 70B | 68.9 | 67.9 | -1.0 |

### Mitigation
- Small KL penalty ($\beta = 0.1-0.2$)
- Mix RLHF data with pretraining data
- Iterated RLHF (multiple rounds of improvement)

## RLHF vs DPO Comparison

| Aspect | PPO (RLHF) | DPO |
|--------|-----------|-----|
| Reward model | Required | Not needed |
| Training stability | Unstable | Stable |
| Compute | 3x SFT | 1.5x SFT |
| Sample efficiency | Lower | Higher |
| Offline data | No | Yes |
| Online data | Yes | Not directly |

## References
- Christiano, Leike, et al., "Deep reinforcement learning from human preferences", NeurIPS 2017
- Stiennon, Ouyang, et al., "Learning to summarize with human feedback", NeurIPS 2020
- Ouyang, Wu, et al., "Training language models to follow instructions with human feedback (InstructGPT)", NeurIPS 2022
- Rafailov, Sharma, et al., "Direct Preference Optimization: Your Language Model is Secretly a Reward Model", NeurIPS 2023
- Bai, Kadavath, et al., "Constitutional AI: Harmlessness from AI Feedback", 2022
