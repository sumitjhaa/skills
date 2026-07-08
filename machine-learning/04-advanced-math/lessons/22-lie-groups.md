# 04.22 Lie Groups and Lie Algebras

## Motivation
Lie groups describe continuous symmetries. In ML, they appear in equivariant neural networks, pose estimation, robotics (rotation groups), and normalising flows built on matrix groups. Understanding the Lie group / Lie algebra correspondence enables building models that are provably invariant or equivariant to rotations, translations, and other continuous transformations.

## Learning Objectives
- Define Lie groups and Lie algebras and understand their relationship via the exponential map.
- Compute the matrix exponential and logarithm for $SO(3)$ and $SE(3)$.
- Understand group actions and equivariance.
- Apply Lie group theory to equivariant neural networks and normalising flows.

## Math Foundation

### Lie Groups
A Lie group $G$ is a smooth manifold that is also a group, where multiplication $m: G \times G \to G$ and inversion $i: G \to G$ are smooth maps.

**Examples**:
- **General linear group** $GL(n, \mathbb{R})$: invertible $n \times n$ real matrices.
- **Special orthogonal group** $SO(n)$: rotation matrices: $R^\top R = I$, $\det R = 1$.
- **Special Euclidean group** $SE(3)$: rigid body motions: $(R, t)$ with $R \in SO(3)$, $t \in \mathbb{R}^3$.
- **Unitary group** $U(n)$: matrices with $U^\dagger U = I$.
- **Lorentz group** $O(1,3)$: symmetries of Minkowski spacetime.

### Lie Algebras
The Lie algebra $\mathfrak{g} = T_e G$ is the tangent space at the identity, equipped with a Lie bracket $[\cdot, \cdot]: \mathfrak{g} \times \mathfrak{g} \to \mathfrak{g}$ that is bilinear, alternating ($[X,X] = 0$), and satisfies the Jacobi identity:

$$[X, [Y, Z]] + [Y, [Z, X]] + [Z, [X, Y]] = 0$$

For matrix groups, the Lie bracket is the matrix commutator $[X, Y] = XY - YX$.

### Examples of Lie Algebras
| Group | Lie Algebra | Description |
|-------|------------|-------------|
| $GL(n)$ | $\mathfrak{gl}(n)$ | All $n \times n$ matrices |
| $SO(n)$ | $\mathfrak{so}(n)$ | Skew-symmetric matrices $X^\top = -X$ |
| $SE(3)$ | $\mathfrak{se}(3)$ | Twists: $(\omega, v)$ with $\omega \in \mathfrak{so}(3)$ |
| $U(n)$ | $\mathfrak{u}(n)$ | Skew-Hermitian matrices $X^\dagger = -X$ |

### Exponential and Logarithm Maps
The matrix exponential maps $\mathfrak{g} \to G$:

$$\exp(X) = \sum_{k=0}^\infty \frac{X^k}{k!}$$

For $SO(3)$, the exponential of a skew-symmetric matrix $[\omega]_\times$ gives a rotation by angle $\|\omega\|$ around axis $\omega/\|\omega\|$ (Rodrigues' formula):

$$\exp([\omega]_\times) = I + \frac{\sin\theta}{\theta} [\omega]_\times + \frac{1 - \cos\theta}{\theta^2} [\omega]_\times^2$$

where $\theta = \|\omega\|$. The logarithm inverts this.

### Baker–Campbell–Hausdorff Formula
For $X, Y \in \mathfrak{g}$ with sufficiently small norms:

$$\log(\exp X \exp Y) = X + Y + \frac12 [X, Y] + \frac{1}{12} ([X, [X, Y]] - [Y, [X, Y]]) + \cdots$$

This is essential for composing transformations in Lie group coordinates.

### Group Actions and Equivariance
A group action of $G$ on a set $M$ is a map $\cdot: G \times M \to M$ satisfying $g \cdot (h \cdot x) = (gh) \cdot x$ and $e \cdot x = x$. A function $f: M \to N$ is equivariant if:

$$f(g \cdot x) = g \cdot f(x) \quad \forall g \in G, x \in M$$

and invariant if $f(g \cdot x) = f(x)$.

## Python Implementation

```python
import numpy as np

def skew_symmetric(v):
    """Convert 3-vector to skew-symmetric matrix."""
    return np.array([[0, -v[2], v[1]],
                     [v[2], 0, -v[0]],
                     [-v[1], v[0], 0]])

def so3_exp(omega):
    """Rodrigues' formula: exponential from so(3) to SO(3)."""
    theta = np.linalg.norm(omega)
    if theta < 1e-10:
        return np.eye(3)
    K = skew_symmetric(omega / theta)
    return np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)

def so3_log(R):
    """Logarithm from SO(3) to so(3)."""
    theta = np.arccos(np.clip((np.trace(R) - 1) / 2, -1.0, 1.0))
    if theta < 1e-10:
        return np.zeros(3)
    w = np.array([R[2,1] - R[1,2], R[0,2] - R[2,0], R[1,0] - R[0,1]])
    return w * (theta / (2 * np.sin(theta)))

def se3_action(T, points):
    """Apply SE(3) transformation (R, t) to a set of 3D points."""
    R, t = T
    return (R @ points.T).T + t

def lie_bracket(X, Y):
    """Matrix Lie bracket: [X, Y] = XY - YX."""
    return X @ Y - Y @ X

# Example: compose rotations
theta1 = np.array([0.3, 0.0, 0.0])
theta2 = np.array([0.0, 0.4, 0.0])
R1 = so3_exp(theta1)
R2 = so3_exp(theta2)
R_combined = R1 @ R2
theta_combined = so3_log(R_combined)
print(f"Composed rotation (BCH approx): {theta_combined}")
print(f"BCH 1st order: {theta1 + theta2 + 0.5 * lie_bracket(skew_symmetric(theta1), skew_symmetric(theta2))[0]}")

# SE(3) example: apply transformation to points
points = np.random.randn(10, 3)
R = so3_exp(np.array([0.2, -0.3, 0.1]))
t = np.array([1.0, 0.5, -0.3])
transformed = se3_action((R, t), points)
print(f"Input shape: {points.shape}, Output shape: {transformed.shape}")
```

## Visualization
Plot a 3D bunny mesh (Stanford Bunny) and apply $SO(3)$ rotations at different angles — the mesh rotates rigidly. A second panel shows the Lie algebra $\mathfrak{so}(3)$ as a 3D vector space, with the exponential map projecting each vector to a rotation matrix, visualised as a sphere of radius $\pi$ (since $\|\omega\| \le \pi$ covers all rotations).

## Connections to Machine Learning

### SE(3)-Equivariant Neural Networks
Equivariant networks for 3D point clouds and molecules use representations of $SE(3)$:
- **Tensor field networks** (Thomas et al. 2018): convolution kernels are radial functions multiplied by spherical harmonics, ensuring $SO(3)$ equivariance.
- **SE(3)-Transformers** (Fuchs et al. 2020): attention mechanism where query-key interactions depend on $SE(3)$-invariant distances, and value aggregation uses equivariant weights.
- **EGNN** (Satorras et al. 2021): equivariant message passing using relative positions and scalar features — no spherical harmonics needed.

These architectures are widely used for molecular property prediction, protein structure prediction, and robotics manipulation.

### Normalising Flows on Lie Groups
Flows on $SO(3)$ build flexible distributions over orientations:
- **Continuous normalising flow**: $h_1 = h_0 + \int_0^1 f_\theta(h_t, t) dt$ where the vector field lives in the Lie algebra.
- **Geodesic flow**: transform samples along geodesics on the Lie group.
- Applications: pose estimation, robotics grasping, and molecular conformation generation.

### Robotic Kinematics
A robot arm's configuration space is the Lie group $SE(3)^n$ (one copy per joint). Forward kinematics maps joint angles to end-effector pose. The Jacobian maps joint velocities $\dot{\theta}$ to end-effector twists $\xi = J(\theta) \dot{\theta}$ (elements of $\mathfrak{se}(3)$). Inverse kinematics solves for joint angles achieving a desired pose — nonlinear optimisation on the product Lie group.

## Practical Considerations

### Numerical Issues
- The matrix exponential suffers from overflow for large $\|X\|$. Use the scaling-and-squaring method.
- For $SO(3)$, the log map is singular at $\theta = \pi$ (180-degree rotations). Use quaternions for robust interpolation.
- The BCH formula converges only for nearby elements; for distant elements, compose in the group and then log.

### Quaternions vs Rotation Matrices
Quaternions represent rotations with 4 parameters (avoiding 3D singularities) and compose via Hamilton product. They are more efficient than $3\times 3$ matrices for composition but must be unit-normalised. For gradients, the $SO(3)$ exponential map on $\mathbb{R}^3$ is preferred in ML because it is unconstrained.

## References
- Hall, *Lie Groups, Lie Algebras, and Representations*, 2nd ed., Springer 2015
- Stillwell, *Naive Lie Theory*, Springer 2008
- Murray, Li, Sastry, *A Mathematical Introduction to Robotic Manipulation*, CRC 1994
- Thomas et al., "Tensor Field Networks: Rotation- and Translation-Equivariant Neural Networks for 3D Point Clouds," *arXiv:1802.08219*, 2018
- Satorras, Hoogeboom, Welling, "E(n) Equivariant Graph Neural Networks," *ICML 2021*
