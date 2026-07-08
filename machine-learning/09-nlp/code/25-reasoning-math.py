"""
09.25 Reasoning & Math — CoT Sampling, Self-Consistency, Verification
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


class ReasoningModel:
    """Simulated reasoning model with controllable accuracy."""

    def __init__(self, accuracy=0.7):
        self.accuracy = accuracy

    def generate_reasoning(self, problem, num_steps=4):
        steps = []
        for i in range(num_steps):
            steps.append(f"  Step {i+1}: As {'n' if np.random.rand() > self.accuracy else ''}ext, {np.random.choice(['compute', 'derive', 'substitute', 'simplify'])}...")
        answer = np.random.randint(0, 100)
        return steps, answer


class MathVerifier:
    """Simple verifier that checks if answer satisfies constraints."""

    def __init__(self):
        self.rng = np.random.RandomState(42)

    def verify(self, problem, answer):
        """Simulated verification — check with reverse computation."""
        # 80% chance of verifying correctly
        return np.random.rand() < 0.8


def self_consistency_decode(model, problem, num_samples=8):
    """Sample multiple CoT paths, return majority answer."""
    answers = []
    all_steps = []
    for _ in range(num_samples):
        steps, answer = model.generate_reasoning(problem)
        answers.append(answer)
        all_steps.append(steps)
    # Majority vote
    unique, counts = np.unique(answers, return_counts=True)
    final = unique[np.argmax(counts)]
    confidence = np.max(counts) / num_samples
    return final, confidence, answers


def best_of_n(model, verifier, problem, n=10):
    """Generate n candidates, pick highest-verified."""
    candidates = []
    for _ in range(n):
        _, answer = model.generate_reasoning(problem)
        verified = verifier.verify(problem, answer)
        candidates.append((answer, verified))
    verified_answers = [a for a, v in candidates if v]
    if verified_answers:
        return max(set(verified_answers), key=verified_answers.count)
    return candidates[0][0]


if __name__ == "__main__":
    model = ReasoningModel(accuracy=0.65)
    verifier = MathVerifier()

    problem = "Solve for x: 2x + 5 = 15"

    # Self-consistency
    final, conf, all_answers = self_consistency_decode(model, problem, num_samples=8)
    unique, counts = np.unique(all_answers, return_counts=True)
    print(f"Problem: {problem}")
    print(f"Answers: {dict(zip(unique, counts))}")
    print(f"Majority: {final} (confidence: {conf:.0%})")

    # Best-of-N with verification
    best = best_of_n(model, verifier, problem, n=10)
    print(f"Best-of-N: {best}")

    # Test-time compute scaling
    for k in [1, 4, 16, 64]:
        final, conf, _ = self_consistency_decode(model, problem, num_samples=k)
        print(f"Samples={k:3d}: final={final}, confidence={conf:.2f}")
