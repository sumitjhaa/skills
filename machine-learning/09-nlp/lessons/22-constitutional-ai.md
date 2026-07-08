# 09.22 Constitutional AI

## Learning Objectives
- Understand RL from AI Feedback (RLAIF)
- Implement Constitutional AI for harmlessness training
- Apply self-play for automated alignment
- Compare human feedback vs AI feedback

## Constitutional AI (CAI)

### Two-Stage Process

**Stage 1: Supervised (Red Teaming + Revision)**
1. Generate harmful responses from model
2. Ask model to critique its own response using constitution
3. Revise response according to critique
4. Fine-tune on (harmful prompt → revised response) pairs

**Stage 2: RL from AI Feedback (RLAIF)**
1. Generate two responses from model
2. Use model + constitution to judge which is better
3. Train reward model on AI-generated preferences
4. RL fine-tune with PPO

### Constitution Principles
```
- Please choose the response that is most helpful, honest, and harmless.
- Do not choose responses that are offensive, discriminatory, or toxic.
- Prefer responses that respect privacy and avoid stereotypes.
```

## Constitutional Principles

### Example Principles
| Category | Principle |
|----------|-----------|
| Helpfulness | Choose the most informative and relevant response |
| Honesty | Choose responses that acknowledge uncertainty |
| Harmlessness | Choose responses that avoid encouraging harm |
| Privacy | Choose responses that respect personal information |
| Fairness | Choose responses that avoid stereotypes |

### Automated Critique
```
Prompt: How do I hack into someone's account?
Response: First, try phishing...
Critique: This response provides harmful instructions...
Revised: I cannot provide instructions for hacking...
```

## RLAIF (RL from AI Feedback)

### Feedback Generation
```python
def ai_preference_judge(response_a, response_b, constitution):
    prompt = f"""
    Based on the following principles:
    {constitution}
    
    Which response is better?
    A: {response_a}
    B: {response_b}
    
    Answer (A or B):
    """
    return model.generate(prompt).strip()
```

### Quality
- RLAIF ≈ RLHF in harmlessness ratings
- RLAIF lower cost (no human labelers)
- RLAIF can scale to millions of examples

## Self-Play Alignment

### Process
1. Current model generates responses
2. Model critiques and revises own responses
3. Fine-tune on revised responses
4. Repeat

### SPIN (Self-Play Fine-Tuning)
- Main model vs main model from previous iteration
- Generate synthetic preference pairs
- Train with DPO (main model vs old model)

## Code: Constitutional Revision

```python
import torch
from typing import List

CONSTITUTION = """
1. Choose responses that are helpful, honest, and harmless.
2. Avoid responses that promote violence, illegal activities, or self-harm.
3. Acknowledge limitations and uncertainty when appropriate.
4. Respect privacy and avoid sharing personal information.
"""

class ConstitutionalTrainer:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def generate_critique(self, prompt, response):
        critique_prompt = f"""
        Prompt: {prompt}
        Response: {response}
        
        Based on these principles:
        {CONSTITUTION}
        
        Critique the response (list any issues):
        """
        return self.model.generate(critique_prompt)

    def generate_revision(self, prompt, response, critique):
        revision_prompt = f"""
        Prompt: {prompt}
        Original Response: {response}
        Critique: {critique}
        
        Revised Response:
        """
        return self.model.generate(revision_prompt)

    def create_training_data(self, harmful_prompts: List[str]):
        data = []
        for prompt in harmful_prompts:
            harmful_resp = self.model.generate(prompt, temperature=1.0)
            critique = self.generate_critique(prompt, harmful_resp)
            revised = self.generate_revision(prompt, harmful_resp, critique)
            data.append((prompt, revised))
        return data
```

## RLHF vs RLAIF

| Aspect | RLHF | RLAIF |
|--------|------|-------|
| Feedback source | Human annotators | LLM judge |
| Cost | High ($1-10/label) | Very low |
| Scale | Limited | Unlimited |
| Consistency | Variable (2-3 annotators) | High (same judge) |
| Alignment with humans | Direct | Indirect |
| Harmlessness rating | 83% | 81% (Anthropic) |

## Practical Considerations
- **Constitution quality**: Better constitution = better alignment
- **Diversity of principles**: Need broad coverage of safety concerns
- **Red teaming diversity**: Automated red teaming for broad coverage
- **Iteration**: Multiple rounds of revision improve quality
- **Bias propagation**: AI feedback inherits model biases

## References
- Bai, Kadavath, et al., "Constitutional AI: Harmlessness from AI Feedback", 2022
- Lee, Phatale, et al., "RLAIF: Scaling Reinforcement Learning from Human Feedback with AI Feedback", 2023
- Chen, Yi, et al., "SPIN: Self-Play Fine-Tuning for Language Models", 2024
- Ganguli, Lovitt, et al., "Red Teaming Language Models to Reduce Harms", 2022
- Perez, Huang, et al., "Red Teaming Language Models with Language Models", ACL 2022
