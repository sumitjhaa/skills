#!/usr/bin/env python3
"""03.37 Bayesian Nonparametrics: Dirichlet Process via Stick-Breaking."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

def stick_break(alpha, K):
    beta = np.random.beta(1, alpha, K)
    pi = np.zeros(K)
    pi[0] = beta[0]
    prod = 1 - beta[0]
    for k in range(1, K):
        pi[k] = beta[k] * prod
        prod *= 1 - beta[k]
    return pi

def effective_atoms(pi, threshold=0.01):
    return int(np.sum(pi > threshold))

def crp_customers(alpha, N):
    """Chinese Restaurant Process: seating N customers."""
    tables = []
    for i in range(N):
        if len(tables) == 0:
            tables.append(1)
        else:
            probs = tables + [alpha]
            probs = np.array(probs) / (i + alpha)
            k = np.random.choice(len(probs), p=probs)
            if k == len(tables):
                tables.append(1)
            else:
                tables[k] += 1
    return tables

def posterior_dp(alpha_prior, prior_mean, n, sum_x):
    """Conjugate DP: Normal-Normal posterior."""
    alpha_post = alpha_prior + n
    mean_post = (alpha_prior * prior_mean + sum_x) / alpha_post
    return alpha_post, mean_post

if __name__ == "__main__":
    print("=== Dirichlet Process: Stick-Breaking Construction ===\n")

    alpha_values = [0.5, 1.0, 5.0, 20.0]
    K = 50

    fig, axes = plt.subplots(2, 3, figsize=(14, 10))
    axes_flat = axes.ravel()

    for idx, alpha in enumerate(alpha_values):
        # Single realization
        pi = stick_break(alpha, K)
        axes_flat[idx].stem(range(1, K + 1), pi, basefmt=" ", linefmt=f"C{idx}-", markerfmt=f"C{idx}o")
        axes_flat[idx].set_ylim(0, max(pi) * 1.2 + 0.05)
        axes_flat[idx].set_xlabel("Atom index k")
        axes_flat[idx].set_ylabel("π_k")
        axes_flat[idx].set_title(f"α = {alpha}")

        theta = np.random.normal(0, 1, K)
        G = np.sum(pi * theta)
        eff = effective_atoms(pi)
        axes_flat[idx].text(0.95, 0.95, f"E[G]={G:.2f}\natoms>{eff}",
                            transform=axes_flat[idx].transAxes, va='top', ha='right', fontsize=9)
        axes_flat[idx].grid(True, axis='y')

    # Multiple realizations: distribution of effective atoms
    n_trials = 500
    ax_hist = axes_flat[4]
    for alpha in [0.5, 1.0, 5.0, 20.0]:
        effs = []
        for _ in range(n_trials):
            pi = stick_break(alpha, K)
            effs.append(effective_atoms(pi))
        ax_hist.hist(effs, bins=20, alpha=0.4, label=f"α={alpha}", density=True)
    ax_hist.set_xlabel("Effective atoms (>0.01)")
    ax_hist.set_ylabel("Density")
    ax_hist.set_title(f"Distribution of Effective Atoms (n={n_trials})")
    ax_hist.legend()
    ax_hist.grid(True, axis='y')

    # CRP seating chart
    ax_crp = axes_flat[5]
    for alpha, color in zip([0.5, 1.0, 5.0], ['C0', 'C1', 'C2']):
        tables = crp_customers(alpha, 100)
        ax_crp.plot(range(1, len(tables) + 1), tables, 'o-', alpha=0.7, label=f"α={alpha}", color=color)
    ax_crp.set_xlabel("Table index")
    ax_crp.set_ylabel("Customers seated")
    ax_crp.set_title("Chinese Restaurant Process (N=100)")
    ax_crp.legend()
    ax_crp.grid(True, axis='y')

    plt.suptitle("Dirichlet Process: Stick-Breaking Weights & CRP", fontsize=14)
    plt.tight_layout()
    plt.savefig("../../assets/phase03/37-bayesian-nonparametrics.png")
    plt.close()

    # Print analysis
    print("Stick-breaking weight statistics:")
    for alpha in alpha_values:
        all_pi = np.array([stick_break(alpha, K) for _ in range(200)])
        mean_eff = np.mean([effective_atoms(pi) for pi in all_pi])
        print(f"  α={alpha:5.1f}: mean effective atoms = {mean_eff:.1f} / {K}")

    print("\nDP posterior inference (conjugate Normal-Normal):")
    np.random.seed(123)
    true_mean = 2.5
    data = np.random.normal(true_mean, 1, 20)
    alpha_prior, prior_mean = 1.0, 0.0
    post_alpha, post_mean = posterior_dp(alpha_prior, prior_mean, len(data), data.sum())
    print(f"  Data: n={len(data)}, mean={data.mean():.2f}")
    print(f"  Prior: α={alpha_prior}, mean={prior_mean}")
    print(f"  Posterior: α={post_alpha:.1f}, mean={post_mean:.2f}")
    print(f"  Posterior predictive: N({post_mean:.2f}, 1 + 1/{post_alpha:.1f})")

    print("\nCRP simulation (N=100):")
    for alpha in [0.5, 1.0, 5.0]:
        tables = crp_customers(alpha, 100)
        print(f"  α={alpha}: {len(tables)} tables, "
              f"largest={max(tables)}, "
              f"table size distribution: {sorted(tables, reverse=True)[:5]}")
