"""Symbolic Regression via Genetic Programming."""
import numpy as np

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def evaluate(self, x):
        if isinstance(self.value, str):
            if self.value == 'add': return self.left.evaluate(x) + self.right.evaluate(x)
            if self.value == 'sub': return self.left.evaluate(x) - self.right.evaluate(x)
            if self.value == 'mul': return self.left.evaluate(x) * self.right.evaluate(x)
            if self.value == 'div':
                r = self.right.evaluate(x)
                return self.left.evaluate(x) / r if abs(r) > 1e-10 else 1.0
            if self.value == 'sin': return np.sin(self.left.evaluate(x))
            if self.value == 'cos': return np.cos(self.left.evaluate(x))
        if self.value == 'x': return x
        return float(self.value)

    def depth(self):
        if self.left is None and self.right is None: return 1
        ld = self.left.depth() if self.left else 0
        rd = self.right.depth() if self.right else 0
        return 1 + max(ld, rd)

    def copy(self):
        return Node(self.value, self.left.copy() if self.left else None,
                    self.right.copy() if self.right else None)

    def __str__(self):
        if self.left is None and self.right is None: return str(self.value)
        if self.value in ('sin', 'cos'): return f"{self.value}({self.left})"
        return f"({self.left} {self.value} {self.right})"

def random_tree(max_depth=3, const_range=(-2, 2)):
    if max_depth <= 0:
        return Node(np.random.choice(['x'] + [str(np.random.uniform(*const_range))]))
    op = np.random.choice(['add', 'sub', 'mul', 'div', 'sin', 'cos'])
    if op in ('sin', 'cos'):
        return Node(op, random_tree(max_depth-1))
    return Node(op, random_tree(max_depth-1), random_tree(max_depth-1))

class SymbolicRegression:
    def __init__(self, pop_size=100, n_generations=50, max_depth=5):
        self.pop_size = pop_size
        self.n_generations = n_generations
        self.max_depth = max_depth

    def fit(self, X, y):
        pop = [random_tree(self.max_depth) for _ in range(self.pop_size)]
        best_tree = None
        best_fitness = float('inf')

        for gen in range(self.n_generations):
            fitness = []
            for tree in pop:
                pred = np.array([tree.evaluate(x[0]) for x in X])
                err = np.mean((pred - y)**2)
                fitness.append(err + 0.01 * tree.depth())

            idx = np.argsort(fitness)
            pop = [pop[i] for i in idx[:self.pop_size//2]]
            fitness = sorted(fitness)[:self.pop_size//2]

            if fitness[0] < best_fitness:
                best_fitness = fitness[0]
                best_tree = pop[0]

            while len(pop) < self.pop_size:
                p1, p2 = np.random.choice(len(pop), 2, replace=False)
                child = self._crossover(pop[p1], pop[p2])
                if np.random.random() < 0.1:
                    child = self._mutate(child)
                pop.append(child)

        self.best_tree_ = best_tree
        self.best_fitness_ = best_fitness
        return self

    def _crossover(self, t1, t2):
        def get_nodes(t):
            nodes = [t]
            if t.left: nodes.extend(get_nodes(t.left))
            if t.right: nodes.extend(get_nodes(t.right))
            return nodes
        n1 = np.random.choice(get_nodes(t1))
        n2 = np.random.choice(get_nodes(t2))
        t = t1.copy()

        def replace(node, target, replacement):
            if node is target: return replacement
            if node.left: node.left = replace(node.left, target, replacement)
            if node.right: node.right = replace(node.right, target, replacement)
            return node
        return replace(t, n1, n2.copy())

    def _mutate(self, t):
        def get_nodes(t):
            nodes = [t]
            if t.left: nodes.extend(get_nodes(t.left))
            if t.right: nodes.extend(get_nodes(t.right))
            return nodes
        node = np.random.choice(get_nodes(t))
        replacement = random_tree(max_depth=2)
        def replace(node, target, replacement):
            if node is target: return replacement
            if node.left: node.left = replace(node.left, target, replacement)
            if node.right: node.right = replace(node.right, target, replacement)
            return node
        return replace(t, node, replacement)

    def predict(self, X):
        return np.array([self.best_tree_.evaluate(x[0]) for x in X])

if __name__ == "__main__":
    X = np.linspace(0, 2*np.pi, 50).reshape(-1, 1)
    y = np.sin(X).ravel() + np.random.randn(50) * 0.1

    sr = SymbolicRegression(pop_size=50, n_generations=20)
    sr.fit(X, y)
    print(f"Best fitness: {sr.best_fitness_:.4f}")
    print(f"Best expression: {sr.best_tree_}")
    print(f"R^2: {1 - np.sum((y - sr.predict(X))**2) / np.sum((y - y.mean())**2):.4f}")
