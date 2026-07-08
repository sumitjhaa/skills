# Lesson 05.27: Bayesian Networks

## Learning Objectives
- Understand DAG representation of conditional independence
- Implement structure learning (score-based and constraint-based)
- Derive parameter learning via MLE and Bayesian methods
- Apply exact and approximate inference

## Definition
A Bayesian Network is a directed acyclic graph (DAG) $G = (V, E)$ where:
- Nodes: random variables $X_1, \dots, X_d$
- Edges: direct probabilistic dependencies
- **Markov property**: Each node is independent of its non-descendants given its parents

$$P(X_1, \dots, X_d) = \prod_{i=1}^d P(X_i \mid \text{Pa}(X_i))$$

This factorization reduces the full joint distribution from $O(2^d)$ to $O(d \cdot 2^{|\text{Pa}|})$ parameters.

### d-Separation
A path between two nodes is blocked if:
- There is a chain $A \to B \to C$ or $A \leftarrow B \leftarrow C$ with $B$ observed
- There is a fork $A \leftarrow B \to C$ with $B$ observed
- There is a collider $A \to B \leftarrow C$ with $B$ not observed and no descendant observed

## Structure Learning

### Score-Based Learning
Find DAG maximizing a score:

$$S(G) = \log P(G|D) \propto \log P(D|G) + \log P(G)$$

**BIC/MDL score**:
$$\text{BIC}(G) = \ell(\hat{\theta}_G) - \frac{\dim(G)}{2} \log n$$

**BDeu score** (Bayesian Dirichlet equivalent uniform prior):

$$\text{BDeu}(G) = \sum_i \sum_j \left( \log \frac{\Gamma(\alpha_{ij})}{\Gamma(N_{ij} + \alpha_{ij})} + \sum_k \log \frac{\Gamma(N_{ijk} + \alpha_{ijk})}{\Gamma(\alpha_{ijk})} \right)$$

Search algorithms: greedy hill climbing, tabu search, genetic algorithms, exact integer programming (for small $d$).

### Constraint-Based Learning
Test conditional independencies (via $\chi^2$ or mutual information):

**PC Algorithm**:
1. Start with complete undirected graph
2. Remove edges based on CI tests (increasing conditioning set size)
3. Orient edges using v-structures
4. Propagate orientations

**Grow-Shrink (GS)**: Find Markov blanket of each node, then orient edges.

## Parameter Learning

### Maximum Likelihood
For discrete nodes with multinomial conditional probability tables (CPTs):

$$\hat{\theta}_{ijk} = \frac{N_{ijk}}{N_{ij}}$$

where $N_{ijk}$ = count of $(X_i = k, \text{Pa}(X_i) = j)$.

### Bayesian Parameter Learning
Dirichlet prior $\text{Dir}(\alpha_{ijk})$:

$$\hat{\theta}_{ijk} = \frac{N_{ijk} + \alpha_{ijk}}{N_{ij} + \sum_k \alpha_{ijk}}$$

Equivalent to Laplace smoothing with prior counts $\alpha_{ijk}$.

### EM for Missing Data
E-step: compute expected sufficient statistics
M-step: MLE on expected counts

## Inference

### Exact Inference
- **Variable elimination**: Eliminate nodes one by one by summing over them. Complexity exponential in treewidth
- **Junction tree**: Cluster original graph into cliques, form tree of cliques. Exact inference in $O(\text{treewidth}^2 n)$

### Approximate Inference
- **Likelihood weighting**: Sample from prior, weight by evidence likelihood
- **Gibbs sampling**: Iteratively sample each variable given all others
- **Loopy belief propagation**: Apply BP on graphs with cycles (works well empirically)
- **Variational inference**: Approximate posterior with simpler distribution

## Code: Simple Bayesian Network Parameter Learning

```python
import numpy as np
from collections import defaultdict

class BayesianNetwork:
    def __init__(self, structure):
        # structure: dict {node: [parent_nodes]}
        self.structure = structure
        self.cpts = {}

    def fit(self, data):
        for node, parents in self.structure.items():
            counts = defaultdict(lambda: defaultdict(int))
            for row in data:
                key = tuple(row[p] for p in parents) if parents else ()
                counts[key][row[node]] += 1
            self.cpts[node] = {}
            for key, outcomes in counts.items():
                total = sum(outcomes.values())
                self.cpts[node][key] = {k: v/total for k, v in outcomes.items()}

    def query(self, node, evidence):
        parents = self.structure[node]
        key = tuple(evidence[p] for p in parents) if parents else ()
        return self.cpts[node][key]
```

## Practical Considerations
- **NP-hard structure learning**: Use heuristics or domain knowledge to constrain search
- **Small data**: Bayesian parameter learning (with prior) essential to avoid overfitting
- **Continuous variables**: Discretize or use conditional Gaussian networks
- **Causal interpretation**: Limited by hidden confounders (PC algorithm addresses this partially)
- **Treewidth**: Sparse graphs (low treewidth) enable efficient exact inference
- **Software**: `pgmpy` (Python), `bnlearn` (R), `Tetrad` (Java)

## Key Points
- $d!$ possible orderings — structure learning is NP-hard
- Model interpretability via DAG visualization (causal diagram)
- Handles missing data naturally via EM
- Causal interpretation limited without latent confounder control
- Exact inference complexity exponential in treewidth

## References
- Pearl, "Probabilistic Reasoning in Intelligent Systems" (1988)
- Koller & Friedman, "Probabilistic Graphical Models" (2009)
- Spirtes, Glymour, Scheines, "Causation, Prediction, and Search" (2000)
- Heckerman, "A Tutorial on Learning with Bayesian Networks" (1995)
- Chickering, "Learning Equivalence Classes of Bayesian-Network Structures" (JMLR, 2002)
