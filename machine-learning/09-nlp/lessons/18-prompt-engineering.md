# 09.18 Prompt Engineering

## Learning Objectives
- Understand prompting strategies for LLMs
- Implement chain-of-thought (CoT) and tree-of-thought (ToT)
- Apply in-context learning and instruction tuning
- Analyze prompt sensitivity and robustness

## Prompt Components

### Basic Structure
```
[System]       → Role, constraints, persona
[Instruction]  → Task description
[Context]      → Background information
[Examples]     → Few-shot demonstrations
[Input]        → Query to process
[Output]       → Desired format
```

## In-Context Learning (ICL)

### Few-Shot Prompting
```
Classify the sentiment of the following reviews:

Review: This movie was fantastic!
Sentiment: Positive

Review: I hated every minute of it.
Sentiment: Negative

Review: The acting was decent but the plot was predictable.
Sentiment: ??? [Neutral]
```

### Key Factors
- Example selection: Similarity to query matters
- Example order: Recent examples have higher influence
- Label balance: Equal positive/negative examples
- Format consistency: Same template for all examples

## Chain-of-Thought (CoT)

### Zero-Shot CoT
```
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 balls. How many tennis balls does he have now?
A: Let's think step by step.
Roger started with 5 balls.
2 cans of 3 balls each = 6 balls.
5 + 6 = 11.
The answer is 11.
```

### Few-Shot CoT
```
Q: {question}
A: {reasoning steps} The answer is {answer}.
```

### Performance
- MATH: 18% → 58% with CoT
- GSM8K: 18% → 92% with CoT + self-consistency
- Effective for arithmetic, logic, symbolic reasoning

## Self-Consistency

### Method
1. Generate $N$ CoT paths (with temperature > 0)
2. Majority vote over final answers

```python
def self_consistency(model, prompt, n=5, temperature=0.7):
    answers = []
    for _ in range(n):
        output = model.generate(prompt, temperature=temperature)
        answer = extract_answer(output)
        answers.append(answer)
    return max(set(answers), key=answers.count)
```

## Tree-of-Thoughts (ToT)

### Approach
- Tree search over thought sequences
- Each node = partial reasoning state
- BFS/DFS to explore reasoning paths
- Prune unpromising branches

### Evaluation
- Game of 24: 7.3% → 74% success rate
- Creative writing: Better coherence and novelty

## Prompt Techniques Summary

| Technique | Description | Best For |
|-----------|-------------|----------|
| Zero-shot | No examples | Simple tasks |
| Few-shot | 2-5 examples | Classification, formatting |
| Chain-of-thought | Step-by-step reasoning | Math, logic |
| Self-consistency | Multiple paths + vote | High-stakes reasoning |
| Tree-of-thought | Tree search | Planning, puzzles |
| ReAct | Reasoning + acting | Agent tasks |
| Reflection | Self-critique answers | Factual accuracy |
| Persona | Role assignment | Domain-specific tasks |

## Code: Structured Prompt Generator

```python
import jinja2

class PromptTemplate:
    def __init__(self, template_str):
        self.template = jinja2.Template(template_str)

    def format(self, **kwargs):
        return self.template.render(**kwargs)

# Example: QA with CoT
QA_TEMPLATE = PromptTemplate("""
{% if system %}{{ system }}

{% endif %}{% if examples %}
Examples:
{% for ex in examples %}
Q: {{ ex.question }}
A: {{ ex.answer }}
{% endfor %}

{% endif %}
Q: {{ question }}
A: {% if use_cot %}Let's think step by step. {% endif %}""")

def few_shot_classify(text, labels, model, examples_per_label=2):
    examples = []
    for label, samples in label_samples.items():
        for sample in samples[:examples_per_label]:
            examples.append({"text": sample, "label": label})
    prompt = f"Classify the text into one of these labels: {', '.join(labels)}\n\n"
    for ex in examples:
        prompt += f"Text: {ex['text']}\nLabel: {ex['label']}\n\n"
    prompt += f"Text: {text}\nLabel:"
    return model.generate(prompt)
```

## Practical Considerations
- **Prompt sensitivity**: Small wording changes cause large output differences
- **Instruction following**: Larger models follow instructions more reliably
- **Temperature**: 0 for deterministic, 0.7-1.0 for creative, >1 for diverse sampling
- **Token limits**: Leave room for completion (20-50% of context window)
- **System prompt**: Effective for setting consistent behaviour across queries

## References
- Brown, Mann, et al., "Language Models are Few-Shot Learners (GPT-3)", NeurIPS 2020
- Wei, Wang, et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", NeurIPS 2022
- Wang, Wei, et al., "Self-Consistency Improves Chain of Thought Reasoning in Language Models", ICLR 2023
- Yao, Yu, et al., "Tree of Thoughts: Deliberate Problem Solving with Large Language Models", NeurIPS 2023
- Kojima, Gu, et al., "Large Language Models are Zero-Shot Reasoners", NeurIPS 2022
