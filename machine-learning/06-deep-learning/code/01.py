"""06.01 - Computational Graphs: DAG construction and topological ordering"""

import numpy as np
from collections import defaultdict


class GraphNode:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.parents = []
        self.children = []


class ComputationalGraph:
    def __init__(self):
        self.nodes = {}
        self.adj = defaultdict(list)
        self.in_degree = defaultdict(int)

    def add_node(self, name, value=None):
        node = GraphNode(name, value)
        self.nodes[name] = node
        if name not in self.in_degree:
            self.in_degree[name] = 0
        return node

    def add_edge(self, from_name, to_name):
        self.adj[from_name].append(to_name)
        self.in_degree[to_name] += 1
        self.nodes[from_name].children.append(self.nodes[to_name])
        self.nodes[to_name].parents.append(self.nodes[from_name])

    def topological_sort(self):
        in_deg = dict(self.in_degree)
        queue = [n for n in self.nodes if in_deg.get(n, 0) == 0]
        order = []
        while queue:
            node = queue.pop(0)
            order.append(node)
            for neighbor in self.adj.get(node, []):
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    queue.append(neighbor)
        return order

    def forward(self):
        order = self.topological_sort()
        results = {}
        for name in order:
            node = self.nodes[name]
            if not node.parents:
                results[name] = node.value
            else:
                parent_vals = [results[p.name] for p in node.parents]
                results[name] = node.value(*parent_vals) if callable(node.value) else node.value
        return results


if __name__ == "__main__":
    g = ComputationalGraph()
    g.add_node("a", 2.0)
    g.add_node("b", 3.0)
    g.add_node("c", 5.0)
    g.add_node("add", lambda x, y: x + y)
    g.add_node("mul", lambda x, y: x * y)
    g.add_node("output", lambda x: x)

    g.add_edge("a", "add")
    g.add_edge("b", "add")
    g.add_edge("add", "mul")
    g.add_edge("c", "mul")
    g.add_edge("mul", "output")

    result = g.forward()
    print(f"Computational graph (a+b)*c = ({2.0}+{3.0})*{5.0} = {result['output']}")
    print(f"Topological order: {g.topological_sort()}")
    print("DAG built and evaluated successfully.")
