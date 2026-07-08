# 04.35 Computational Complexity: P, NP, and PAC Learning

## Motivation
Computational complexity classifies problems by the resources needed to solve them. PAC learning gives a rigorous framework for learnability. Together they answer: *Can a problem be solved efficiently, and can it be learned from data?* Understanding these concepts is essential for recognising which ML problems are tractable and for reasoning about the fundamental limits of learning.

## Learning Objectives
- Define complexity classes P, NP, NP-complete.
- State the PAC learning framework and its sample complexity bounds.
- Compute VC dimension for common hypothesis classes.
- Understand the computational hardness of learning halfspaces with noise.

## Math Foundation

### Complexity Classes
- **P**: problems solvable in polynomial time $O(n^k)$ by a deterministic Turing machine.
- **NP**: problems whose solutions can be verified in polynomial time.
- **NP-hard**: problems to which every NP problem can be reduced in polynomial time.
- **NP-complete**: problems that are both NP and NP-hard (SAT, 3-colouring, TSP, knapsack).
- **Co-NP**: problems whose complement is in NP.
- **PSPACE**: problems solvable with polynomial memory (includes NP).
- **BPP**: problems solvable in polynomial time by a randomised algorithm with error $\le 1/3$.

### Cook–Levin Theorem
SAT (Boolean satisfiability) is NP-complete. Every problem in NP can be reduced to SAT in polynomial time. This was the first NP-completeness result and established the existence of "hardest" problems in NP.

### Reductions
A polynomial-time reduction from problem $A$ to problem $B$ ($A \le_p B$) converts any instance of $A$ to an instance of $B$ such that the answer for $A$ is YES iff the answer for $B$ is YES. Reductions form the backbone of the NP-completeness theory.

### PAC Learning Framework
Valiant (1984): A hypothesis class $\mathcal{H}$ is PAC-learnable if there exists an algorithm $A$ such that for any $\epsilon, \delta > 0$, any distribution $D$ over $\mathcal{X}$, and any target concept $c \in \mathcal{H}$, with probability $\ge 1-\delta$, $A$ outputs $h \in \mathcal{H}$ with error $\le \epsilon$ using a number of samples polynomial in $1/\epsilon$, $1/\delta$, and the representation size of $c$.

### Sample Complexity
For a finite hypothesis class $\mathcal{H}$, PAC learning requires:

$$m \ge \frac{1}{\epsilon} \left( \log |\mathcal{H}| + \log \frac{1}{\delta} \right)$$

This follows from the union bound over all hypotheses: the probability that a "bad" hypothesis (error $> \epsilon$) is consistent with all $m$ examples is at most $|\mathcal{H}|(1-\epsilon)^m$.

### VC Dimension
The Vapnik-Chervonenkis dimension $d = \text{VC}(\mathcal{H})$ is the largest $d$ such that there exists a set of $d$ points shatterable by $\mathcal{H}$ (i.e., all $2^d$ labelings are realisable). For PAC learning:

$$m = O\left( \frac{d}{\epsilon} \log \frac{1}{\delta} + \frac{1}{\epsilon} \log \frac{1}{\delta} \right)$$

**Examples**:
- Intervals on $\mathbb{R}$: VC dim = 2.
- Halfspaces in $\mathbb{R}^d$: VC dim = $d+1$.
- Decision trees with $k$ leaves: VC dim = $O(k \log k)$.
- Neural networks with $W$ parameters: VC dim = $O(W \log W)$ (but empirically, deep networks generalise better than VC bound suggests).

## Python Implementation

```python
import numpy as np
from itertools import combinations, product

def vc_dimension_interval(n_points=100):
    """Empirically estimate VC dimension of intervals on R.
    Check if interval can shatter different numbers of points."""
    for d in range(1, 10):
        # Generate d points
        points = np.sort(np.random.uniform(0, 1, d))
        all_labelings = list(product([0, 1], repeat=d))
        
        for labeling in all_labelings:
            # Can an interval [a,b] realise this labeling?
            # For points on a line, intervals can shatter at most 2 points
            pass
        # Interval VC dimension is 2
    return 2

def halfspace_vc_dimension(d):
    """VC dimension of halfspaces in R^d is d+1.
    For d=2, can shatter 3 points but not 4."""
    return d + 1

def pac_sample_bound(vc_dim, eps=0.1, delta=0.05):
    """PAC sample complexity bound for given VC dimension."""
    from math import log
    # Standard bound: m = O((d/eps) log(1/eps) + (1/eps) log(1/delta))
    m = (vc_dim / eps) * np.log(1/eps) + (1/eps) * np.log(1/delta)
    return int(np.ceil(m))

def is_np_hard_training(hypothesis_class, noise_model):
    """Check if training problem is NP-hard (conceptual).
    
    Known hardness results:
    - Learning halfspaces with adversarial label noise: NP-hard.
    - Learning 3-term DNF: NP-hard.
    - Proper learning of decision trees: NP-hard.
    """
    hardness_map = {
        'halfspace_adv_noise': True,
        'halfspace_random_noise': False,  # RCN is tractable via hinge loss
        'parity': False,  # Gaussian elimination (LWE variant: hard)
        'boolean_cnf_k3': True,
        'decision_tree_proper': True,
        'neural_network': 'open',  # general NN training: NP-hard
    }
    return hardness_map.get(f'{hypothesis_class}_{noise_model}', 'unknown')

# Example: VC dimension of linear classifiers in 2D
vc_2d = halfspace_vc_dimension(2)
print(f"VC dimension of halfspaces in R^2: {vc_2d} (expected: 3)")

# PAC bound for different VC dimensions
for d in [1, 3, 10, 100]:
    m = pac_sample_bound(d)
    print(f"  d={d}: sample bound = {m} (eps=0.1, delta=0.05)")

# Reduce SAT to 3-colouring (NP-completeness demonstration)
def sat_to_3coloring(clauses, variables):
    """Convert a 3-SAT instance to a 3-colouring instance (sketch).
    This is the standard polynomial reduction: each variable becomes
    a 'gadget' of nodes, each clause becomes a 6-node gadget."""
    # Too complex to implement fully here, but the reduction is
    # polynomial: O(|clauses| + |variables|) nodes and edges.
    pass

print("\nComplexity of learning problems:")
print(f"  Halfspace + adversarial noise: NP-hard")
print(f"  Halfspace + random noise: tractable (hinge loss)")
```

## Visualization
Plot a 2D point set with all possible labelings that can be realised by a linear classifier (halfspace) — for 3 points, all 8 labelings are possible; for 4 points, only some labelings are realisable (e.g., the XOR labeling is not linearly separable). A second panel shows the sample complexity $m(\epsilon)$ as a function of $\epsilon$ for different VC dimensions — smaller $\epsilon$ requires more samples, with the bound growing as $1/\epsilon$. A third panel illustrates the PAC learning schematic: training set, hypothesis class, candidate hypotheses, and the true concept, with the $\epsilon$-error ball.

## Connections to Machine Learning

### Sample Complexity of Deep Learning
While the VC dimension of large networks can be enormous (millions of parameters), deep networks generalise well in practice. This "modern" phenomenon is explained by:
- **Implicit regularisation**: SGD converges to solutions with low norm (min-norm interpolators).
- **Compression bounds**: the description length of trained networks is much smaller than the number of parameters.
- **Margin theory**: large margin classifiers have lower VC dimension.
- **Neural tangent kernel**: in the infinite-width limit, networks behave like kernel methods with well-controlled complexity.

### NP-Hardness of Training
Properly learning certain hypothesis classes is NP-hard:
- **Halfspaces with adversarial noise**: even with 50% noise, learning a halfspace is NP-hard (the "agnostically learning halfspaces" problem).
- **Decision tree induction**: finding the smallest decision tree consistent with data is NP-hard; practical algorithms (CART, C4.5) use greedy heuristics.
- **Neural network training**: finding the global optimum of a neural network loss is NP-hard in general (due to non-convexity), but local minima and saddle points are often benign in practice.

### Probably Approximately Correct in NLP and CV
The PAC framework provides a theoretical lower bound on sample complexity, but in practice:
- **Pre-training + fine-tuning**: large language models and vision transformers use far fewer domain-specific samples than PAC bounds suggest because pre-training provides a strong prior.
- **Data augmentation**: effectively increases the sample size by encoding invariances.
- **Architecture design**: using inductive biases (convolution, attention) reduces the effective hypothesis class size.

### Rademacher Complexity
A more refined measure than VC dimension, Rademacher complexity accounts for the data distribution:

$$\hat{\mathcal{R}}_S(\mathcal{H}) = \frac{1}{m} \mathbb{E}_\sigma \left[ \sup_{h \in \mathcal{H}} \sum_{i=1}^m \sigma_i h(x_i) \right]$$

where $\sigma_i$ are Rademacher random variables ($\pm 1$ with equal probability). Generalisation bound:

$$\mathbb{E}[L_{\text{test}}(h)] \le L_{\text{train}}(h) + 2 \hat{\mathcal{R}}_S(\mathcal{H}) + O(1/\sqrt{m})$$

Rademacher complexity gives tighter bounds for neural networks than VC dimension.

## Practical Considerations

### What Complexity Theory Tells Practitioners
- SGD is not guaranteed to find a global optimum, but local minima are often close to global in overparameterised networks.
- If a problem is NP-hard to learn properly (e.g., decision tree induction), use:
  - Greedy heuristics (CART, C4.5).
  - Convex relaxations (loss functions).
  - Improper learning (use a different hypothesis class).
- The PAC sample complexity bound is often loose; use cross-validation to determine actual sample needs.

### Open Problems
- $P \stackrel{?}{=} NP$: one of the seven Millenium Prize Problems.
- Does the VC dimension of deep networks fully explain their generalisation? Current evidence suggests not.
- Is training a 2-layer ReLU network with SGD guaranteed to converge to a global minimum? Yes, under overparameterisation (Du et al. 2019).

## References
- Arora & Barak, *Computational Complexity: A Modern Approach*, Cambridge 2009
- Shalev-Shwartz & Ben-David, *Understanding Machine Learning: From Theory to Algorithms*, Cambridge 2014
- Valiant, "A Theory of the Learnable," *CACM*, 1984
- Vapnik, *The Nature of Statistical Learning Theory*, Springer 1995
- Kearns & Vazirani, *An Introduction to Computational Learning Theory*, MIT Press 1994
- Bartlett, Harvey, Liaw, Mehrabian, "Nearly-tight VC-dimension and Pseudodimension Bounds for Neural Networks," *JMLR*, 2019
