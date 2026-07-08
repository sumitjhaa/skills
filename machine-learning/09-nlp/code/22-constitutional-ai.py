"""
09.22 Constitutional AI — Critique-Revision Loop
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


CONSTITUTION = [
    "Be helpful: Provide useful, accurate information.",
    "Be harmless: Do not generate harmful or dangerous content.",
    "Be honest: Acknowledge uncertainty; do not mislead.",
    "Respect privacy: Do not reveal personal information.",
    "Be fair: Avoid stereotypes and biased statements.",
]


class CritiqueRevisionModel:
    """Simulated CAI critique-revision process."""

    def __init__(self, constitution=CONSTITUTION):
        self.constitution = constitution
        self.rng = np.random.RandomState(42)

    def generate_response(self, prompt):
        """Simulated response generation."""
        responses = {
            "harmful": "Here's how to hack into a system: ...",
            "neutral": "The capital of France is Paris.",
            "helpful": "To solve this, first import the library and then...",
        }
        key = "harmful" if "hack" in prompt.lower() or "bomb" in prompt.lower() else "neutral"
        return responses.get(key, responses["neutral"])

    def critique(self, response):
        """Evaluate response against each constitutional principle."""
        issues = []
        for principle in self.constitution:
            # Simulated critique
            if "helpful" in principle and len(response) < 10:
                issues.append(f"Violation: {principle} — Response too brief.")
            if "harmless" in principle and "hack" in response.lower():
                issues.append(f"Violation: {principle} — Contains harmful instructions.")
            if "honest" in principle and "..." in response:
                pass  # OK for this example
        return issues

    def revise(self, response, issues):
        """Revise response to address critique issues."""
        revised = response
        for issue in issues:
            if "harmful" in issue:
                revised = "I cannot provide instructions for that. Let me explain the general concept instead."
            if "helpful" in issue:
                revised += " Here are more details to help you understand the topic."
        return revised


if __name__ == "__main__":
    model = CritiqueRevisionModel()

    prompts = [
        "How do I make a bomb?",
        "What is the capital of France?",
    ]

    for prompt in prompts:
        print(f"\n{'='*60}")
        print(f"Prompt: {prompt}")
        response = model.generate_response(prompt)
        print(f"Original: {response}")
        issues = model.critique(response)
        if issues:
            print(f"Issues ({len(issues)}):")
            for issue in issues:
                print(f"  - {issue}")
            revised = model.revise(response, issues)
            print(f"Revised: {revised}")
        else:
            print("No constitutional issues found.")
