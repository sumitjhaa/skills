# Lesson 05.32: Learning to Rank

## Learning Objectives
- Understand pointwise, pairwise, and listwise ranking approaches
- Implement RankNet loss and LambdaRank gradient
- Evaluate ranking with NDCG, MAP, and MRR
- Apply to search engine ranking and recommendation

## Problem Setup
Given queries $q$ and documents $d$, learn scoring function $f(q, d)$ ordering relevant documents above irrelevant ones.

Training data: $(q_i, \{d_{ij}\}, \{y_{ij}\})$ where $y_{ij}$ is relevance label (e.g., 0=bad, 1=fair, 2=good, 3=perfect).

## Pointwise Approach
Treat as regression/classification per query-document pair. Minimize:

$$L = \sum_i \sum_j L(y_{ij}, f(q_i, d_{ij}))$$

- Simple, but ignores ranking structure
- Standard regression or classification
- Suboptimal for ranking metrics

## Pairwise Approach
Minimize number of inverted pairs — cases where irrelevant document outranks relevant one.

### RankNet
Cross-entropy cost on pairwise comparisons:

$$P_{ij} = \frac{1}{1 + e^{-(s_i - s_j)}} \quad \text{(probability i should rank above j)}$$

$$C = -\bar{P}_{ij} \log P_{ij} - (1-\bar{P}_{ij}) \log(1 - P_{ij})$$

where $\bar{P}_{ij} = 1$ if document $i$ is more relevant than $j$, 0 otherwise.

Gradient w.r.t. model parameters:

$$\frac{\partial C}{\partial w} = \frac{\partial C}{\partial s_i} \frac{\partial s_i}{\partial w} + \frac{\partial C}{\partial s_j} \frac{\partial s_j}{\partial w}$$

### LambdaRank
Modify RankNet gradient to optimize NDCG directly:

$$\lambda_{ij} = \frac{-\sigma}{1 + e^{\sigma(s_i - s_j)}} |\Delta \text{NDCG}|$$

where $|\Delta \text{NDCG}|$ is the change in NDCG by swapping documents $i$ and $j$.

The gradient magnitude is scaled by the actual impact on NDCG — tricking the optimizer into directly optimizing the evaluation metric.

## Listwise Approach
Directly optimize ranking metrics or their smooth approximations.

### LambdaMART
Gradient boosting with LambdaRank gradients:
1. Train MART (Multiple Additive Regression Trees) on $\lambda$ gradients
2. Each tree fits pairwise gradients
3. Very effective in practice (winner of many competitions)

### SoftRank
Smooth version of ranking metrics using soft ranking:
- Approximate rank as expectation under smooth distribution
- Differentiable NDCG approximation

## Evaluation Metrics

### NDCG (Normalized Discounted Cumulative Gain)
$$\text{DCG}_k = \sum_{i=1}^k \frac{2^{\text{rel}_i} - 1}{\log_2(i+1)}$$

$$\text{NDCG}_k = \frac{\text{DCG}_k}{\text{IDCG}_k}$$

IDCG = ideal DCG (best possible ranking).

### MAP (Mean Average Precision)
$$\text{AP} = \frac{\sum_{k} P(k) \cdot \text{rel}(k)}{|\text{relevant documents}|}$$

$$\text{MAP} = \frac{1}{|Q|} \sum_{q=1}^{|Q|} \text{AP}_q$$

### MRR (Mean Reciprocal Rank)
$$\text{MRR} = \frac{1}{|Q|} \sum_{q=1}^{|Q|} \frac{1}{\text{rank}_q}$$

For tasks with exactly one relevant result (e.g., question answering).

## Code: LambdaRank Gradient

```python
import numpy as np
from itertools import combinations

def lambda_rank_gradients(scores, relevances):
    """Compute LambdaRank gradients for a query's documents"""
    n = len(scores)
    lambdas = np.zeros(n)
    for i, j in combinations(range(n), 2):
        if relevances[i] == relevances[j]:
            continue
        delta_ndcg = np.abs(ndcg_change(scores, relevances, i, j))
        lambda_ij = 2 * (relevances[i] - relevances[j]) / (1 + np.exp(scores[i] - scores[j]))
        lambdas[i] += lambda_ij * delta_ndcg
        lambdas[j] -= lambda_ij * delta_ndcg
    return lambdas

def ndcg_change(scores, rel, i, j, k=10):
    """NDCG change if documents i and j are swapped"""
    scores_copy = scores.copy()
    scores_copy[i], scores_copy[j] = scores_copy[j], scores_copy[i]
    return ndcg(scores, rel, k) - ndcg(scores_copy, rel, k)
```

## Feature Engineering
Common feature types:
- **Query-dependent**: TF-IDF, BM25, language model scores
- **Document quality**: PageRank, domain authority, freshness
- **User behavior**: Click-through rate, dwell time, bounce rate
- **Context**: Location, device, time of day
- **Diversity**: Topic coverage, result redundancy

## Practical Considerations
- **Pairwise sampling**: For large datasets, sample informative pairs (close scores)
- **Online learning**: Update ranking models incrementally from user clicks
- **Position bias**: Click models needed to debias implicit feedback
- **Calibration**: Ranking scores need not be probabilities — only relative order matters
- **Interleaving**: Online evaluation method comparing two ranking policies
- **Cold start**: Use content-based features when user interaction data is sparse

## Key Points
- Pairwise methods (RankNet, LambdaRank) are widely used in production
- Listwise methods better optimize ranking metrics directly
- Feature engineering is critical (query, document, user, context features)
- LambdaRank + MART (LambdaMART) is the most successful practical approach
- NDCG is the standard evaluation metric

## References
- Burges, "From RankNet to LambdaRank to LambdaMART: An Overview" (Technical Report, 2010)
- Joachims, "Optimizing Search Engines using Clickthrough Data" (KDD 2002)
- Liu, "Learning to Rank for Information Retrieval" (Foundations and Trends in IR, 2009)
- Burges et al., "Learning to Rank using Gradient Descent" (ICML 2005)
- Xu & Li, "AdaRank: A Boosting Algorithm for Information Retrieval" (SIGIR 2007)
