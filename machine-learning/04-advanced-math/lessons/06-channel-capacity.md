# 04.06 Channel Capacity and Blahut–Arimoto

## Motivation
Channel capacity is the maximum rate at which information can be reliably transmitted over a noisy channel. It is the central quantity of Shannon's noisy channel coding theorem and connects to error-correcting codes, distributed optimisation, and information-theoretic generalisation bounds in machine learning. The Blahut–Arimoto algorithm provides an efficient way to compute capacity for arbitrary discrete memoryless channels.

## Learning Objectives
- Define channel capacity as the maximum mutual information over input distributions.
- Derive capacity for classical channels (BSC, AWGN, binary erasure).
- Implement the Blahut–Arimoto algorithm for capacity computation.
- Apply channel capacity concepts to information-theoretic generalisation bounds and communication-efficient ML.

## Math Foundation

### Channel Model
A discrete memoryless channel (DMC) is defined by a transition matrix $p(y|x)$ for $x \in \mathcal{X}$, $y \in \mathcal{Y}$. The channel is memoryless because $p(y_1,\dots,y_n | x_1,\dots,x_n) = \prod_{t=1}^n p(y_t|x_t)$.

### Capacity Definition
The channel capacity $C$ is the maximum mutual information between input and output, maximised over input distributions:

$$C = \max_{p(x)} I(X;Y) = \max_{p(x)} \sum_{x,y} p(x) p(y|x) \log \frac{p(y|x)}{\sum_{x'} p(x') p(y|x')}$$

Capacity is measured in bits per channel use (base 2) or nats (base $e$).

### Properties
1. $0 \le C \le \log \min(|\mathcal{X}|, |\mathcal{Y}|)$.
2. $C$ is a concave function of $p(x)$ (since mutual information is concave in $p(x)$ for fixed $p(y|x)$).
3. $C$ is a convex function of $p(y|x)$.
4. The capacity-achieving distribution is often unique but may not be uniform.

## Classical Channels

### Binary Symmetric Channel (BSC)
A BSC with crossover probability $p$ flips each bit with probability $p$:

$$C_{\text{BSC}} = 1 - H(p) = 1 - p \log_2 \frac{1}{p} - (1-p) \log_2 \frac{1}{1-p}$$

The capacity-achieving input distribution is uniform: $p(0) = p(1) = 0.5$.

### Binary Erasure Channel (BEC)
A BEC with erasure probability $\epsilon$ erases (replaces with $?$) each bit with probability $\epsilon$:

$$C_{\text{BEC}} = 1 - \epsilon$$

The capacity-achieving distribution is uniform.

### Additive White Gaussian Noise (AWGN) Channel
For a continuous channel with input power constraint $\mathbb{E}[X^2] \le P$ and noise $Z \sim \mathcal{N}(0, N)$:

$$C_{\text{AWGN}} = \frac12 \log_2 \left( 1 + \frac{P}{N} \right) \text{ bits per channel use}$$

The capacity-achieving input distribution is Gaussian $\mathcal{N}(0, P)$. This is the Shannon-Hartley theorem.

### Multiple-Input Multiple-Output (MIMO) Channel
For a MIMO channel $\mathbf{y} = \mathbf{H}\mathbf{x} + \mathbf{n}$ with $n_t$ transmit and $n_r$ receive antennas:

$$C = \log_2 \det\left( \mathbf{I}_{n_r} + \frac{P}{n_t} \mathbf{H} \mathbf{H}^\dagger \right)$$

This demonstrates that MIMO systems offer capacity scaling linearly with $\min(n_t, n_r)$ at high SNR.

## Blahut–Arimoto Algorithm

The algorithm iteratively updates the input distribution to maximise $I(X;Y)$:

1. Initialise $p(x)$ (e.g., uniform).
2. Compute $r(x|y) = \frac{p(x) p(y|x)}{\sum_{x'} p(x') p(y|x')}$ (the posterior).
3. Update: $p(x) \leftarrow \frac{\exp\left( D_{\text{KL}}(p(y|x) \| \sum_{x'} p(x') p(y|x')) \right)}{\sum_{x''} \exp\left( D_{\text{KL}}(p(y|x'') \| \sum_{x'} p(x') p(y|x')) \right)}$.
4. Repeat until convergence. The capacity is the final $I(X;Y)$.

The algorithm is guaranteed to converge to the global optimum because $I(X;Y)$ is concave in $p(x)$.

```python
import numpy as np

def channel_capacity_ba(transition, max_iter=1000, tol=1e-12):
    """Blahut-Arimoto algorithm for channel capacity.
    
    Args:
        transition: matrix p(y|x) of shape (n_inputs, n_outputs)
    Returns:
        C: capacity (nats)
        p_opt: optimal input distribution
    """
    n_in, n_out = transition.shape
    p = np.ones(n_in) / n_in  # uniform initialisation
    
    for _ in range(max_iter):
        # joint p(x,y) = p(x) * p(y|x)
        joint = p[:, None] * transition
        
        # marginal p(y)
        py = joint.sum(axis=0)
        
        # conditional p(x|y) = joint / p(y)
        p_x_given_y = joint / (py[None, :] + 1e-12)
        
        # divergence D_KL(p(y|x) || p(y))
        div = np.sum(transition * (np.log(transition + 1e-12) - np.log(py[None, :] + 1e-12)), axis=1)
        
        # update p(x)
        p_new = np.exp(div)
        p_new /= p_new.sum()
        
        # check convergence
        if np.max(np.abs(p_new - p)) < tol:
            p = p_new
            break
        p = p_new
    
    # final mutual information
    joint = p[:, None] * transition
    px = p[:, None]
    py = joint.sum(axis=0)
    mi = np.sum(joint * np.log(joint / (px * py[None, :]) + 1e-12))
    
    return mi, p

# Example: BSC with crossover probability 0.1
bsc = np.array([[0.9, 0.1], [0.1, 0.9]])
C, p_opt = channel_capacity_ba(bsc)
# Also compute BSC capacity analytically
C_ana = 1.0 - (-0.1*np.log2(0.1) - 0.9*np.log2(0.9))
print(f"BSC(0.1) capacity (BA): {C/np.log(2):.6f} bits")
print(f"BSC(0.1) capacity (analytic): {C_ana:.6f} bits")

# Example: 3-input, 2-output asymmetric channel
chan = np.array([[0.8, 0.2], [0.6, 0.4], [0.3, 0.7]])
C2, p2 = channel_capacity_ba(chan)
print(f"Asymmetric channel capacity: {C2/np.log(2):.6f} bits")
print(f"Optimal input distribution: {p2}")
```

## Visualization
Plot the capacity of a BSC as a function of crossover probability $p$ — symmetric about $p=0.5$ with maximum 1 at $p=0$. For the Blahut-Arimoto algorithm, show the convergence of the estimate of $C$ across iterations for a randomly-initialised $3 \times 3$ channel. A third panel shows the optimal input distribution compared to uniform — note when they differ (asymmetric channels).

## Shannon's Noisy Channel Coding Theorem

The theorem states that for any rate $R < C$, there exists a sequence of codes of block length $n$ such that the maximum probability of error tends to zero as $n \to \infty$. Conversely, for any $R > C$, reliable communication is impossible — the error probability approaches 1 for any code.

### Proof Sketch
The proof uses random coding: generate $2^{nR}$ codewords i.i.d. from $p(x)$, and decode via joint typicality. The probability that a transmitted codeword is not uniquely determined by the channel output vanishes as $n$ grows, provided $R < C$. The converse uses Fano's inequality.

### Implications
- **Separation theorem**: source coding (compression) and channel coding (error correction) can be designed separately without loss of optimality.
- **Practical codes**: modern LDPC codes and polar codes achieve rates close to capacity with tractable decoding.
- **Finite blocklength**: for finite $n$, the maximal rate is $C - \sqrt{V/n} Q^{-1}(\epsilon) + O(\log n/n)$ where $V$ is the channel dispersion.

## Connections to Machine Learning

### Information-Theoretic Generalisation Bounds
The mutual information between the training data $S$ and the learned hypothesis $W$ bounds the generalisation gap:

$$\mathbb{E}[L(W) - \hat{L}(W)] \le \sqrt{\frac{I(W;S)}{2n}}$$

This follows from using the channel capacity of a "learning channel" $p(w|s)$. Tighter bounds use the conditional mutual information $I(W_i; Z_i | S_{i-1})$ analogous to the capacity of a channel with feedback.

### Communication-Efficient Distributed Learning
In federated learning, each client communicates a gradient or model update to a central server over a bandwidth-limited channel. The optimal compression strategy for the uplink channel is a rate–distortion problem where the distortion is the increase in loss. Gradient quantisation methods (e.g., QSGD, TernGrad) can be analysed as channel coding problems where the goal is to maximise the information per transmitted bit.

### Neural Network Capacity
The information bottleneck theory of deep learning posits that networks learn by compressing the input while preserving label information, analogous to transmitting information through a series of noisy channels (the layers). The capacity of each layer limits the information that can propagate, and the network's generalisation relates to the total information bottleneck capacity.

## Practical Considerations

### Algorithmic Details
- The Blahut–Arimoto algorithm converges geometrically — the error decreases as $\exp(-Cn)$ for $n$ iterations.
- For continuous channels (AWGN), the capacity-achieving distribution is continuous, but the algorithm can be applied by discretising the input space.
- For multiple-constraint channels (e.g., peak and average power), the optimisation is over $p(x)$ with additional constraints handled by Lagrange multipliers.

### Computing Capacity for Large Alphabets
When $|\mathcal{X}|$ is large, the BA iteration $O(|\mathcal{X}|^2)$ may be expensive. Alternatives include:
- **Gradient-based optimisation**: use the fact that $\nabla_{p(x)} I = D_{\text{KL}}(p(y|x) \| p(y)) - C$.
- **Blahut–Arimoto in dual form**: $C = \max_{p(x)} \min_{r(y)} \sum_{x,y} p(x) p(y|x) \log \frac{p(y|x)}{r(y)}$.
- **Monte Carlo Blahut–Arimoto**: sample inputs when $|\mathcal{X}|$ is large.

## References
- Cover & Thomas, *Elements of Information Theory*, 2nd ed.
- Shannon, "A Mathematical Theory of Communication," *Bell System Technical Journal*, 1948
- Blahut, "Computation of Channel Capacity and Rate-Distortion Functions," *IEEE Trans. Info. Theory*, 1972
- Arimoto, "An algorithm for computing the capacity of arbitrary discrete memoryless channels," *IEEE Trans. Info. Theory*, 1972
- Xu & Raginsky, "Information-Theoretic Analysis of Generalization Capability of Learning Algorithms," *NeurIPS 2017*
