# Phase 01: Linear Algebra — Practice Exercises

Mix of theoretical questions and coding exercises covering the full phase.

---

## Exercise 1: Vector Geometry

**Theoretical**: Prove that for any vectors **a**, **b** ∈ ℝ³:
- (**a** × **b**) · **a** = 0
- (**a** × **b**) · **b** = 0

**Coding**: Implement a function that verifies these properties numerically for 100 random vector pairs.

**Hint**: Use `np.cross` and `np.dot`.

---

## Exercise 2: Gram–Schmidt vs Modified Gram–Schmidt

**Theoretical**: Why is Modified Gram–Schmidt more numerically stable than Classical Gram–Schmidt?

**Coding**: Generate a 20×20 matrix with condition number 10¹². Compare the orthogonality error ||QᵀQ − I|| for CGS and MGS.

**Hint**: Use `np.linalg.svd` to create a matrix with controlled condition number by setting singular values.

---

## Exercise 3: LU Stability

**Coding**: Implement Gaussian elimination without pivoting and with partial pivoting. Solve a Hilbert matrix (H[i,j] = 1/(i+j+1)) of size 10×10. Compare the forward error for both methods.

**Hint**: `from scipy.linalg import hilbert`

---

## Exercise 4: Matrix Multiplication Analysis

**Theoretical**: What is the cache complexity of the naive O(n³) algorithm vs a tiled algorithm with tile size b?

**Coding**: Benchmark naive, ikj-loop-order, tiled (b=32), and BLAS matrix multiplication for n = 32, 64, 128, 256, 512. Plot log-log of time vs n. What are the slopes?

**Hint**: Use `time.perf_counter()` and `matplotlib`.

---

## Exercise 5: Least Squares via QR vs Normal Equations

**Theoretical**: Why is solving A**x** ≈ **b** via QR preferred over the normal equations AᵀA**x** = Aᵀ**b** when A is ill-conditioned?

**Coding**: Construct A with cond(A) = 10¹⁰. Compare the residual norms from QR vs normal equations.

**Hint**: The normal equations square the condition number: cond(AᵀA) = cond(A)².

---

## Exercise 6: SVD Compression

**Coding**: Write a function that takes an image (as a 2D numpy array) and compresses it using truncated SVD. For each compression level k = 1, 5, 10, 25, 50, compute:
- Storage ratio: k(m+n) / (mn)
- Relative reconstruction error: ||A − Aₖ||_F / ||A||_F

Plot error vs storage ratio. At what k do you achieve 10× compression with less than 5% error?

**Hint**: Use `plt.imshow` with `cmap='gray'` to visualize.

---

## Exercise 7: Power Iteration vs QR Algorithm

**Coding**: Implement power iteration to find the dominant eigenvalue of a 100×100 symmetric matrix. Compare the number of iterations needed when the eigenvalue gap (λ₁ − λ₂) is 0.1 vs 1.0 vs 10.0.

**Theoretical**: How does the convergence rate of power iteration depend on |λ₂/λ₁|?

**Hint**: You can control the eigenvalue gap by constructing A = Q diag(λ) Qᵀ with chosen eigenvalues.

---

## Exercise 8: Spectral Clustering

**Coding**: Generate two interleaving half-moons using `sklearn.datasets.make_moons`. Apply:
1. K-means clustering
2. Spectral clustering with RBF kernel

Compare the clustering accuracy (adjusted Rand index). Explain why spectral clustering succeeds where k-means fails.

**Hint**: For spectral clustering, build the similarity matrix using `exp(-||x_i - x_j||² / (2σ²))`.

---

## Exercise 9: NMF vs SVD for Topic Modeling

**Coding**: Create a term-document matrix with 100 documents, 500 terms, and 5 topics. Each document is a mixture of topics, and each topic has a distribution over terms (both nonnegative).

Apply both NMF and truncated SVD to recover topics with k=5. Compare:
- Non-negativity of recovered factors
- Interpretability (do the NMF topics match the ground truth topics?)
- Reconstruction error

**Hint**: Use the multiplicative update NMF from lesson 14. Generate ground truth factors W_true, H_true and form V = W_true @ H_true.

---

## Exercise 10: Tensor Completion

**Coding**: Create a 10×8×6 tensor with CP rank 3. Remove 70% of the entries randomly. Use CP-ALS to complete the tensor. Compare the completion accuracy with matrix completion (flattening the tensor to 10×48).

Plot the convergence of both methods. Under what conditions does the tensor method significantly outperform the matrix method?

**Hint**: Flatten the tensor by merging the last two modes. Use the CP-ALS implementation from lesson 15 or 24.

---

## Exercise 11: Condition Number and Perturbation

**Theoretical**: Prove that for solving A**x** = **b**, the relative error in **x** is bounded by κ(A) times the relative perturbation in the data.

**Coding**: For a 10×10 matrix with condition number 10⁶, add random perturbations of size ε = 10⁻¹², 10⁻¹⁰, 10⁻⁸, 10⁻⁶, 10⁻⁴ to A and b. Plot log-log of forward error vs ε. Is the slope approximately 1? Where does the bound κ(A)·ε become tight?

---

## Exercise 12: Random Matrix Phase Transition

**Coding**: Generate a spiked covariance model with n = 500, p = 200, rank-1 signal with strength ρ varying from 0 to 3. For each ρ, compute the largest eigenvalue of the sample covariance matrix. Plot the eigenvalue vs ρ.

**Theoretical**: At what value of ρ does the top eigenvalue separate from the bulk predicted by the Marchenko–Pastur law? Compute the theoretical threshold 1/√(p/n).

**Hint**: See lesson 16 for the spiked covariance implementation.
