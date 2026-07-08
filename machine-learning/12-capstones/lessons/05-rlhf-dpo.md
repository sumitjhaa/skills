# Lesson 12.05: RLHF / DPO from Scratch

## Project Architecture

Implement Reinforcement Learning from Human Feedback (RLHF) using Direct Preference Optimization (DPO) and train a language model to follow instructions.

```
Phase 1: Supervised Fine-Tuning (SFT)
  Pretrained LM → Finetune on high-quality demonstrations
  Loss: standard cross-entropy on response tokens

Phase 2: Preference Data
  Generate pairs (y_w, y_l) from same prompt
  Human/comparison: "which response is better?"

Phase 3a: RLHF (PPO)
  ├── Train reward model: r_φ(x, y) from preference pairs
  │    Loss: -log σ(r_φ(x, y_w) - r_φ(x, y_l))
  ├── Optimize policy: π_θ against reward model
  │    Loss: -E[r_φ(x, y)] + β KL(π_θ || π_ref)
  │    Using PPO with value function

Phase 3b: DPO (simpler alternative)
  No reward model needed!
  Loss: -log σ(β log(π_θ(y_w|x)/π_ref(y_w|x))
                - β log(π_θ(y_l|x)/π_ref(y_l|x)))
```

## Design Decisions

### Data
- Create synthetic preference data: for each prompt, generate two responses and label based on length/quality heuristics
- Or use the Anthropic HH-RLHF dataset (preference pairs)

### DPO (Direct Preference Optimization)
- Avoids training a separate reward model
- Directly optimizes the policy using preference pairs
- Key insight: the optimal reward is implicit in the policy ratio
- Loss: `-log σ(β (log π_θ(y_w|x) - log π_ref(y_w|x) - log π_θ(y_l|x) + log π_ref(y_l|x)))`

### PPO implementation (for comparison)
- Reward model: a transformer with a scalar head
- PPO clip objective with value function (critic)
- KL penalty to prevent policy from diverging too far

### Evaluation
- Track reward model score
- Track KL divergence from reference policy
- Generate samples before/after alignment
- Compute win-rate against SFT baseline

## Implementation Guide

1. **Implement the base transformer** (reuse from project 12.02)
2. **Implement SFT training** on instruction-following data
3. **Create synthetic preference data** or load HH-RLHF
4. **Implement DPO loss**
5. **Train DPO** on preference pairs
6. **Implement reward model** (transformer with scalar head)
7. **Implement PPO** with KL penalty and value function
8. **Train PPO** on same preference data
9. **Compare DPO vs. PPO** (samples, KL, simplicity)
10. **Generate and evaluate aligned samples**

## Key Insights

- DPO eliminates the need for a separate reward model, simplifying the pipeline
- The implicit reward in DPO is `r(x,y) = β log(π_θ(y|x) / π_ref(y|x)) + constant`
- PPO requires 4 models (policy, ref, reward, value); DPO needs 2 (policy, ref)
- KL penalty in both approaches prevents the model from gaming the reward
- Preference-based alignment is sensitive to data quality and labeling noise
