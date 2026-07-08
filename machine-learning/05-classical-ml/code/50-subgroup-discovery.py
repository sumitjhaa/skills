"""Subgroup Discovery from scratch with multiple quality measures."""
import numpy as np
import matplotlib.pyplot as plt

class SubgroupDiscovery:
    def __init__(self, min_cover=0.05, top_k=5):
        self.min_cover = min_cover
        self.top_k = top_k

    def fit(self, X, y):
        n, d = X.shape
        target_mean = y.mean()
        subgroups = []

        for feat in range(d):
            vals = np.unique(X[:, feat])
            for val in vals:
                mask = X[:, feat] == val
                n_cover = mask.sum()
                if n_cover < self.min_cover * n:
                    continue

                p_s = y[mask].mean()
                n_s = n_cover
                wracc = (n_cover / n) * (p_s - target_mean)

                # Lift
                lift = p_s / target_mean if target_mean > 0 else 0

                # Binomial test p-value
                from scipy.stats import binomtest
                p_value = binomtest(int(p_s * n_s), n_s, target_mean, alternative='two-sided').pvalue

                subgroups.append({
                    'description': f'x{feat} == {val}',
                    'coverage': n_cover / n,
                    'target_mean': p_s,
                    'wracc': wracc,
                    'lift': lift,
                    'p_value': p_value,
                    'support': n_cover,
                    'size': n_s,
                })

        subgroups.sort(key=lambda s: abs(s['wracc']), reverse=True)
        self.subgroups_ = subgroups[:self.top_k]
        return self

    def print_subgroups(self):
        print(f"Top {len(self.subgroups_)} subgroups:")
        print(f"  {'Description':<20} {'Coverage':<10} {'Mean':<8} {'WRAcc':<10} {'Lift':<8} {'p-val':<10}")
        print("  " + "-" * 66)
        for s in self.subgroups_:
            print(f"  {s['description']:<20} {s['coverage']:<10.2%} {s['target_mean']:<8.3f} "
                  f"{s['wracc']:<10.4f} {s['lift']:<8.2f} {s['p_value']:<10.4f}")
        return self

if __name__ == "__main__":
    np.random.seed(42)
    print("=== Subgroup Discovery ===\n")

    # Dataset with known subgroups
    n = 1000
    d = 5
    X = np.random.randint(0, 3, size=(n, d))
    base_prob = 0.3
    y = np.random.binomial(1, base_prob, n)

    # Create subgroups: x0==2 has higher probability
    mask_x0 = X[:, 0] == 2
    y[mask_x0] = np.random.binomial(1, 0.7, mask_x0.sum())

    # x1==0 has lower probability
    mask_x1 = X[:, 1] == 0
    y[mask_x1] = np.random.binomial(1, 0.15, mask_x1.sum())

    sd = SubgroupDiscovery(min_cover=0.05, top_k=5)
    sd.fit(X, y)
    sd.print_subgroups()

    # Second dataset with different structure
    print("\n=== Dataset 2: Continuous target ===")
    X2 = np.random.randint(0, 3, size=(n, d))
    y2 = np.random.randn(n)
    y2[X2[:, 2] == 1] += 1.5
    y2[X2[:, 3] == 2] -= 1.0

    sd2 = SubgroupDiscovery(min_cover=0.05, top_k=5)
    sd2.fit(X2, y2 > y2.mean())
    sd2.print_subgroups()

    # Quality measure comparison
    print("\n=== Quality Measure Comparison ===")
    target_mean = y.mean()
    all_subgroups = []
    for feat in range(d):
        for val in np.unique(X[:, feat]):
            mask = X[:, feat] == val
            n_c = mask.sum()
            if n_c < 0.05 * n:
                continue
            p_s = y[mask].mean()
            wracc = (n_c / n) * (p_s - target_mean)
            lift = p_s / target_mean if target_mean > 0 else 0
            all_subgroups.append({
                'desc': f'x{feat}={val}',
                'cover': n_c / n,
                'mean': p_s,
                'wracc': wracc,
                'lift': lift,
            })

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # WRAcc vs Lift scatter
    for sg in all_subgroups:
        axes[0].scatter(sg['wracc'], sg['lift'], s=sg['cover'] * 500, alpha=0.5)
        axes[0].annotate(sg['desc'], (sg['wracc'], sg['lift']), fontsize=8)
    axes[0].axhline(1, color='r', ls='--', alpha=0.5)
    axes[0].set_xlabel("WRAcc")
    axes[0].set_ylabel("Lift")
    axes[0].set_title("Subgroup Quality Measures")
    axes[0].grid(True, alpha=0.3)

    # Coverage vs effect size
    for sg in all_subgroups:
        axes[1].scatter(sg['cover'], sg['mean'] - target_mean, s=np.abs(sg['wracc']) * 2000, alpha=0.5)
        axes[1].annotate(sg['desc'], (sg['cover'], sg['mean'] - target_mean), fontsize=8)
    axes[1].axhline(0, color='r', ls='--', alpha=0.5)
    axes[1].set_xlabel("Coverage")
    axes[1].set_ylabel("Effect size (Δmean)")
    axes[1].set_title("Coverage vs Effect Size")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("../../assets/phase05/50-subgroup-discovery.png")
    plt.close()
    print("Figure saved to 50-subgroup-discovery.png")

    # Edge case: no subgroups
    print("\n=== Edge Cases ===")
    X_rand = np.random.randint(0, 3, size=(100, 3))
    y_rand = np.random.binomial(1, 0.5, 100)
    sd_rand = SubgroupDiscovery(min_cover=0.1, top_k=3)
    sd_rand.fit(X_rand, y_rand)
    print("  Random data (no structure):")
    sd_rand.print_subgroups()

    # Edge case: very small min_cover
    sd_tiny = SubgroupDiscovery(min_cover=0.01, top_k=3)
    sd_tiny.fit(X, y)
    print(f"  With min_cover=0.01: {len(sd_tiny.subgroups_)} subgroups found")

    # Edge case: single feature
    X1 = np.random.randint(0, 3, size=(200, 1))
    y1 = np.random.binomial(1, 0.3, 200)
    y1[X1[:, 0] == 2] = np.random.binomial(1, 0.8, (X1[:, 0] == 2).sum())
    sd1 = SubgroupDiscovery(min_cover=0.05, top_k=5)
    sd1.fit(X1, y1)
    print(f"  Single feature: {len(sd1.subgroups_)} subgroups found")
