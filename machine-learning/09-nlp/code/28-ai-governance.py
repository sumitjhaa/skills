"""
09.28 AI Governance — Model Card Generator & Bias Audit
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


class ModelCard:
    """Generate standardized model cards (per Mitchell et al. 2019)."""

    def __init__(self, model_name, model_type, model_description):
        self.model_name = model_name
        self.model_type = model_type
        self.description = model_description
        self.sections = {}

    def add_section(self, title, content):
        self.sections[title] = content

    def generate(self):
        card = f"# Model Card: {self.model_name}\n\n"
        card += f"**Model Type:** {self.model_type}\n\n"
        card += f"**Description:** {self.description}\n\n"
        for title, content in self.sections.items():
            card += f"## {title}\n{content}\n\n"
        return card


class BiasAudit:
    """Simple fairness audit across demographic groups."""

    def __init__(self, groups):
        self.groups = groups

    def measure_disparity(self, scores, sensitive_attr):
        """Compute demographic parity difference."""
        groups = np.unique(sensitive_attr)
        rates = {}
        for g in groups:
            mask = sensitive_attr == g
            rates[g] = np.mean(scores[mask])
        max_rate = max(rates.values())
        min_rate = min(rates.values())
        return {"rates": rates, "disparity": max_rate - min_rate}

    def equal_opportunity(self, predictions, labels, sensitive_attr, positive_class=1):
        """Check equal TPR across groups."""
        groups = np.unique(sensitive_attr)
        tprs = {}
        for g in groups:
            mask = sensitive_attr == g
            actual_positive = labels[mask] == positive_class
            if actual_positive.sum() > 0:
                tpr = np.mean(predictions[mask][actual_positive] == positive_class)
                tprs[g] = tpr
        return tprs


if __name__ == "__main__":
    # Model Card
    card = ModelCard("NLP-Safe-1.0", "Transformer LM", "Safety-filtered language model")
    card.add_section("Intended Use", "Educational text generation with safety guardrails")
    card.add_section("Training Data", "Filtered subset of CommonCrawl, 100B tokens")
    card.add_section("Ethical Considerations", "Model may reflect biases in training data; not for medical or legal use")
    card.add_section("Evaluation", "MMLU: 68.2%, TruthfulQA: 72.1%, Toxicity: <0.5%")
    print(card.generate())

    # Bias Audit
    np.random.seed(42)
    n = 100
    groups = np.random.choice(["A", "B"], size=n)
    scores = np.random.rand(n)
    predictions = (scores > 0.5).astype(int)
    labels = np.random.randint(0, 2, size=n)

    audit = BiasAudit(["A", "B"])
    disparity = audit.measure_disparity(scores, groups)
    print(f"Demographic parity disparity: {disparity['disparity']:.3f}")
    print(f"Group rates: {disparity['rates']}")
    tprs = audit.equal_opportunity(predictions, labels, groups)
    print(f"Equal opportunity TPRs: {tprs}")
