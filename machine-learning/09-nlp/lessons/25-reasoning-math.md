# 09.25 Reasoning & Math

## Learning Objectives
- Understand mathematical reasoning in LLMs
- Implement tool-augmented reasoning (PoT, PAL)
- Apply verification and self-consistency for math
- Evaluate on MATH, GSM8K, and Olympiad benchmarks

## Math Reasoning Challenges

### Why Math is Hard for LLMs
- Exact arithmetic requires precise computation
- Multi-step reasoning with error propagation
- Symbolic manipulation
- Verify/self-correct reasoning traces

### Approaches
| Method | Description | GSM8K | MATH |
|--------|-------------|-------|------|
| Direct answer | No CoT | 18% | 6% |
| Chain-of-thought | Step-by-step | 58% | 21% |
| Self-consistency | Majority vote (n=40) | 74% | 33% |
| Tool-use (PoT) | Execute code | 84% | 51% |
| Verification | Check + revise | 87% | 55% |

## Program-of-Thought (PoT)

### Generate Code Instead of Text
```
Q: A train travels 120 km in 2 hours. What is its speed?
A:
```python
def solution():
    distance = 120  # km
    time = 2  # hours
    speed = distance / time
    return speed
```

### Execution
```python
exec(code, globals())  # Execute generated code
result = solution()
```

## Verification

### Self-Verification
1. Generate answer with CoT
2. Verify each step:
   - Rephrase step as question
   - Ask model to confirm
3. Regenerate if step is wrong

### Majority Vote + Verification
```python
def verified_vote(model, question, n_samples=20):
    answers = []
    for _ in range(n_samples):
        ans = model.generate_with_cot(question)
        verified = model.verify_answer(ans)
        if verified:
            answers.append(ans)
    return majority_vote(answers)
```

## Code-Mixing

### PAL (Program-Aided Language Models)
Interleave reasoning text and code:

```
Q: Bob has 5 apples. Alice gives him 3 more. How many apples does Bob have?
Let's compute this step by step.
apples_bob = 5  # Bob starts with 5
apples_from_alice = 3  # Alice gives 3
apples_bob += apples_from_alice
So Bob has {apples_bob} apples.
```

## Math Benchmarks

| Benchmark | Domain | Questions | Format | Human | GPT-4 | Claude 3.5 |
|-----------|--------|-----------|--------|-------|-------|------------|
| GSM8K | Grade school math | 8.5K | Word problems | 92% | 92% | 95% |
| MATH | Competition math | 5K | LaTeX | 90% | 55% | 67% |
| MMLU-STEM | Multi-subject | ~3K | Multiple choice | 89% | 77% | 82% |
| AIME | Olympiad math | 30 | Proof/answer | 90% | 12% | 22% |
| Putnam | University math | 12 | Proof | 40% | 3% | 5% |

## Code: Math Verification

```python
import re
import torch

class MathVerifier:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def extract_final_answer(self, solution_text):
        patterns = [
            r"The answer is \$?(\\d+(?:\\.\\d+)?)\$?",
            r"\banswer\s+is\s+(-?\\d+(?:\\.\\d+)?)",
            r"\boxed\{(-?\\d+(?:\\.\\d+)?)\}",
        ]
        for p in patterns:
            m = re.search(p, solution_text)
            if m:
                return m.group(1)
        return None

    def verify_step(self, problem, step_text):
        prompt = f"""
        Problem: {problem}
        Proposed step: {step_text}
        
        Is this step mathematically correct? Answer Yes or No, and explain.
        """
        response = self.model.generate(prompt)
        return response.strip().startswith("Yes")

    def verify_solution(self, problem, solution):
        steps = solution.split("\\n")
        for step in steps:
            if not self.verify_step(problem, step):
                return False
        return True

    def reject_sampling(self, problem, n_samples=10):
        solutions = []
        for _ in range(n_samples):
            sol = self.model.generate_with_cot(problem)
            if self.verify_solution(problem, sol):
                solutions.append(self.extract_final_answer(sol))
        return max(set(solutions), key=solutions.count)
```

## Practical Considerations
- **Arithmetic**: LLMs struggle with large numbers → use code execution
- **Units**: Model confuses units (km vs miles) → explicit unit tracking
- **Multi-step**: Each step has ~5-10% error → verification critical
- **Proofs**: Open-ended math proofs remain challenging
- **OOD math**: Models fail on problems slightly different from training

## References
- Wei, Wang, et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", NeurIPS 2022
- Chen, Tworek, et al., "Evaluating Large Language Models Trained on Code (Codex)", 2021
- Cobbe, Kosaraju, et al., "Training Verifiers to Solve Math Word Problems (GSM8K)", 2021
- Gao, Madaan, et al., "PAL: Program-aided Language Models", ICML 2023
- Lightman, Kosaraju, et al., "Let's Verify Step by Step (Math Verifier)", 2023
