# Lesson 05.49: Association Rules (Apriori, FP-Growth)

## Learning Objectives
- Understand frequent itemset mining and association rules
- Implement Apriori with candidate generation and pruning
- Implement FP-Growth with tree-based mining
- Evaluate rules with support, confidence, lift, conviction

## Basic Concepts
- **Itemset**: Set of items $I = \{i_1, \dots, i_k\}$ where each $i_j$ is from a set of possible items
- **$k$-itemset**: Itemset with $k$ items
- **Support**: $\text{supp}(I) = \frac{\text{count}(I)}{n}$ — fraction of transactions containing $I$
- **Confidence**: $\text{conf}(X \Rightarrow Y) = \frac{\text{supp}(X \cup Y)}{\text{supp}(X)}$ — conditional probability
- **Lift**: $\text{lift}(X \Rightarrow Y) = \frac{\text{supp}(X \cup Y)}{\text{supp}(X) \cdot \text{supp}(Y)}$ — independence measure
  - Lift = 1: independent
  - Lift > 1: positive correlation
  - Lift < 1: negative correlation
- **Conviction**: $\frac{1 - \text{supp}(Y)}{1 - \text{conf}(X \Rightarrow Y)}$ — how much rule depends on antecedent
- **Leverage**: $\text{supp}(X \cup Y) - \text{supp}(X) \cdot \text{supp}(Y)$
- **All-confidence**: $\min(\text{conf}(X \Rightarrow Y), \text{conf}(Y \Rightarrow X))$

## Apriori Algorithm
**Apriori principle**: All subsets of a frequent itemset must be frequent.

### Algorithm
```
F_1 = {frequent 1-itemsets}
k = 2
while F_{k-1} is not empty:
    C_k = apriori_gen(F_{k-1})  # candidate k-itemsets
    count support of C_k by scanning DB
    F_k = {c in C_k : support(c) >= min_supp}
    k += 1
return union of all F_k
```

**Apriori-gen**:
1. Join: $F_{k-1} \bowtie F_{k-1}$ — combine two $(k-1)$-itemsets sharing $k-2$ items
2. Prune: remove any $c \in C_k$ where a $(k-1)$-subset is not in $F_{k-1}$

### Complexity
- Worst-case $O(2^d)$ candidates
- Realistic: $O(\text{number of frequent itemsets})$
- Requires $k$ database scans for $k$ iterations

## FP-Growth (Frequent Pattern Tree)
Avoids candidate generation by compressing the database into a tree:

1. **FP-tree construction**:
   - Scan DB, count frequent items (sorted by frequency descending)
   - Build tree: each transaction → path; nodes share prefixes; count increments

2. **FP-tree mining**:
   - For each item (starting from least frequent):
     - Build conditional pattern base (paths ending in this item)
     - Build conditional FP-tree (recursively)
     - Generate patterns by concatenating suffix with frequent patterns from conditional tree

**Advantages**: Typically 10-100x faster than Apriori, no candidate generation.

## Rule Generation
From frequent itemset $Y = X \cup Y'$:
- Generate rule $X \Rightarrow Y'$
- Compute confidence: $\text{supp}(X \cup Y') / \text{supp}(X)$
- Keep if confidence $\geq$ min_conf

### Pruning
If $X' \Rightarrow Y'$ has confidence below threshold, any rule $X \subset X' \Rightarrow Y'$ will also have low confidence. Prune accordingly.

## Code: FP-Growth Simplified

```python
from collections import defaultdict

class FPTree:
    def __init__(self):
        self.root = {}
        self.header_table = defaultdict(list)

    def insert(self, items, count=1):
        node = self.root
        for item in items:
            if item not in node:
                node[item] = {}
            node[item]['count'] = node[item].get('count', 0) + count
            node = node[item]

def build_fp_tree(transactions, header_order):
    tree = FPTree()
    for t in transactions:
        ordered = [i for i in header_order if i in t]
        tree.insert(ordered)
    return tree
```

## Practical Considerations
- **min_supp choice**: Critical parameter — too low → too many rules, too high → missing rules
- **Data characteristics**: Apriori works well for sparse data (market baskets), FP-Growth for dense
- **Rule filtering**: Use lift > 1, conviction > 1, and confidence > threshold
- **Correlation ≠ causation**: Strong rules don't imply causal relationships
- **Redundant rules**: Among rules with same consequent, keep only the most interesting
- **Large data**: Use partition-based or sampling approximations

## Applications
- **Market basket analysis**: "Customers who bought X also bought Y"
- **Recommendation**: Cross-selling, product placement
- **Medical diagnosis**: Symptom-disease associations
- **Web usage mining**: Page visit patterns

## Key Points
- Apriori: $O(2^d)$ worst case, works well with pruning for sparse data
- FP-Growth: Typically 10x faster than Apriori
- min_supp choice critical — rule explosion at low thresholds
- Compare rules with lift, conviction, not just support/confidence
- Association ≠ causation

## References
- Agrawal, Imieliński, Swami, "Mining Association Rules between Sets of Items in Large Databases" (SIGMOD 1993)
- Agrawal & Srikant, "Fast Algorithms for Mining Association Rules" (VLDB 1994)
- Han, Pei, Yin, "Mining Frequent Patterns without Candidate Generation" (SIGMOD 2000)
- Tan, Steinbach, Kumar, "Introduction to Data Mining", Ch. 6
- Brin et al., "Dynamic Itemset Counting and Implication Rules for Market Basket Data" (SIGMOD 1997)
