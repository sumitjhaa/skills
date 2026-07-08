"""
07.26 Neural-Symbolic: Logic Tensor Network / DeepProbLog style.
"""
import numpy as np
import matplotlib.pyplot as plt


class LogicLayer:
    """Simple differentiable logic: AND, OR, NOT as neural computations."""
    @staticmethod
    def fuzzy_and(a, b):
        return a * b

    @staticmethod
    def fuzzy_or(a, b):
        return a + b - a * b

    @staticmethod
    def fuzzy_not(a):
        return 1 - a


class NeuralSymbolicModel:
    """Neural perception -> symbolic reasoning pipeline."""
    def __init__(self, input_dim=4, hidden_dim=16, n_predicates=4):
        self.percept_W1 = np.random.randn(input_dim, hidden_dim) * 0.1
        self.percept_b1 = np.zeros(hidden_dim)
        self.percept_W2 = np.random.randn(hidden_dim, n_predicates) * 0.1
        self.percept_b2 = np.zeros(n_predicates)
        self.logic = LogicLayer()

    def perceive(self, x):
        h = np.tanh(x @ self.percept_W1 + self.percept_b1)
        return 1 / (1 + np.exp(-(h @ self.percept_W2 + self.percept_b2)))

    def reason(self, predicates):
        p1, p2, p3, p4 = predicates[:, 0], predicates[:, 1], predicates[:, 2], predicates[:, 3]
        # Rule: (p1 AND p2) OR (NOT p3 AND p4)
        rule1 = self.logic.fuzzy_and(p1, p2)
        rule2 = self.logic.fuzzy_and(self.logic.fuzzy_not(p3), p4)
        return self.logic.fuzzy_or(rule1, rule2)

    def forward(self, x):
        preds = self.perceive(x)
        return self.reason(preds), preds


if __name__ == "__main__":
    np.random.seed(42)
    model = NeuralSymbolicModel()
    x = np.random.randn(20, 4)
    output, preds = model.forward(x)
    print("Neural-Symbolic Reasoning:")
    print(f"Input shape: {x.shape}")
    print(f"Predicates (perception): {preds.shape}")
    print(f"Reasoning output: {output.shape}")
    print(f"Output values (should be in [0,1]): {output}")

    plt.figure(figsize=(10, 4))
    plt.subplot(121)
    plt.imshow(preds, aspect='auto', cmap='RdYlBu', vmin=0, vmax=1)
    plt.colorbar(label='Truth value')
    plt.xlabel('Predicate')
    plt.ylabel('Sample')
    plt.title('Neural Perception Outputs')
    plt.subplot(122)
    plt.bar(range(len(output)), output)
    plt.xlabel('Sample')
    plt.ylabel('Reasoning output')
    plt.title('(p1 AND p2) OR (NOT p3 AND p4)')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/neural_symbolic.png')
    plt.close()
    print("Saved neural_symbolic.png")
