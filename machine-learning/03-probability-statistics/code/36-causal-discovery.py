#!/usr/bin/env python3
"""03.36 Causal Discovery: PC algorithm skeleton (conditional independence testing)."""
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

np.random.seed(42)

def partial_corr_xyz(a, b, c):
    r_ab = pearsonr(a, b)[0]
    r_ac = pearsonr(a, c)[0]
    r_bc = pearsonr(b, c)[0]
    r_ab_c = (r_ab - r_ac * r_bc) / np.sqrt((1 - r_ac**2) * (1 - r_bc**2) + 1e-10)
    z = np.arctanh(r_ab_c) * np.sqrt(len(a) - 3)
    p = 2 * (1 - 0.5 * (1 + math.erf(np.abs(z) / np.sqrt(2))))
    return r_ab_c, p

def generate_chain(n=1000):
    """X -> Z -> Y"""
    X = np.random.normal(0, 1, n)
    Z = 0.8 * X + np.random.normal(0, 0.5, n)
    Y = 0.7 * Z + np.random.normal(0, 0.3, n)
    return X, Z, Y, "Chain: X → Z → Y"

def generate_fork(n=1000):
    """X <- Z -> Y (confounder)"""
    Z = np.random.normal(0, 1, n)
    X = 0.8 * Z + np.random.normal(0, 0.5, n)
    Y = 0.7 * Z + np.random.normal(0, 0.3, n)
    return X, Z, Y, "Fork: X ← Z → Y"

def generate_collider(n=1000):
    """X -> Z <- Y (collider)"""
    X = np.random.normal(0, 1, n)
    Y = np.random.normal(0, 1, n)
    Z = 0.8 * X + 0.7 * Y + np.random.normal(0, 0.3, n)
    return X, Z, Y, "Collider: X → Z ← Y"

def analyze_dag(X, Z, Y, name):
    print(f"\n--- {name} ---")
    corr_xy, p_xy = pearsonr(X, Y)
    corr_xz, p_xz = pearsonr(X, Z)
    corr_zy, p_zy = pearsonr(Z, Y)
    pc_xy_z, p_xy_z = partial_corr_xyz(X, Y, Z)

    print(f"  Corr(X,Y) = {corr_xy:.3f} (p={p_xy:.4f})")
    print(f"  Corr(X,Z) = {corr_xz:.3f} (p={p_xz:.4f})")
    print(f"  Corr(Z,Y) = {corr_zy:.3f} (p={p_zy:.4f})")
    print(f"  Partial Corr(X,Y|Z) = {pc_xy_z:.3f} (p={p_xy_z:.4f})")

    # PC algorithm interpretations
    marg_dep = p_xy < 0.05
    cond_indep = p_xy_z > 0.05
    if marg_dep and cond_indep:
        print("  ✓ PC: X ⟂ Y | Z  => chain or fork structure")
    elif marg_dep and not cond_indep:
        print("  ✗ PC: X and Y remain dependent given Z => collider?")
    elif not marg_dep:
        print("  ? PC: X and Y marginally independent")

    return corr_xy, p_xy, pc_xy_z, p_xy_z

def draw_dag(ax, name, x_pos=0.1, z_pos=0.5, y_pos=0.9):
    ax.axis('off')
    for label, pos, color in [("X", x_pos, "lightblue"), ("Z", z_pos, "lightgreen"), ("Y", y_pos, "lightcoral")]:
        ax.annotate(label, xy=(pos, 0.5), fontsize=14, ha='center',
                    bbox=dict(boxstyle="round", facecolor=color))
    if "Chain" in name:
        ax.annotate("", xy=(0.35, 0.5), xytext=(0.18, 0.5), arrowprops=dict(arrowstyle="->", lw=2))
        ax.annotate("", xy=(0.65, 0.5), xytext=(0.58, 0.5), arrowprops=dict(arrowstyle="->", lw=2))
    elif "Fork" in name:
        ax.annotate("", xy=(0.35, 0.5), xytext=(0.5, 0.5), arrowprops=dict(arrowstyle="->", lw=2))
        ax.annotate("", xy=(0.65, 0.5), xytext=(0.5, 0.5), arrowprops=dict(arrowstyle="->", lw=2))
    elif "Collider" in name:
        ax.annotate("", xy=(0.5, 0.5), xytext=(0.35, 0.5), arrowprops=dict(arrowstyle="->", lw=2))
        ax.annotate("", xy=(0.5, 0.5), xytext=(0.65, 0.5), arrowprops=dict(arrowstyle="->", lw=2))
    ax.set_title(name)

if __name__ == "__main__":
    generators = [generate_chain, generate_fork, generate_collider]
    all_results = []

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    for idx, gen in enumerate(generators):
        X, Z, Y, name = gen()
        corr_xy, p_xy, pc_xy_z, p_xy_z = analyze_dag(X, Z, Y, name)
        all_results.append((name, corr_xy, p_xy, pc_xy_z, p_xy_z))

        # Scatter plots
        row = idx // 3
        col = idx % 3
        ax1 = axes[row, col]
        ax1.scatter(X, Y, s=5, alpha=0.3, c='blue')
        ax1.set_xlabel("X"); ax1.set_ylabel("Y")
        ax1.set_title(f"{name}\nCorr(X,Y)={corr_xy:.3f}")

        # DAG drawing
        ax2 = axes[row + 1, col] if row == 0 and idx < 3 else None

    # Draw DAGs in the bottom row
    for idx, gen in enumerate(generators):
        _, _, _, name = gen()
        draw_dag(axes[1, idx], name)

    plt.tight_layout()
    plt.savefig("../../assets/phase03/36-causal-discovery.png")
    plt.close()
    print("\nFigure saved to 36-causal-discovery.png")

    # Summary
    print("\n=== Summary ===")
    print(f"{'Structure':<25} {'Corr(X,Y)':<12} {'p-val':<10} {'Partial Corr':<14} {'p-val':<10}")
    print("-" * 75)
    for name, cxy, pxy, pcz, pz in all_results:
        print(f"{name:<25} {cxy:<12.3f} {pxy:<10.4f} {pcz:<14.3f} {pz:<10.4f}")

    # Additional: test with different sample sizes
    print("\n--- Sample Size Robustness ---")
    for n in [50, 200, 1000, 5000]:
        X, Z, Y, name = generate_chain(n)
        _, p_xy = pearsonr(X, Y)
        _, p_xy_z = partial_corr_xyz(X, Y, Z)
        print(f"  n={n:5d}: marginal p={p_xy:.4f}, conditional p={p_xy_z:.4f}")

    # Edge case: deterministic relationships
    print("\n--- Deterministic Edge Case ---")
    n = 200
    X = np.random.normal(0, 1, n)
    Z = X.copy()
    Y = Z.copy()
    r, p = pearsonr(X, Y)
    pc, pp = partial_corr_xyz(X, Y, Z)
    print(f"  Deterministic X=Z=Y: Corr={r:.4f}, p={p:.4f}, Partial={pc:.4f}, p={pp:.4f}")
