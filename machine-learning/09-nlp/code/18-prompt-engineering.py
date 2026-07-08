"""
09.18 Prompt Engineering — CoT, Self-Consistency, DSPy-style Program
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


class SimpleReasoningModel:
    """Dummy reasoning model that simulates CoT + answer."""

    def __init__(self, seed=42):
        self.rng = np.random.RandomState(seed)

    def generate_reasoning(self, question, num_steps=5):
        steps = []
        for i in range(num_steps):
            step = f"Step {i+1}: Considering {['the numbers', 'the operations', 'the result'][i%3]}..."
            steps.append(step)
        answer = self.rng.randint(0, 100)
        return steps, answer

    def generate_answer(self, question):
        return self.rng.randint(0, 100)


def self_consistency(model, question, num_samples=5):
    """Sample multiple reasoning paths and take majority vote."""
    answers = []
    reasoning_paths = []
    for _ in range(num_samples):
        steps, answer = model.generate_reasoning(question)
        answers.append(answer)
        reasoning_paths.append(steps)
    # Majority vote
    unique, counts = np.unique(answers, return_counts=True)
    final_answer = unique[np.argmax(counts)]
    return final_answer, answers, reasoning_paths


class DSPyModule:
    """
    Simplified DSPy-style program with signature and optimizer.
    """

    def __init__(self, signature):
        self.signature = signature  # e.g., "question -> answer"
        self.demonstrations = []

    def __call__(self, question, use_cot=True):
        if use_cot:
            prompt = f"Question: {question}\nLet's think step by step.\n"
        else:
            prompt = f"Question: {question}\nAnswer: "
        return prompt

    def compile(self, train_data):
        """Bootstrap few-shot examples."""
        self.demonstrations = []
        for q, a in train_data[:3]:
            if self.demonstrations:
                demo = f"Question: {q}\nAnswer: {a}"
            else:
                demo = f"Q: {q}\nA: {a}"
            self.demonstrations.append(demo)


if __name__ == "__main__":
    model = SimpleReasoningModel(seed=42)

    # CoT + Self-Consistency
    question = "If a train travels at 60 mph for 2 hours, how far does it go?"
    final_answer, all_answers, _ = self_consistency(model, question, num_samples=5)
    print(f"Question: {question}")
    print(f"All answers: {all_answers}")
    print(f"Final (majority): {final_answer}")

    # DSPy-style
    module = DSPyModule("question -> answer")
    train_data = [
        ("What is 2+2?", "4"),
        ("Capital of France?", "Paris"),
        ("Speed of light?", "299,792,458 m/s"),
    ]
    module.compile(train_data)
    prompt = module(question)
    print(f"\nDSPy-style CoT prompt:\n  {prompt[:80]}...")
    print(f"Demonstrations: {len(module.demonstrations)} few-shot examples")
