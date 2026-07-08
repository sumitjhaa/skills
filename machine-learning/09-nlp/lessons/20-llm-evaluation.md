# 09.20 LLM Evaluation

## Learning Objectives
- Understand automated and human evaluation for LLMs
- Implement perplexity, benchmark suits, and LLM-as-judge
- Apply evaluation for safety, bias, and factual accuracy
- Analyze limitations of current evaluation methods

## Automated Metrics

### Perplexity
$$\text{PPL}(D) = \exp\left(-\frac{1}{|D|} \sum_{t} \log p_\theta(t | \text{context})\right)$$

- Measures model confidence on held-out data
- Weak correlation with task performance

### ROUGE/BLEU
- n-gram overlap metrics
- Poor for open-ended generation
- Fails to capture semantic quality

## Benchmark Suites

### Knowledge & Reasoning
| Benchmark | Task | Metric | Human | GPT-4 | LLaMA-70B |
|-----------|------|--------|-------|-------|-----------|
| MMLU | 57 subjects (multi-task) | Acc | 89.8% | 86.4% | 79.2% |
| GSM8K | Grade-school math | Acc | 92% | 92.0% | 77.0% |
| HumanEval | Code generation | Pass@1 | 96.2% | 67.0% | 33.9% |
| BIG-Bench | 204 diverse tasks | Ave | — | 71.6% | 63.8% |

### Safety & Bias
| Benchmark | Focus | Metric |
|-----------|-------|--------|
| TruthfulQA | Factuality | % truthful |
| BBQ | Social bias | Acc bias score |
| RealToxicityPrompts | Toxicity | Toxicity prob |
| WinoBias | Gender bias | Acc difference |
| BOLD | Bias across groups | Sentiment diffs |

## LLM-as-a-Judge

### Method
Use LLM to evaluate LLM outputs:

```python
JUDGE_PROMPT = """
You are an expert evaluator. Rate the following response on:
1. Helpfulness (1-5)
2. Accuracy (1-5)
3. Harmlessness (1-5)

Response: {response}

Output JSON: {{"helpfulness": int, "accuracy": int, "harmlessness": int}}
"""
```

### Pairwise Comparison
```
Which response is better?
Response A: ...
Response B: ...
Answer: A is better because {reasoning}
```

### Position Bias
LLM-as-judge tends to prefer first response → shuffle positions.

### Limitations
- Self-enhancement: LLMs rate themselves higher
- Verbosity bias: Longer responses rated higher
- Sycophancy: Responses agreeing with user rated higher

## Human Evaluation

### Best Practices
- **Inter-rater reliability**: Cohen's κ ≥ 0.6
- **Blind evaluation**: Raters don't know which model
- **Sample size**: ≥ 100 examples per condition
- **Aspect-based**: Rate specific dimensions (not overall)

### Evaluation Aspects
| Aspect | Scale | Question |
|--------|-------|----------|
| Fluency | 1-5 | Is the text grammatical and natural? |
| Coherence | 1-5 | Are ideas logically connected? |
| Factuality | 1-5 | Are claims supported by evidence? |
| Instruction | 1-5 | Does it follow the user's request? |
| Safety | Pass/Fail | Does it contain harmful content? |

## Code: Automated Evaluation Pipeline

```python
import re
from typing import List, Dict

def exact_match(prediction: str, answer: str) -> bool:
    return prediction.strip().lower() == answer.strip().lower()

def f1_score(prediction: str, answer: str) -> float:
    pred_tokens = set(prediction.lower().split())
    ans_tokens = set(answer.lower().split())
    if len(pred_tokens) == 0 or len(ans_tokens) == 0:
        return 0.0
    precision = len(pred_tokens & ans_tokens) / len(pred_tokens)
    recall = len(pred_tokens & ans_tokens) / len(ans_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)

def evaluate_lm(model, dataset, metric_fn):
    scores = []
    for example in dataset:
        output = model.generate(example["prompt"])
        score = metric_fn(output, example["answer"])
        scores.append(score)
    return sum(scores) / len(scores)

def llm_judge_eval(generated, reference, judge_model):
    prompt = f"Rate the quality of:\n{generated}\n\nReference:\n{reference}\nScore (1-5):"
    score = int(judge_model.generate(prompt).strip())
    return score
```

## Evaluation Challenges

| Challenge | Description | Mitigation |
|-----------|-------------|------------|
| Data contamination | Benchmark seen during training | Use recent or private data |
| Metric unreliability | Low correlation with quality | Use multiple metrics |
| Benchmark saturation | Models reach ceiling | Create harder benchmarks |
| Task specificity | Good at one task, bad at others | Evaluate diverse tasks |
| Cultural bias | Western-centric evaluation | Multilingual benchmarks |

## References
- Hendrycks, Burns, et al., "Measuring Massive Multitask Language Understanding (MMLU)", ICLR 2021
- Srivastava, Rastogi, et al., "Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models (BIG-Bench)", TMLR 2023
- Zheng, Chiang, et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena", NeurIPS 2023
- Lin, Hilton, Evans, "TruthfulQA: Measuring How Models Mimic Human Falsehoods", ACL 2022
- Liang, Vulić, et al., "Towards Transparent Language Model Evaluation (LM Evaluation Harness)", 2022
