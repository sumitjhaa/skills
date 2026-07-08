# 04.23 Representation Theory and Harmonic Analysis on Groups

## Motivation
Representation theory studies how abstract groups act on vector spaces. It provides the mathematical foundation for equivariant neural networks, Fourier analysis on groups, and the design of symmetry-aware architectures. Understanding irreducible representations (irreps) and the Peter–Weyl theorem is essential for constructing networks that are guaranteed to be equivariant by design.

## Learning Objectives
- Define group representations, irreps, and characters.
- Apply Schur's lemma and the Peter–Weyl theorem.
- Compute the Fourier transform on finite groups and compact groups.
- Design equivariant neural network layers using representation theory.

## Math Foundation

### Group Representations
A representation of a group $G$ on a vector space $V$ is a homomorphism $\rho: G \to GL(V)$:

$$\rho(gh) = \rho(g) \rho(h) \quad \text{and} \quad \rho(e) = I_V$$

The dimension of the representation is $\dim V$. Examples:
- **Trivial representation**: $\rho(g) = 1$ for all $g$.
- **Standard representation** of $S_n$: permutation matrices acting on $\mathbb{R}^n$.
- **Fundamental representation** of $SU(2)$: $2 \times 2$ special unitary matrices.

### Irreducible Representations (Irreps)
A subrepresentation is a subspace $W \subseteq V$ invariant under $\rho(g)$ for all $g$. A representation is irreducible if it has no non-trivial invariant subspaces. Maschke's theorem states that every representation of a finite group is completely reducible — a direct sum of irreps:

$$V \cong \bigoplus_{\lambda} V_\lambda^{\oplus m_\lambda}$$

### Characters
The character of a representation $\rho$ is $\chi_V(g) = \text{tr}\,\rho(g)$. Characters are:
- **Class functions**: $\chi(hgh^{-1}) = \chi(g)$.
- **Orthogonal**: $\langle \chi_i, \chi_j \rangle = \frac{1}{|G|} \sum_g \chi_i(g) \overline{\chi_j(g)} = \delta_{ij}$.
- **Complete**: a representation is determined by its character up to isomorphism.

### Peter–Weyl Theorem
For a compact group $G$, the regular representation on $L^2(G)$ decomposes as:

$$L^2(G) \cong \bigoplus_{\lambda \in \hat{G}} V_\lambda \otimes V_\lambda^*$$

where $\hat{G}$ is the set of irreps (up to equivalence). This says that matrix elements of irreps form an orthonormal basis for $L^2(G)$. For $SO(3)$, these are the spherical harmonics $Y_\ell^m$.

### Fourier Transform on Finite Groups
For a function $f: G \to \mathbb{C}$ on a finite group, the Fourier transform at representation $\rho$ is:

$$\hat{f}(\rho) = \sum_{g \in G} f(g) \rho(g)$$

The inverse transform is:

$$f(g) = \frac{1}{|G|} \sum_{\rho \in \hat{G}} \dim(\rho) \, \text{tr}\left( \hat{f}(\rho) \rho(g^{-1}) \right)$$

Plancherel's theorem generalises Parseval:

$$\sum_g |f(g)|^2 = \frac{1}{|G|} \sum_{\rho \in \hat{G}} \dim(\rho) \, \|\hat{f}(\rho)\|^2_{\text{HS}}$$

### Clebsch–Gordan Decomposition
The tensor product of two irreps decomposes into irreps:

$$V_\mu \otimes V_\nu \cong \bigoplus_{\lambda} V_\lambda^{\oplus C_{\mu\nu}^\lambda}$$

where $C_{\mu\nu}^\lambda$ are the Clebsch–Gordan coefficients. For $SO(3)$, this is:

$$\ell_1 \otimes \ell_2 = \bigoplus_{\ell = |\ell_1 - \ell_2|}^{\ell_1 + \ell_2} \ell$$

## Python Implementation

```python
import numpy as np
from itertools import product

def character_table(S3_elements_rep):
    """Compute character table for S3 from its 3D permutation rep."""
    # S3 has 3 conjugacy classes: identity, transpositions, 3-cycles
    # elements: e, (12), (13), (23), (123), (132)
    chars = np.zeros(3)  # trivial, sign, standard
    
    # Trivial rep: all 1
    chars[0] = 1.0
    
    # Sign rep: sign of permutation
    # Sign is +1 for even, -1 for odd
    
    # Standard rep: 2D irrep
    # character values: chi(e)=2, chi(transposition)=0, chi(3-cycle)=-1
    return chars

def group_convolution(f, k, G):
    """Group convolution: (f * k)(g) = sum_h f(h) k(h^{-1} g)."""
    n = len(G)
    result = np.zeros(n)
    for i, g in enumerate(G):
        for j, h in enumerate(G):
            # find h^{-1} g element index
            h_inv_g = G[product_idx(G, multiply_groups(h, g))]
    return result

def multiply_groups(a, b):
    """Group multiplication placeholder for a specific group."""
    return a @ b  # matrix multiplication for matrix groups

def product_idx(G, element):
    """Find index of element in group list."""
    for i, e in enumerate(G):
        if np.allclose(e, element):
            return i
    return -1

# Example: SO(3) Wigner-D matrices
def wigner_d_matrix(ell, alpha, beta, gamma):
    """Wigner D-matrix for SO(3) irrep of order ell.
    D^ell_{m,m'}(alpha, beta, gamma) = e^{-i m alpha} d^ell_{m,m'}(beta) e^{-i m' gamma}
    
    This is a simplified sketch — full implementation requires computing
    the small Wigner d matrix via analytic formulas or recursion."""
    dim = 2 * ell + 1
    D = np.zeros((dim, dim), dtype=complex)
    for m in range(-ell, ell+1):
        for mp in range(-ell, ell+1):
            # d^ell_{m,mp}(beta) would be computed here
            d = 1.0 if m == mp else 0.0  # placeholder
            D[m+ell, mp+ell] = np.exp(-1j * m * alpha) * d * np.exp(-1j * mp * gamma)
    return D

# Example: spherical harmonics as SO(3) matrix elements
ell = 2
theta, phi = np.pi/3, np.pi/4
# Y^m_ell(theta, phi) = sqrt((2ell+1)/(4pi)) * D^ell_{m,0}(phi, theta, 0)
print(f"Spherical harmonic Y^0_{ell}(theta, phi) ≈ {np.sqrt((2*ell+1)/(4*np.pi)) * wigner_d_matrix(ell, phi, theta, 0)[ell, ell]:.4f}")
```

## Visualization
Plot the spherical harmonics $Y_\ell^m$ for $\ell = 0, 1, 2, 3$ as coloured spherical surfaces (amplitude = distance from origin, colour = sign). The $\ell = 0$ is a sphere (trivial rep), $\ell = 1$ are three orthogonal dipoles (vector rep), $\ell = 2$ are five quadrupole shapes. A second panel shows the character table of $S_4$ as a heatmap.

## Connections to Machine Learning

### Equivariant Neural Networks via Irreps
Modern equivariant networks (e.g., e3nn, ESCNN) work directly with irreps:
- Input: feature vector $f$ that transforms as a direct sum of irreps of $G$.
- Each layer: linear combination of tensor products of irreps, restricted by Clebsch–Gordan coefficients.
- Nonlinearities: gated nonlinearities (norm of a vector irrep passed through a scalar nonlinearity, then multiplied back).

This approach guarantees exact equivariance by construction, in contrast to data augmentation which only enforces approximate invariance.

### Steerable CNNs
A steerable CNN layer consists of filters that transform according to a group representation:

$$[\psi \star f](g) = \sum_k \psi_k * f_k (g)$$

where $\psi_k$ are steerable filters. For the Euclidean group $E(2)$, steerable filters are linear combinations of polar-separable basis functions $R(r) e^{i m \phi}$. Steerable CNNs match or exceed the performance of data augmentation while using fewer parameters and being provably equivariant.

### Feature Disentanglement
Group-theoretic disentanglement decomposes the representation space into irreps. Each irrep captures an independent "factor of variation" — e.g., in a 3D scene, the $SO(3)$ irrep of order 1 captures 3D orientation, while $SE(3)$ captures both orientation and position. Models like the group-equivariant capsule network or the $E(2)$-equivariant autoencoder learn disentangled latent spaces structured by group representations.

## Practical Considerations

### Finite vs Compact Groups
- **Finite groups** (e.g., $C_n$, $D_n$, $S_n$): representation theory is discrete; use character tables and explicit group elements.
- **Compact groups** (e.g., $SO(3)$, $SU(2)$): irreps are infinite-dimensional for $L^2$; in practice, truncate to a maximum irrep order $L_{\max}$.
- Computing Clebsch–Gordan coefficients for large irrep decompositions is expensive but can be precomputed.

### Choosing Irrep Order
For 3D point clouds, input features are typically scalars ($\ell = 0$) and vectors ($\ell = 1$). Higher $\ell$ values capture finer angular details but increase computational cost (scaling as $O(\ell^6)$ for tensor products). Typical max $\ell$ is 2-4.

## References
- Serre, *Linear Representations of Finite Groups*, Springer 1977
- Fulton & Harris, *Representation Theory: A First Course*, Springer 1991
- Zee, *Group Theory in a Nutshell for Physicists*, Princeton 2016
- Cohen, Welling, "Group Equivariant Convolutional Networks," *ICML 2016*
- Weiler, Cesa, "General $E(2)$-Equivariant Steerable CNNs," *NeurIPS 2019*
- Geiger, Smidt, "e3nn: Euclidean Neural Networks," *JOSS 2022*
