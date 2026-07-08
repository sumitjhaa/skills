# Lesson 07.26: Neural-Symbolic Integration

## Learning Objectives
- Understand how neural and symbolic systems complement each other
- Implement differentiable logic constraints (LTN, DeepProbLog)
- Apply neural theorem proving for mathematical reasoning
- Design neuro-symbolic architectures for interpretable AI

## Theory
Neural-symbolic AI integrates neural networks (pattern recognition, learning) with symbolic reasoning (logic, rules, interpretability).

### Complementary Strengths
| Aspect | Neural | Symbolic |
|--------|--------|----------|
| Learning | From data (gradient-based) | From rules (deductive) |
| Interpretability | Low (black box) | High (explicit rules) |
| Robustness | Good (noisy data) | Brittle (exact matching) |
| Reasoning | Implicit | Explicit, verifiable |
| Generalization | Interpolation | Extrapolation |

## LTN (Logic Tensor Networks)

### Real-Valued Logic
Replace Boolean truth values with continuous values in $[0, 1]$:

$$\text{Truth}(A \land B) = \min(\text{Truth}(A), \text{Truth}(B))$$
$$\text{Truth}(A \lor B) = \max(\text{Truth}(A), \text{Truth}(B))$$
$$\text{Truth}(\lnot A) = 1 - \text{Truth}(A)$$

### Grounding
Map symbols to neural representations:
- Constants $c \to \text{Embedding}(c) \in \mathbb{R}^d$
- Predicates $P \to \text{NN}(x)$ that outputs truth value or probability
- Functions $f \to f(x)$ that transforms embeddings

### Loss from Logic
$$\mathcal{L}_{\text{logic}} = \sum_{\text{rules } r} (1 - \text{satisfiability}(r))$$

Backpropagate through logic constraints to update neural weights.

## DeepProbLog

### Probabilistic Logic Programming
Extend Prolog with neural predicates:

$$p(X, Y) \leftarrow q(X), \text{NeuralPredicate}(X, Y)$$

- Neural predicates: Output probability distribution over possible groundings
- Logic inference: Combines probabilities according to logical rules
- Training: Maximize likelihood of observed facts via backprop

## Neural Theorem Proving

### Differentiable Proof Search
Score each possible proof step via neural network:

$$s(\text{proof}_i) = \prod_{t=1}^T \text{NN}_\theta(\text{step}_t)$$

- Forward: Search over proof trees (beam search)
- Backward: Score gradients guide search toward correct proofs

### Graph Neural Network Reasoners (GNN-R)
Represent knowledge graph as graph, use GNN to reason:
- Nodes: entities
- Edges: relations
- Message passing implements logical inference

## Program Synthesis

### Neural-Guided Search
```
NN suggests next program token → Search verifies candidates → Best program
```

- **Sketch-guided**: NN fills holes in program sketch
- **Execution-guided**: Use program execution results as features

### Key Approaches
| Method | Strategy | Representative |
|--------|----------|---------------|
| DreamCoder | Wake-sleep: generate programs, compress | Ellis et al. |
| DeepCoder | NN predicts likely program tokens | Balog et al. |
| AlphaDev | RL for algorithm discovery | Mankowitz et al. |
| Codex/LM | LLM generates code from prompts | Chen et al. |

## Code: Simple LTN Implementation

```python
import torch
import torch.nn as nn

class LogicTensorNetwork:
    """Simplified LTN with grounded predicates"""
    
    @staticmethod
    def conjunction(*args):
        return torch.min(torch.stack(args), dim=0)[0]
    
    @staticmethod
    def disjunction(*args):
        return torch.max(torch.stack(args), dim=0)[0]
    
    @staticmethod
    def negation(x):
        return 1 - x
    
    @staticmethod
    def implication(a, b):
        return torch.max(1 - a, b)

class GroundedPredicate(nn.Module):
    def __init__(self, embedding_dim):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(embedding_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid(),
        )

    def forward(self, x):
        return self.mlp(x).squeeze(-1)

# Example: "If it's a bird, it can fly" constraint
def bird_fly_constraint(bird_pred, fly_pred, embeddings):
    bird_prob = bird_pred(embeddings)
    fly_prob = fly_pred(embeddings)
    # Rule: bird(x) → fly(x)
    rule_satisfaction = 1 - bird_prob * (1 - fly_prob)
    return torch.mean(1 - rule_satisfaction)  # loss
```

## Applications
- **Visual question answering**: Neural perception + symbolic reasoning on scenes
- **Scientific discovery**: Extract symbolic equations from neural observations
- **Interpretable classification**: Rule-based explanations from learned concepts
- **Robotics**: Task planning with learned skills + logic constraints
- **Math reasoning**: Neural theorem proving for automated deduction

## Challenges
- **Differentiability**: Discrete logic operations need continuous relaxations
- **Scalability**: Symbolic reasoning is NP-hard in worst case
- **Grounding**: Connecting symbols to continuous perception is difficult
- **Knowledge integration**: Merging learned rules with expert knowledge
- **Evaluation**: Benchmarks for neural-symbolic systems are limited

## References
- Garcez, Broda, Gabbay, "Neural-Symbolic Learning and Reasoning", Springer 2015
- Manhaeve, Dumancic, Kimmig, Demeyer, De Raedt, "DeepProbLog: Neural Probabilistic Logic Programming", NeurIPS 2018
- Serafini & Garcez, "Logic Tensor Networks: Deep Learning and Logical Reasoning from Data and Knowledge", 2016
- Ellis, Wong, Nye, Sable-Meyer, et al., "DreamCoder: Bootstrapping Inductive Program Synthesis with Wake-Sleep Library Learning", PLDI 2021
- Selsam, Lamm, Benedikt, Liang, Finkbeiner, "Learning to Reason: Learning SMT Solvers", ICLR 2019
