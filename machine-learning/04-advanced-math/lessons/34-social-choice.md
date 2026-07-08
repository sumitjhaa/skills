# 04.34 Social Choice and Voting Theory

## Motivation
Social choice theory studies how individual preferences are aggregated into collective decisions. Its impossibility theorems and fairness criteria inform the design of algorithmic fairness, recommender systems, and democratic AI alignment. Understanding Arrow's theorem, Condorcet paradoxes, and fair division is essential for building systems that aggregate diverse human preferences.

## Learning Objectives
- State and prove Arrow's impossibility theorem.
- Understand the Condorcet paradox and the median voter theorem.
- Apply social choice concepts to algorithmic fairness and rank aggregation.
- Analyse the properties of voting rules (Borda, plurality, STV).

## Math Foundation

### Preference Aggregation
A preference profile is a collection of $n$ rankings $\succ_1, \dots, \succ_n$ over a set of $m$ alternatives $\mathcal{A}$. A social welfare function $F$ maps profiles to a single ranking $\succ = F(\succ_1, \dots, \succ_n)$.

### Arrow's Impossibility Theorem
Arrow (1951) proved that for $m \ge 3$ alternatives, no social welfare function can satisfy all four conditions:
1. **Unrestricted domain**: works for all possible preference profiles.
2. **Pareto efficiency**: if every voter prefers $a$ to $b$, the social outcome ranks $a$ above $b$.
3. **Independence of irrelevant alternatives (IIA)**: the relative ranking of $a$ and $b$ depends only on individual rankings of $a$ and $b$, not on other alternatives.
4. **Non-dictatorship**: there is no voter whose ranking is always the social ranking.

Any function satisfying 1-3 is a dictatorship. This is a fundamental impossibility result — there is no "perfect" voting rule.

### Proof Sketch
1. Start with all voters ranking $b$ last. By Pareto, $b$ is last in social ranking.
2. Move $b$ up one voter at a time. There is a pivot voter $v^*$ where $b$ moves above all other alternatives.
3. Show $v^*$ is a dictator for any pairwise comparison not involving $b$.
4. Show $v^*$ is also decisive for comparisons involving $b$.

### Condorcet Paradox
Majority voting can produce cycles: three voters with preferences $A \succ B \succ C$, $B \succ C \succ A$, $C \succ A \succ B$ yield $A \succ B \succ C \succ A$ (majority prefers $A$ over $B$, $B$ over $C$, and $C$ over $A$).

### Median Voter Theorem
If preferences are single-peaked on a one-dimensional axis, the Condorcet winner (an alternative that beats every other in pairwise majority) exists and equals the median voter's peak. This explains why political parties converge to the centre in two-party systems.

### Gibbard–Satterthwaite Theorem
Every non-dictatorial voting rule that selects a single winner is manipulable: there exists a voter who can achieve a better outcome by misreporting their preferences. No voting system is strategy-proof (truthful) unless it is dictatorial.

### Common Voting Rules
| Rule | Description | Properties |
|------|------------|-----------|
| **Plurality** | Most first-choice votes wins | Simple, but ignores minority preferences |
| **Borda count** | $m-1$ points for 1st, $m-2$ for 2nd, etc. | Considers whole ranking, vulnerable to strategic nomination |
| **STV (Single Transferable Vote)** | Eliminate lowest, transfer votes | Reduces wasted votes, proportional |
| **Condorcet methods** | If a Condorcet winner exists, they win | Minimax, Schulze, ranked pairs |
| **Approval voting** | Vote for any number of candidates | Simple, expressive |

## Python Implementation

```python
import numpy as np
from itertools import permutations, combinations
from collections import Counter

def borda_score(ranking, m):
    """Borda score of each alternative given a ranking list.
    ranking: list of alternatives in order (1st to last)"""
    scores = np.zeros(m)
    for i, alt in enumerate(ranking):
        scores[alt] = m - 1 - i
    return scores

def borda_winner(profiles, m):
    """Aggregate Borda scores across voters."""
    total = np.zeros(m)
    for ranking in profiles:
        total += borda_score(ranking, m)
    return np.argmax(total), total

def condorcet_winner(profiles, m):
    """Find Condorcet winner if one exists."""
    # pairwise preference matrix: prefs[i,j] = count preferring i over j
    prefs = np.zeros((m, m))
    for ranking in profiles:
        for i in range(m):
            for j in range(i+1, m):
                prefs[ranking[i], ranking[j]] += 1  # i beats j
    
    for alt in range(m):
        if all(prefs[alt, j] > prefs[j, alt] for j in range(m) if j != alt):
            return alt
    return None  # No Condorcet winner (cycle exists)

def plurality_winner(profiles):
    """Most first-choice votes wins."""
    first_choices = [r[0] for r in profiles]
    counts = Counter(first_choices)
    return max(counts, key=counts.get)

def stv_winner(profiles, m, n_seats=1):
    """Single Transferable Vote (simplified: single winner)."""
    votes = [list(r) for r in profiles]  # copy rankings
    eliminated = set()
    n_voters = len(votes)
    quota = n_voters // (n_seats + 1) + 1
    
    while len(eliminated) < m - n_seats:
        # count first-choice votes (excluding eliminated)
        first_choices = []
        for v in votes:
            for alt in v:
                if alt not in eliminated:
                    first_choices.append(alt)
                    break
        
        counts = Counter(first_choices)
        if not counts:
            break
        
        # check if any candidate reaches quota
        winner = max(counts, key=counts.get)
        if counts[winner] >= quota or len(eliminated) == m - n_seats - 1:
            return winner
        
        # eliminate last-place candidate
        loser = min(counts, key=counts.get)
        eliminated.add(loser)
    
    return None

# Example: Condorcet paradox
profiles = [
    [0, 1, 2],  # A > B > C
    [1, 2, 0],  # B > C > A
    [2, 0, 1],  # C > A > B
]
m = 3

print("Condorcet paradox example:")
cw = condorcet_winner(profiles, m)
print(f"  Condorcet winner: {cw} (should be None — cycle)")
borda_alt, borda_scores = borda_winner(profiles, m)
print(f"  Borda winner: {borda_alt} with scores {borda_scores}")
print(f"  Plurality winner: {plurality_winner(profiles)}")

# Example: single-peaked preferences (Condorcet winner exists)
profiles_sp = [
    [0, 1, 2, 3],
    [1, 0, 2, 3],
    [1, 2, 0, 3],
    [2, 1, 3, 0],
    [2, 3, 1, 0],
]
cw_sp = condorcet_winner(profiles_sp, 4)
print(f"\nSingle-peaked Condorcet winner: {cw_sp}")
```

## Visualization
Plot a 2D policy space with voter ideal points and candidate positions. The Condorcet winner (if it exists) is the position that beats all others in pairwise majority — equivalent to the median voter in one dimension. A second panel shows the Borda scores for different candidates as a bar chart. A third panel illustrates Arrow's theorem: a heatmap showing which IIA axiom is violated by different voting rules.

## Connections to Machine Learning

### Algorithmic Fairness
Social choice theory provides impossibility theorems for fair classification. The "impossibility of fairness" results (Kleinberg et al. 2017) show that three natural fairness criteria (demographic parity, equalised odds, calibration) cannot all be satisfied simultaneously — an analogue of Arrow's theorem for algorithmic fairness.

### Rank Aggregation in Recommendation
Recommender systems aggregate user preferences into a ranked list. Methods include:
- **Borda count**: simple but sensitive to strategic voting (shilling attacks).
- **Condorcet methods**: robust but expensive for large candidate sets.
- **Learning to rank**: learn a ranking function from pairwise comparisons, analogous to preference aggregation.
- **Plackett-Luce**: probabilistic model of rankings parameterised by item strengths.

### Multi-Agent RL and Preference Aggregation
In multi-agent systems, agents may have different preferences over outcomes. Social choice mechanisms aggregate these preferences:
- **Majority voting**: simple but can cycle (Condorcet).
- **Utilitarian aggregation**: sum of utilities, requires inter-personal comparability.
- **Nash social welfare**: product of utilities, favours egalitarian outcomes.
- **Lexicographic preferences**: hierarchical preferences common in AI safety.

### AI Alignment
Aligning AI systems with human preferences is fundamentally a social choice problem:
- **RLHF**: learns a reward model from human preferences (pairwise comparisons), then optimises the policy. This performs a form of preference aggregation over the human raters.
- **Constitutional AI**: uses a set of principles (a "constitution") to constrain behaviour, analogous to a social contract.
- **Direct preference learning**: methods like DPO and SLiC learn from preference data without explicit reward models.

## Practical Considerations

### Computational Aspects
- Computing the Condorcet winner: $O(nm^2)$ pairwise comparisons.
- Schulze method (beatpath): $O(m^3)$ via Floyd-Warshall on the pairwise margin matrix.
- STV: $O(nm^2)$ in practice.
- For large-scale rank aggregation (e.g., web search), use approximate methods or local kemenisation.

### Strategic Voting
- All non-dictatorial voting rules are manipulable (Gibbard-Satterthwaite).
- In practice, manipulation requires detailed knowledge of others' preferences.
- Some rules (e.g., quadratic voting) are harder to manipulate than others.

## References
- Arrow, *Social Choice and Individual Values*, 2nd ed., Yale 1963
- Sen, *Collective Choice and Social Welfare*, Holden-Day 1970
- Moulin, *Fair Division and Collective Welfare*, MIT Press 2003
- Brandt et al., *Handbook of Computational Social Choice*, Cambridge 2016
- Kleinberg, Mullainathan, Raghavan, "Inherent Trade-Offs in the Fair Determination of Risk Scores," *ITCS 2017*
- Christiano et al., "Deep Reinforcement Learning from Human Preferences," *NeurIPS 2017*
