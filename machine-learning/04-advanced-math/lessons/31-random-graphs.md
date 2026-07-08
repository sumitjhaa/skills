# 04.31 Random Graphs and Percolation Theory

## Motivation
Random graphs model complex networks — social networks, biological networks, the internet. Percolation theory describes connectivity in random media. Both are essential for understanding graph-based learning, epidemic modelling, and network resilience. The phase transition from disconnected to connected networks has profound implications for GNN training, information diffusion, and community detection.

## Learning Objectives
- Define the Erdős–Rényi model and its phase transition for the giant component.
- Describe small-world and scale-free network models.
- Apply percolation theory to connectivity and robustness.
- Analyse community detection in the stochastic block model.

## Math Foundation

### Erdős–Rényi Model $G(n,p)$
Each of the $\binom{n}{2}$ possible edges is present independently with probability $p$. Properties:
- **Expected degree**: $\langle d \rangle = p(n-1) \approx np$.
- **Degree distribution**: Binomial($n-1, p$), Poisson($np$) for large $n$.
- **Phase transition**: as $np$ passes through 1, the graph undergoes a dramatic change:
  - $np < 1$: all components are $O(\log n)$ (subcritical).
  - $np = 1$: largest component is $O(n^{2/3})$ (critical).
  - $np > 1$: unique giant component of size $\Theta(n)$, plus small components of size $O(\log n)$ (supercritical).
  - $np = \log n$: graph becomes connected (with high probability).

### Giant Component Size
In the supercritical regime, the giant component fraction $S = |C_1|/n$ satisfies:

$$S = 1 - e^{-npS}$$

This implicit equation has a non-zero solution for $np > 1$.

### Small-World Networks (Watts–Strogatz)
Start with a regular ring lattice (each node connected to $k$ nearest neighbours), then rewire each edge with probability $q$:
- $q = 0$: regular lattice, high clustering, long path lengths.
- $q = 1$: random graph, low clustering, short path lengths.
- $0 < q \ll 1$: **small-world** — high clustering (regular) + short path lengths (random).

### Scale-Free Networks (Barabási–Albert)
Growth with preferential attachment: new nodes connect to existing nodes with probability proportional to degree. Yields power-law degree distribution:

$$P(k) \propto k^{-\gamma}, \quad \gamma = 3$$

Scale-free networks are robust to random failures but vulnerable to targeted attacks (hub removal).

### Percolation
- **Bond percolation**: each edge of a lattice is "open" with probability $p$, "closed" with probability $1-p$.
- **Site percolation**: each site is open with probability $p$.
- **Critical probability** $p_c$: threshold above which an infinite open cluster exists.
- For bond percolation on $\mathbb{Z}^2$, $p_c = 1/2$ (Kesten 1980).

### Stochastic Block Model (SBM)
Nodes are assigned to communities $c_i \in \{1,\dots,K\}$. Edges exist with probability $p_{\text{in}}$ within communities and $p_{\text{out}}$ between communities. The detectability threshold (Decelle et al. 2011) is:

$$\epsilon = \frac{p_{\text{out}}}{p_{\text{in}}}, \quad \epsilon_c = \frac{\sqrt{c} - 1}{\sqrt{c} + 1}$$

where $c = np$ is the average degree. Below $\epsilon_c$, no algorithm can detect communities better than chance.

## Python Implementation

```python
import numpy as np
from scipy.special import lambertw

def erdos_renyi(n, p):
    """Generate G(n, p) random graph adjacency matrix."""
    A = np.random.rand(n, n) < p
    A = np.triu(A, 1) + np.triu(A, 1).T
    return A.astype(float)

def giant_component_fraction(A):
    """Compute size of giant component via BFS."""
    n = A.shape[0]
    visited = np.zeros(n, dtype=bool)
    max_comp = 0
    
    for start in range(n):
        if visited[start]:
            continue
        # BFS
        queue = [start]
        visited[start] = True
        comp_size = 0
        while queue:
            v = queue.pop(0)
            comp_size += 1
            neighbors = np.where(A[v] > 0)[0]
            for u in neighbors:
                if not visited[u]:
                    visited[u] = True
                    queue.append(u)
        max_comp = max(max_comp, comp_size)
    
    return max_comp / n

def giant_component_theory(c):
    """Theoretical giant component fraction for G(n, c/n).
    S = 1 - exp(-c * S). Solution via Lambert W."""
    if c <= 1:
        return 0.0
    # Solve S = 1 - exp(-c*S) => (-c*S) * exp(-c*S) = -c * exp(-c)
    # => -c*S = W(-c * exp(-c))
    w = lambertw(-c * np.exp(-c), k=-1)  # lower branch
    S = 1 + w / c
    return float(np.real(S))

def barabasi_albert(n, m0=5, m=2):
    """Generate Barabasi-Albert scale-free network."""
    # Start with m0 fully connected nodes
    A = np.zeros((n, n))
    degrees = np.zeros(n)
    
    for i in range(m0):
        for j in range(i+1, m0):
            A[i, j] = A[j, i] = 1
            degrees[i] += 1
            degrees[j] += 1
    
    # Add remaining nodes with preferential attachment
    for new_node in range(m0, n):
        probs = degrees[:new_node] / max(degrees[:new_node].sum(), 1e-10)
        # Connect to m distinct existing nodes
        targets = np.random.choice(new_node, size=m, p=probs, replace=False)
        for t in targets:
            A[new_node, t] = A[t, new_node] = 1
            degrees[new_node] += 1
            degrees[t] += 1
    
    return A

# Example: giant component as function of c
print("Giant component fraction vs average degree c:")
for c in [0.5, 0.8, 1.0, 1.5, 2.0, 3.0]:
    A = erdos_renyi(500, c / 500)
    S_emp = giant_component_fraction(A)
    S_theory = giant_component_theory(c)
    print(f"  c={c:.1f}: empirical S={S_emp:.3f}, theory S={S_theory:.3f}")

# Degree distribution of scale-free network
A_sf = barabasi_albert(1000)
degrees = np.sum(A_sf, axis=1)
deg_counts = np.bincount(degrees.astype(int))
print(f"\nScale-free network stats:")
print(f"  Max degree: {degrees.max():.0f}")
print(f"  Mean degree: {degrees.mean():.2f}")
```

## Visualization
Plot the giant component fraction $S$ vs average degree $c$ for Erdős–Rényi graphs — the phase transition at $c=1$ is sharp. A second panel shows the degree distribution of a Barabási–Albert network on a log-log plot: the power-law tail $P(k) \propto k^{-3}$ appears as a straight line. A third panel shows the percolation threshold on a 2D lattice: below $p_c$, only finite clusters; above $p_c$, a spanning cluster exists.

## Connections to Machine Learning

### GNNs on Random Graphs
Graph neural networks generalise differently on random vs structured graphs:
- On Erdős–Rényi graphs, GNNs benefit from the lack of long-range dependencies and can achieve good performance with few layers.
- On scale-free graphs, GNNs struggle with high-degree hub nodes (oversmoothing, neighbourhood explosion).
- Many GNN datasets (Cora, Citeseer) have degree distributions closer to power-law than Poisson.

### Community Detection
The stochastic block model is the canonical generative model for community detection. Modern methods:
- **Spectral clustering**: eigenvectors of the graph Laplacian or non-backtracking matrix.
- **Belief propagation**: optimal algorithm near the detectability threshold.
- **Variational inference**: scalable SBM inference via VI.
- **Deep learning**: GNN-based community detection (DMoN, NOCD).

### Network Robustness
Percolation theory quantifies network resilience:
- **Random failure**: scale-free networks are robust (need to remove > 80% of nodes randomly to break connectivity).
- **Targeted attack**: scale-free networks are fragile (removing the top 5% of hubs disconnects the network).
- **Graph adversarial attacks**: GNNs can be attacked by perturbing edges or nodes to maximise misclassification — percolation theory explains why removing certain edges is maximally disruptive.

### Epidemiology on Networks
Disease spread on contact networks is a percolation process:
- SIR model: each infected node transmits to each neighbour with probability $p$ (bond percolation).
- Epidemic threshold: $p_c = \langle d \rangle / \langle d^2 - d \rangle$ (heterogeneous networks have lower thresholds).
- Graph neural networks for epidemic forecasting learn the percolation dynamics on the contact graph.

## Practical Considerations

### Finite Size Effects
- Phase transitions are sharp only in the $n \to \infty$ limit. For finite $n$, the transition is smoothed over a critical window of width $n^{-1/3}$ (for Erdős–Rényi).
- Empirical random graphs may appear disconnected even above the percolation threshold if $n$ is small.

### Generating Realistic Graphs
Real networks often have properties not captured by basic models:
- **Degree correlations**: assortative vs disassortative mixing.
- **Clustering**: higher than in ER or BA models.
- **Community structure**: hierarchical, overlapping.
- Use the configuration model with prescribed degree sequence, or the LFR benchmark for community structure.

## References
- Bollobás, *Random Graphs*, 2nd ed., Cambridge 2001
- Newman, *Networks: An Introduction*, Oxford 2010
- Barabási, *Network Science*, Cambridge 2016
- Erdős & Rényi, "On the Evolution of Random Graphs," *Publ. Math. Inst. Hung. Acad. Sci.*, 1960
- Watts & Strogatz, "Collective Dynamics of 'Small-World' Networks," *Nature*, 1998
- Barabási & Albert, "Emergence of Scaling in Random Networks," *Science*, 1999
- Decelle et al., "Inference and Phase Transitions in the Detection of Modules in Sparse Networks," *Physical Review E*, 2011
