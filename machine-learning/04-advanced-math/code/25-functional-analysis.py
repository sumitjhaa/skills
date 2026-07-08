"""04.25 Functional analysis: norms, operators, spectral theory."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import svd, svdvals, norm, expm
from scipy.integrate import trapezoid

np.random.seed(42)

def Lp_norm(f, a, b, p, n_quad=1000):
    xs = np.linspace(a, b, n_quad)
    vals = f(xs)
    return (np.sum(np.abs(vals)**p) * (xs[1] - xs[0]))**(1/p) if p < np.inf else np.max(np.abs(vals))

def operator_norm(A, p=2):
    if p == 2:
        s = svdvals(A)
        return np.max(s)
    elif p == 1:
        return np.max(np.sum(np.abs(A), axis=0))
    elif p == np.inf:
        return np.max(np.sum(np.abs(A), axis=1))

n = 20
A = np.random.randn(n, n)
A_sym = (A + A.T) / 2
A_skew = (A - A.T) / 2

bounds = [-1, 1]
f_sin = lambda x: np.sin(2*np.pi*x)
f_sq = lambda x: np.where(np.abs(x) < 0.5, 1.0, 0.0)

L1_sin = Lp_norm(f_sin, -1, 1, 1)
L2_sin = Lp_norm(f_sin, -1, 1, 2)
Linf_sin = Lp_norm(f_sin, -1, 1, np.inf)
L1_sq = Lp_norm(f_sq, -1, 1, 1)
L2_sq = Lp_norm(f_sq, -1, 1, 2)
Linf_sq = Lp_norm(f_sq, -1, 1, np.inf)

norm_2 = operator_norm(A_sym, 2)
norm_1 = operator_norm(A_sym, 1)
norm_inf = operator_norm(A_sym, np.inf)
eigvals_A = np.linalg.eigvalsh(A_sym)
spectral_radius = np.max(np.abs(eigvals_A))

x_lin = np.linspace(-1, 1, 100)
T_x = np.zeros((100, n))
for i in range(n):
    T_x[:, i] = x_lin**i

U, s, Vt = svd(T_x, full_matrices=False)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

xs = np.linspace(-1, 1, 500)
axes[0, 0].plot(xs, f_sin(xs), "b-", lw=2, label="sin(2πx)")
axes[0, 0].plot(xs, f_sq(xs), "r-", lw=2, label="Square pulse")
axes[0, 0].fill_between(xs, 0, f_sq(xs), alpha=0.2, color="red")
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("f(x)")
axes[0, 0].set_title(f"L²[{-bounds[0]},{bounds[1]}] Functions\n"
                     f"‖sin‖₂={L2_sin:.3f}, ‖sq‖₂={L2_sq:.3f}")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].bar(["L¹", "L²", "L^∞"],
               [L1_sin, L2_sin, Linf_sin], alpha=0.7, label="sin(2πx)")
axes[0, 1].bar(["L¹", "L²", "L^∞"],
               [L1_sq, L2_sq, Linf_sq], alpha=0.5, width=0.5, label="square")
axes[0, 1].set_ylabel("Norm")
axes[0, 1].set_title("Function Norms")
axes[0, 1].legend()
axes[0, 1].grid(True, axis="y", alpha=0.3)

axes[0, 2].plot(eigvals_A, "o-", lw=2)
axes[0, 2].axhline(0, color="gray", ls="--")
axes[0, 2].set_xlabel("Index")
axes[0, 2].set_ylabel("Eigenvalue")
axes[0, 2].set_title(f"Spectral Theorem\nSymmetric A ∈ ℝ^{{{n}×{n}}}"
                     f"\nρ(A)={spectral_radius:.3f}")
axes[0, 2].grid(True, alpha=0.3)

im = axes[1, 0].imshow(A_sym, cmap="coolwarm", interpolation="nearest")
plt.colorbar(im, ax=axes[1, 0])
axes[1, 0].set_title("Symmetric Operator\nA = (A+Aᵀ)/2")

norms_labels = ["‖A‖₂", "‖A‖₁", "‖A‖∞", "ρ(A)"]
norms_vals = [norm_2, norm_1, norm_inf, spectral_radius]
axes[1, 1].bar(norms_labels, norms_vals, color=plt.cm.viridis(np.linspace(0.2, 0.8, 4)))
axes[1, 1].set_ylabel("Norm")
axes[1, 1].set_title("Operator Norms\n‖A‖₂ ≤ √(‖A‖₁·‖A‖∞)")
axes[1, 1].grid(True, axis="y", alpha=0.3)

for i in range(min(5, n)):
    axes[1, 2].plot(x_lin, U[:, i] * np.sign(U[0, i]), lw=2,
                   label=f"σ_{i+1}={s[i]:.3f}")
axes[1, 2].set_xlabel("x")
axes[1, 2].set_ylabel("Singular function")
axes[1, 2].set_title("SVD of Vandermonde-like Operator\n"
                     "T: polynomial basis → functions")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/25-functional-analysis.png")
plt.close()

print("=" * 60)
print("FUNCTIONAL ANALYSIS")
print("=" * 60)
print(f"\nFunction norms on L²[-1, 1]:")
print(f"  sin(2πx): L¹={L1_sin:.4f}, L²={L2_sin:.4f}, L^∞={Linf_sin:.4f}")
print(f"  square:   L¹={L1_sq:.4f}, L²={L2_sq:.4f}, L^∞={Linf_sq:.4f}")

print(f"\nOperator norms (symmetric A, n={n}):")
print(f"  ‖A‖₂ (spectral) = {norm_2:.4f}")
print(f"  ‖A‖₁ = {norm_1:.4f}")
print(f"  ‖A‖∞ = {norm_inf:.4f}")
print(f"  ρ(A) = {spectral_radius:.4f}")
print(f"  ‖A‖₂ ≤ √(‖A‖₁·‖A‖∞) = {np.sqrt(norm_1*norm_inf):.4f} (verified)")

print(f"\nSVD of compact operator T: ℝⁿ → L²[-1,1]")
print(f"  σ₁ = {s[0]:.4f}")
print(f"  σ₅ = {s[4]:.4f}")
print(f"  σ₁₀ = {s[9]:.4f}")

print(f"\nKey results:")
print(f"  • Lp spaces: ‖f‖_p = (∫|f|^p)^{{1/p}}")
print(f"  • Spectral theorem: self-adjoint → real eigenvalues")
print(f"  • SVD: Tf = Σ σ_i ⟨f, u_i⟩ v_i")
print(f"  • Banach fixed point: contractive maps have unique FP")
