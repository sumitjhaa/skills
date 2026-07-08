# Lesson 05.43: Symbolic Regression

## Learning Objectives
- Understand genetic programming for symbolic expression discovery
- Implement tree-based GP with crossover and mutation
- Apply Pareto front analysis for accuracy vs complexity tradeoff
- Compare with neural network regression

## Genetic Programming (GP)
Evolves mathematical expressions to fit data:

**Terminals**: Variables ($x_1, x_2, \dots$), constants ($\pi, e, 1.0$)
**Functions**: $+, -, \times, \div, \sin, \cos, \exp, \log, \sqrt{\;}$

Expressions represented as trees (parsed). Evaluate fitness by matching data.

## Algorithm
1. **Initialize**: Random population of expression trees (ramped half-and-half: half full trees, half grow trees)
2. **Evaluate fitness**: $f(i) = \frac{1}{n} \sum_{j=1}^n (y_j - \text{eval}(T_i, x_j))^2$ (MSE)
3. **Selection**: Tournament (pick best among random $k$ individuals)
4. **Crossover**: Swap random subtrees between two parents
5. **Mutation**: Replace random subtree with random new tree
6. **Repeat** steps 2-5 for $G$ generations
7. Return best expression(s) from final population

### Crossover
1. Select random node in parent A
2. Select random node in parent B
3. Swap subtrees rooted at these nodes
4. Children may have different sizes

### Mutation
- **Subtree mutation**: Replace subtree with random tree
- **Point mutation**: Replace one node (function or terminal)
- **Hoist mutation**: Replace individual with one of its subtrees (reduces size)
- **Shrink mutation**: Replace subtree with a terminal

## Pareto Front
Multi-objective optimization: minimize both error and complexity:

$$\text{Fitness}(T) = \text{MSE}(T) + \lambda \cdot \text{size}(T)$$

- Size = number of nodes (or tree depth)
- Pareto front: set of expressions where no other expression has both lower MSE and smaller size
- Plot: error vs complexity — identify "knee" where tradeoff is optimal

## Bloat Control
GP tends to produce very large trees (bloat) because:
- Larger trees have more "opportunities" for crossover (depth bias)
- Protection from crossover damage (redundant subtrees)

**Controls**:
- **Parsimony pressure**: $\lambda \cdot \text{size}$ penalty
- **Maximum depth constraint**: Hard limit on tree size
- **Lexicographic selection**: First compare error, then size
- **Double tournament**: Tournament on error, then on size
- **Tarpeian method**: Randomly kill bloated individuals

## Comparison with Neural Networks

| Aspect | Symbolic Regression | Neural Networks |
|--------|-------------------|-----------------|
| Output | Interpretable expression | Black-box weights |
| Extrapolation | Can extrapolate logically | Often extrapolates poorly |
| Optimization | Evolutionary (stochastic) | Gradient-based |
| Input noise | Relatively robust | Regularization needed |
| Model size | Very compact (10-100 nodes) | Large ($10^3$-$10^6$ params) |
| High dimensions | Poor ($d > 10$) | Excellent |

## Code: Minimal GP

```python
import numpy as np

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def evaluate(node, x, constants):
    if node.value == '+': return evaluate(node.left, x, constants) + evaluate(node.right, x, constants)
    elif node.value == '-': return evaluate(node.left, x, constants) - evaluate(node.right, x, constants)
    elif node.value == '*': return evaluate(node.left, x, constants) * evaluate(node.right, x, constants)
    elif node.value == 'sin': return np.sin(evaluate(node.left, x, constants))
    elif node.value == 'x': return x
    elif isinstance(node.value, int): return constants[node.value]
    return node.value

def random_tree(depth, functions, constants, max_depth=3, full=False):
    if depth >= max_depth or (not full and np.random.random() < 0.3):
        if np.random.random() < 0.5:
            return Node(np.random.choice(constants))
        return Node('x')
    f = np.random.choice(functions)
    if f in ['sin', 'cos', 'exp', 'log', 'sqrt']:
        return Node(f, random_tree(depth+1, functions, constants, max_depth, full))
    return Node(f, random_tree(depth+1, functions, constants, max_depth, full),
                random_tree(depth+1, functions, constants, max_depth, full))

def size(node):
    if node is None: return 0
    return 1 + size(node.left) + size(node.right)
```

## Applications
- **Scientific discovery**: Kepler's laws, physics equations from experimental data
- **Financial modeling**: Interpretable trading rules, option pricing
- **Industrial control**: Simplified process models for control systems
- **Feature engineering**: Learned transformations for downstream ML

## References
- Koza, "Genetic Programming: On the Programming of Computers by Means of Natural Selection" (MIT Press, 1992)
- Schmidt & Lipson, "Distilling Free-Form Natural Laws from Experimental Data" (Science, 2009)
- Cranmer et al., "Discovering Symbolic Models from Deep Learning with Inductive Biases" (NeurIPS 2020)
- Virgolin et al., "A Survey on Genetic Programming for Symbolic Regression" (arXiv, 2022)
- Udrescu & Tegmark, "AI Feynman: A Physics-Inspired Method for Symbolic Regression" (Science Advances, 2020)
