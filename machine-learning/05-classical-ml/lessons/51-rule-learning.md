# Lesson 05.51: Rule Learning (CN2, RIPPER)

## Learning Objectives
- Understand separate-and-conquer rule induction
- Implement CN2 beam search for rule discovery
- Apply RIPPER for efficient rule set learning
- Analyze bias-variance in rule-based models

## Separate-and-Conquer
Learn rules sequentially, removing covered positive examples:

1. Find best rule covering current data
2. Remove examples covered by rule
3. Repeat until stopping criterion met
4. Optionally: prune or optimize rule set

**Why "separate-and-conquer"**: Each rule focuses on remaining uncovered examples.

## CN2 Algorithm
Induces ordered or unordered rule sets.

### Search
Beam search for best rule (general-to-specific):

```
beam = [empty rule (all examples covered)]
while beam not empty:
    candidates = []
    for rule in beam:
        candidates += specialize(rule)
    beam = select_best_k(candidates, quality)
```

**Specialization**: Add a condition (feature = value) to a rule.
**Beam width**: Usually 5-10.

### Rule Quality
- **Laplace estimate**: $\frac{p+1}{p+n+|C|}$ — corrected accuracy avoiding zero
- **Entropy**: Information gain of rule vs default
- **Likelihood ratio statistic**: $2 \sum_j n_j \log(n_j / e_j)$

### Pruning in CN2
Use likelihood ratio statistic:
$$\text{LR} = 2 \sum_j n_j \log(n_j / e_j)$$

- $n_j$: observed class frequencies in covered instances
- $e_j$: expected frequencies under null (no rule effect)

Stop adding conditions when LR improvement is not statistically significant.

## RIPPER (Repeated Incremental Pruning to Produce Error Reduction)

### IREP (Incremental Reduced Error Pruning)
1. Split data: 2/3 grow, 1/3 prune
2. Grow rule by adding conditions until no false negatives remain
3. Prune rule greedily: remove final condition if it reduces error on pruning set

Pruning metric: $(p-n)/(p+n)$ where $p$ = true positives, $n$ = false positives.

### RIPPER Optimization
1. **Build phase**: Repeatedly grow + prune rules for each class (from least to most frequent)
2. **Prune phase**: Simplify each rule, considering:
   - Replacement: replace rule with simpler rule covering subset
   - Revision: add conditions to rule
   - Keep if it improves pruning-set error
3. **Optimize phase**: For each rule in turn:
   - Consider two alternatives: replacement and revision
   - Pick the one minimizing description length

### MDL-Based Stopping
Stop adding rules when description length of rule set exceeds description length without rules:

$$\text{Description length} = \text{bits to encode rules} + \text{bits to encode exceptions}$$

## CN2 vs RIPPER

| Aspect | CN2 | RIPPER |
|--------|-----|--------|
| Search | Beam search | Greedy |
| Pruning | Likelihood ratio | Reduced error |
| Output | Ordered/unordered | Ordered rule list |
| Complexity | $O(b \cdot d \cdot v \cdot n)$ | $O(r \cdot d \cdot n)$ |
| Overfitting | Less (beam helps) | More (greedy) |
| Interpretability | Good | Good |

## Code: Simple CN2 Rule Inducer

```python
import numpy as np
from collections import Counter

def cn2_induction(X, y, beam_width=5, max_conditions=3):
    n, d = X.shape
    rules = []
    remaining = np.ones(n, dtype=bool)
    while np.sum(remaining) > 0 and len(rules) < 10:
        beam = [([], [])]  # (conditions, covered_indices)
        for _ in range(max_conditions):
            new_beam = []
            for conditions, covered in beam:
                # Specialize
                for feat in range(d):
                    for val in np.unique(X[remaining, feat]):
                        new_cond = conditions + [(feat, val)]
                        new_covered = np.all([X[:, f] == v for f, v in new_cond], axis=0) & remaining
                        if np.sum(new_covered) > 0:
                            new_beam.append((new_cond, new_covered))
            beam = sorted(new_beam, key=lambda x: laplace_quality(x[1], y), reverse=True)[:beam_width]
        if beam:
            best_rule, covered = beam[0]
            rules.append(best_rule)
            remaining[covered] = False
    return rules
```

## Advantages
- **Interpretable**: If-then rules are human-readable
- **Mixed features**: Handle numeric and categorical naturally
- **Missing values**: Naturally handled by condition checks
- **Efficient**: RIPPER scales to $10^5$+ instances
- **Modular**: Add/remove rules without retraining

## Limitations
- **Axis-aligned**: Only feature-value condition splits
- **Complex boundaries**: Need many rules for non-axis-aligned patterns
- **Noise sensitivity**: Outliers can induce spurious rules
- **Fragility**: Small data changes can change rule set significantly
- **Overlap**: Rules may conflict (especially unordered sets)

## References
- Clark & Niblett, "The CN2 Induction Algorithm" (Machine Learning, 1989)
- Cohen, "Fast Effective Rule Induction" (ICML 1995)
- Furnkranz, "Separate-and-Conquer Rule Learning" (AI Review, 1999)
- Quinlan, "Learning Logical Definitions from Relations" (Machine Learning, 1990)
- Witten & Frank, "Data Mining", Ch. 6 (Rules)
