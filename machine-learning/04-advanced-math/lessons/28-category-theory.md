# 04.28 Category Theory: Categories, Functors, Natural Transformations

## Motivation
Category theory abstracts mathematical structure into objects and morphisms, providing a unifying language for different areas of mathematics and ML — from functorial data analysis to the categorical foundations of deep learning and probabilistic programming. Understanding categories helps reason about compositionality, equivariance, and the structure of learning algorithms.

## Learning Objectives
- Define categories, functors, and natural transformations.
- Understand universal properties and adjoint functors.
- Apply categorical thinking to persistent homology, probabilistic programming, and backpropagation.
- Recognise monads as a structure for computational effects.

## Math Foundation

### Categories
A category $\mathcal{C}$ consists of:
- A collection of objects $\text{Ob}(\mathcal{C})$.
- For each pair $A, B$, a set $\text{Hom}_{\mathcal{C}}(A, B)$ of morphisms $f: A \to B$.
- Composition: $\circ: \text{Hom}(B, C) \times \text{Hom}(A, B) \to \text{Hom}(A, C)$.
- Identity morphism $\text{id}_A: A \to A$ for each $A$.
- Associativity: $(f \circ g) \circ h = f \circ (g \circ h)$.
- Identity: $f \circ \text{id}_A = f = \text{id}_B \circ f$.

**Examples**: $\mathbf{Set}$ (sets and functions), $\mathbf{Vec}_k$ (vector spaces and linear maps), $\mathbf{Top}$ (topological spaces and continuous maps), $\mathbf{Prob}$ (probability spaces and Markov kernels).

### Functors
A functor $F: \mathcal{C} \to \mathcal{D}$ maps objects to objects and morphisms to morphisms, preserving:
- Composition: $F(g \circ f) = F(g) \circ F(f)$.
- Identities: $F(\text{id}_A) = \text{id}_{F(A)}$.

**Examples**:
- **Forgetful functor**: $U: \mathbf{Vec} \to \mathbf{Set}$ forgets vector space structure.
- **Free functor**: $F: \mathbf{Set} \to \mathbf{Vec}$ sends a set to the free vector space on it.
- **Power set functor**: $\mathcal{P}: \mathbf{Set} \to \mathbf{Set}$ sends $X$ to $\mathcal{P}(X)$ and $f$ to the direct image.
- **Persistent homology**: $H_k: \mathbf{Fil} \to \mathbf{Pers}$ sends a filtered complex to its persistence module.

### Natural Transformations
A natural transformation $\eta: F \Rightarrow G$ between functors $F, G: \mathcal{C} \to \mathcal{D}$ is a family of morphisms $\eta_A: F(A) \to G(A)$ in $\mathcal{D}$ such that for every $f: A \to B$:

$$\eta_B \circ F(f) = G(f) \circ \eta_A$$

**Example**: The determinant $\det: GL_n \Rightarrow (-)^\times$ is a natural transformation from the general linear group functor to the multiplicative group functor.

### Yoneda Lemma
For any functor $F: \mathcal{C} \to \mathbf{Set}$ and object $A$:

$$\text{Nat}(\text{Hom}_{\mathcal{C}}(A, -), F) \cong F(A)$$

This says an object is completely determined by its relationship to all other objects (represented by the hom-functor $\text{Hom}(A,-)$). The Yoneda embedding $\mathcal{C} \to \mathbf{Set}^{\mathcal{C}^{\text{op}}}$ is fully faithful.

### Adjoint Functors
$F: \mathcal{C} \to \mathcal{D}$ and $G: \mathcal{D} \to \mathcal{C}$ are adjoint ($F \dashv G$) if:

$$\text{Hom}_{\mathcal{D}}(F A, B) \cong \text{Hom}_{\mathcal{C}}(A, G B)$$

naturally in $A$ and $B$. The unit $\eta: \text{id}_{\mathcal{C}} \Rightarrow GF$ and counit $\varepsilon: FG \Rightarrow \text{id}_{\mathcal{D}}$ satisfy the triangle identities.

### Monads
A monad on $\mathcal{C}$ is an endofunctor $T: \mathcal{C} \to \mathcal{C}$ with natural transformations:
- Unit: $\eta: \text{id}_{\mathcal{C}} \Rightarrow T$
- Multiplication: $\mu: T^2 \Rightarrow T$
satisfying associativity ($\mu \circ T\mu = \mu \circ \mu T$) and unit laws ($\mu \circ \eta T = \text{id}_T = \mu \circ T\eta$).

Monads capture computational effects: state, non-determinism, exceptions, probability. The Kleisli category of a monad has morphisms $A \to T B$ (effectful computations).

## Python Implementation

```python
import numpy as np
from typing import Callable, Any, TypeVar

# Categorical concepts in code

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

class Category:
    """Abstract base for a category."""
    def compose(self, f: Callable[[A], B], g: Callable[[B], C]) -> Callable[[A], C]:
        return lambda x: g(f(x))
    
    def identity(self, x: A) -> A:
        return x

class Monad(Category):
    """A monad on a category."""
    def __init__(self, functor: Callable, unit: Callable, bind: Callable):
        self.functor = functor  # T: obj -> obj
        self.unit = unit        # eta: A -> T A
        self.bind = bind        # bind: T A -> (A -> T B) -> T B
    
    def fmap(self, f: Callable[[A], B]):
        """Lift a function to the monad: fmap f = bind . (unit . f)"""
        return lambda x: self.bind(x)(lambda a: self.unit(f(a)))

# Example: Probability monad (distributions as categorical monad)
class Distribution:
    """Simple discrete probability distribution."""
    def __init__(self, probs: dict):
        self.probs = probs  # {outcome: probability}
    
    def expectation(self, f: Callable):
        return sum(p * f(x) for x, p in self.probs.items())

class ProbabilityMonad(Monad):
    """The probability monad on Set."""
    def __init__(self):
        def functor(X):
            return type('Dist', (), {})  # placeholder
        def unit(x):
            return Distribution({x: 1.0})
        def bind(dist: Distribution, f: Callable):
            result = {}
            for x, p in dist.probs.items():
                inner = f(x).probs
                for y, q in inner.items():
                    result[y] = result.get(y, 0) + p * q
            return Distribution(result)
        super().__init__(functor, unit, bind)

# Example: functor for data transformation
def persistent_homology_functor(K):
    """Functor from filtered simplicial complexes to persistence modules (sketch)."""
    return lambda epsilon: K[epsilon]  # returns homology at scale epsilon

# Example: natural transformation between functors
def natural_transformation_demo():
    """Illustrate a natural transformation between two functors."""
    # F(X) = X (identity), G(X) = list(X)
    # Natural transformation eta_X: X -> list(X) by x -> [x]
    def eta(x):
        return [x]
    # Check naturality: for any f: X -> Y,
    # eta_Y . f = list(f) . eta_X
    f = lambda x: x * 2
    x = 5
    lhs = eta(f(x))  # [10]
    rhs = list(map(f, eta(x)))  # map(f, [5]) = [10]
    print(f"Naturality holds: {lhs == rhs}")

natural_transformation_demo()

# Example: categorical composition in neural networks
def layer_compose(layers):
    """Compose neural network layers (as functions)."""
    def forward(x):
        for layer in layers:
            x = layer(x)
        return x
    return forward
```

## Visualization
Draw a commutative diagram illustrating a natural transformation $\eta: F \Rightarrow G$: two parallel functorial paths from $A$ to $F(B)$ and $G(B)$ commute. A second panel shows the Yoneda lemma as an embedding: the category $\mathcal{C}$ embeds fully faithfully into the category of presheaves $\mathbf{Set}^{\mathcal{C}^{\text{op}}}$.

## Connections to Machine Learning

### Functorial Data Analysis (Persistent Homology)
Persistent homology is a functor from the category of filtered topological spaces to the category of persistence modules (graded vector spaces with linear maps). The stability theorem is a statement about the Lipschitz property of this functor. Topological data analysis pipelines are functorial: composing data acquisition $\to$ filtration $\to$ homology $\to$ vectorisation is a sequence of functors.

### Categorical Probabilistic Programming
A probabilistic program is a morphism in the Kleisli category of the probability monad. The monad structure gives:
- $\eta$: deterministic computation.
- $\text{bind}$: sequential composition of probabilistic computations (conditioning, sampling). 
Libraries like MonadBayes (Haskell) and Pyro (implicitly) use monadic structure for modular probabilistic programming.

### Deep Learning as a Catamorphism
Backpropagation in neural networks can be viewed as a catamorphism (fold over the network structure). The categorical lens framework (Fong, Spivak, Tuyeras 2019) describes supervised learning as a functor from the category of network architectures to the category of learning algorithms, with the backpropagation of errors arising naturally from the functorial structure.

### Compositional Generalisation
Category theory formalises compositionality — the ability to understand a whole from its parts. Neural networks that exhibit compositional generalisation (e.g., systematic generalisation in question answering) can be understood as learning a functor from a syntactic category (parse trees) to a semantic category (vector space meanings). The DisCoCat framework models natural language as a category of string diagrams.

## Practical Considerations

### Why Category Theory?
- **Unification**: reveals common patterns across different areas (products, adjunctions, monads).
- **Compositionality**: categorical thinking encourages compositional, modular design.
- **Equivariance**: group actions and equivariant maps are naturally categorical.

### When Not to Use Category Theory
- Most practical ML does not require category theory.
- Categorical reasoning is abstract; implementation details (differentiability, numerical stability) are not captured.
- The main value is conceptual insight rather than practical tooling.

## References
- Mac Lane, *Categories for the Working Mathematician*, 2nd ed., Springer 1998
- Spivak, *Category Theory for the Sciences*, MIT Press 2014
- Fong, Spivak, Tuyeras, "Backprop as a Functor," *arXiv:1711.10455*, 2019
- Fong & Spivak, *An Invitation to Applied Category Theory: Seven Sketches in Compositionality*, Cambridge 2019
- Coecke & Kissinger, *Picturing Quantum Processes*, Cambridge 2017
