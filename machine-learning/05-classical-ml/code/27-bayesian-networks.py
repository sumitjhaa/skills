"""Bayesian Networks (structure + parameter learning) from scratch."""
import numpy as np
from itertools import product

class BayesianNetwork:
    def __init__(self):
        self.graph = {}
        self.cpts = {}

    def add_edge(self, parent, child):
        if parent not in self.graph:
            self.graph[parent] = []
        self.graph[parent].append(child)

    def fit(self, data, structure=None):
        self.vars = list(range(data.shape[1]))
        if structure:
            self._learn_params(data)
        else:
            self._learn_structure(data)

    def _learn_params(self, data):
        for node, parents in self.graph.items():
            if parents:
                for p in parents:
                    if p not in self.graph:
                        self.graph[p] = []
            self._fit_cpt(data, node)

    def _fit_cpt(self, data, node, parents=None):
        if parents is None:
            parents = self.graph.get(node, [])
        n = data.shape[1]
        if not parents:
            self.cpts[node] = {}
            vals, counts = np.unique(data[:, node], return_counts=True)
            self.cpts[node]['prior'] = {v: c/len(data) for v, c in zip(vals, counts)}
        else:
            cpt = {}
            parent_vals = [np.unique(data[:, p]) for p in parents]
            for combo in product(*parent_vals):
                mask = np.all([data[:, p] == v for p, v in zip(parents, combo)], axis=0)
                if np.sum(mask) > 0:
                    vals, counts = np.unique(data[mask][:, node], return_counts=True)
                    cpt[combo] = {v: c/np.sum(mask) for v, c in zip(vals, counts)}
                else:
                    cpt[combo] = {0: 0.5, 1: 0.5}
            self.cpts[node] = cpt

    def _learn_structure(self, data):
        self.graph = {i: [] for i in range(data.shape[1])}
        for i in range(data.shape[1]):
            for j in range(data.shape[1]):
                if i != j and np.abs(np.corrcoef(data[:, i], data[:, j])[0, 1]) > 0.3:
                    self.graph[i].append(j)
        self._learn_params(data)

    def sample(self, n_samples=1):
        samples = np.zeros((n_samples, len(self.vars)))
        for _ in range(n_samples):
            for v in self.vars:
                parents = self.graph.get(v, [])
                if not parents:
                    prior = self.cpts[v]['prior']
                    vals, probs = zip(*prior.items())
                    samples[_, v] = np.random.choice(vals, p=probs)
                else:
                    combo = tuple(samples[_, p] for p in parents)
                    if combo in self.cpts[v]:
                        vals, probs = zip(*self.cpts[v][combo].items())
                        samples[_, v] = np.random.choice(vals, p=probs)
        return samples

if __name__ == "__main__":
    np.random.seed(42)
    n = 500
    X = np.zeros((n, 3))
    X[:, 0] = np.random.binomial(1, 0.5, n)  # A ~ Bern(0.5)
    for i in range(n):
        X[i, 1] = np.random.binomial(1, 0.3 + 0.4 * X[i, 0])  # B | A
        X[i, 2] = np.random.binomial(1, 0.2 + 0.5 * X[i, 1])  # C | B

    bn = BayesianNetwork()
    bn.add_edge(0, 1)
    bn.add_edge(1, 2)
    bn.fit(X)
    print("Bayesian Network CPTs learned")

    samples = bn.sample(10)
    print(f"Generated {len(samples)} samples")
    print("Sample (first 5):\n", samples[:5])
