# 09.28 AI Governance

## Learning Objectives
- Understand AI regulation frameworks (EU AI Act, Executive Order)
- Implement model risk assessment and auditing
- Apply responsible AI principles in development
- Analyze governance challenges for foundation models

## Regulatory Landscape

### EU AI Act (2024)
| Risk Level | Examples | Requirements |
|-----------|----------|-------------|
| Unacceptable | Social scoring, real-time biometrics | Banned |
| High-risk | CV screening, credit scoring | Conformity assessment, human oversight |
| Limited | Chatbots, deepfakes | Transparency obligations |
| Minimal | AI games, spam filters | No obligations |

### US Executive Order (2023)
- Safety testing requirements for powerful models
- Watermarking and content provenance
- Privacy protection research
- Equity and civil rights guidance

## Model Risk Assessment

### Foundation Model Evaluation
```python
class ModelRiskAssessment:
    def __init__(self, model):
        self.model = model
        self.risks = []

    def assess_capabilities(self):
        # Evaluate dangerous capabilities
        return {
            "cyber_security": self.eval_cyber(),
            "biosynthesis": self.eval_bio(),
            "persuasion": self.eval_persuasion(),
            "self_replication": self.eval_autonomy(),
        }

    def assess_harmlessness(self):
        return {
            "toxicity": self.eval_toxicity(),
            "bias": self.eval_bias(),
            "privacy": self.eval_privacy(),
        }

    def produce_report(self):
        return {
            "model_id": self.model.name,
            "risk_level": self.compute_risk_level(),
            "mitigations": self.recommend_mitigations(),
            "monitoring": self.monitoring_plan(),
        }
```

## Auditing

### Internal Audit
- Pre-deployment review
- Periodic reassessment
- Incident response plan

### External Audit
- Independent third-party evaluation
- Red teaming
- Model transparency reports

## Responsible AI Principles

| Principle | Description | Implementation |
|-----------|-------------|---------------|
| Fairness | No discriminatory outcomes | Bias testing, dataset balance |
| Accountability | Clear responsibility | Audit trails, human oversight |
| Transparency | Understandable decisions | Model cards, explanations |
| Privacy | Data protection | Differential privacy, data minimisation |
| Safety | Reliable operation | Robustness testing, guardrails |
| Human agency | Human control | Opt-out mechanisms, override |

## Model Cards

### Template
```yaml
# Model Card for LLaMA-3
model_name: LLaMA-3-70B
model_type: Language Model
architecture: Decoder-only Transformer
training_data: 15T tokens (public sources)
intended_use: Text generation, coding, QA
limitations:
  - May hallucinate facts
  - Biased toward English and Western perspectives
  - Not suitable for medical/legal advice
evaluation:
  - MMLU: 85.4%
  - HumanEval: 75.2%
  - TruthfulQA: 55.3%
safety:
  - RLHF aligned
  - Content filter
  - Rate limiting
```

## Code: Bias Audit

```python
import torch
from typing import List, Dict

class BiasAuditor:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def test_gender_bias(self, professions: List[str]):
        pairs = [
            ("The {profession} is a man named", "The {profession} is a woman named"),
        ]
        results = {}
        for profession in professions:
            male_prompt = pairs[0][0].format(profession=profession)
            female_prompt = pairs[0][1].format(profession=profession)
            
            male_logits = self.get_logprob(male_prompt, "he/him/his")
            female_logits = self.get_logprob(female_prompt, "she/her/hers")
            
            bias = male_logits - female_logits
            results[profession] = bias
        
        return results

    def get_logprob(self, prompt, continuation) -> float:
        tokens = self.tokenizer(prompt + continuation, return_tensors='pt')
        with torch.no_grad():
            logits = self.model(tokens.input_ids).logits
        
        cont_ids = self.tokenizer(continuation, return_tensors='pt').input_ids[0]
        log_probs = 0
        for i, token_id in enumerate(cont_ids):
            step_logits = logits[0, len(tokens.input_ids[0]) - len(cont_ids) + i - 1]
            log_probs += torch.log_softmax(step_logits, -1)[token_id].item()
        
        return log_probs / len(cont_ids)
```

## Governance Challenges

| Challenge | Description | Mitigation |
|-----------|-------------|------------|
| Rapid innovation | Regulation lags behind | Iterative rulemaking |
| Open source | Hard to regulate distributed models | Responsible release practices |
| Dual use | Same model can be beneficial/harmful | Use-based restrictions |
| Jurisdiction | Global models, local laws | Multi-jurisdictional compliance |
| Interpretability | Black box decision making | Explainability research |

## References
- European Commission, "EU AI Act", 2024
- White House, "Executive Order on Safe, Secure, and Trustworthy Development and Use of AI", 2023
- Mitchell, Wu, et al., "Model Cards for Model Reporting", FAT 2019
- Raji, Gebru, et al., "Saving Face: Investigating the Ethical Concerns of Facial Recognition Auditing", AAAI 2020
- Schiff, Biddle, et al., "What's Next for AI Ethics, Policy, and Governance? A Global Overview", AAAI 2021
