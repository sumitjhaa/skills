import numpy as np
import matplotlib.pyplot as plt

def is_pareto_efficient(costs):
    n = len(costs)
    is_efficient = np.ones(n, dtype=bool)
    for i in range(n):
        for j in range(n):
            if i != j and np.all(costs[j] <= costs[i]) and np.any(costs[j] < costs[i]):
                is_efficient[i] = False
                break
    return is_efficient

def nsga2_crowding_distance(front):
    n = len(front)
    m = front.shape[1]
    distance = np.zeros(n)
    for obj in range(m):
        idx = np.argsort(front[:, obj])
        distance[idx[0]] = np.inf
        distance[idx[-1]] = np.inf
        for i in range(1, n - 1):
            if front[idx[-1], obj] != front[idx[0], obj]:
                distance[idx[i]] += (front[idx[i+1], obj] - front[idx[i-1], obj]) / (front[idx[-1], obj] - front[idx[0], obj])
    return distance

def hypervolume_2d(front, ref_point):
    front = front[np.argsort(front[:, 0])]
    hv = 0.0
    prev_x = ref_point[0]
    for i in range(len(front) - 1, -1, -1):
        hv += (prev_x - front[i, 0]) * (ref_point[1] - front[i, 1])
        prev_x = front[i, 0]
    return hv

def main():
    print("=" * 60)
    print("MULTI-OBJECTIVE OPTIMIZATION")
    print("=" * 60)

    print("\n--- Pareto Front Identification ---")
    np.random.seed(42)
    n_points = 50
    costs = np.random.rand(n_points, 2)
    pareto_mask = is_pareto_efficient(costs)
    print(f"  Total points: {n_points}")
    print(f"  Pareto-optimal: {pareto_mask.sum()}")

    print(f"\n--- Weighted Sum Scalarization ---")
    f1 = lambda x: (x[0] - 1)**2 + (x[1] - 2)**2
    f2 = lambda x: (x[0] + 1)**2 + (x[1] - 1)**2

    from scipy.optimize import minimize
    pareto_points = []
    for w1 in np.linspace(0, 1, 11):
        w2 = 1 - w1
        obj = lambda x: w1 * f1(x) + w2 * f2(x)
        res = minimize(obj, x0=[0, 0], method='L-BFGS-B')
        pareto_points.append(res.x)
    pareto_points = np.array(pareto_points)
    pareto_costs = np.array([[f1(p), f2(p)] for p in pareto_points])
    print(f"  Found {len(pareto_points)} Pareto points via weighted sum")

    print(f"\n--- ε-Constraint Method ---")
    eps_points = []
    for eps in np.linspace(0.5, 5, 10):
        cons = {'type': 'ineq', 'fun': lambda x: eps - f2(x)}
        res = minimize(f1, x0=[0, 0], constraints=cons, method='SLSQP')
        if res.success:
            eps_points.append(res.x)
    eps_points = np.array(eps_points)
    print(f"  Found {len(eps_points)} Pareto points via ε-constraint")

    print(f"\n--- Hypervolume Calculation ---")
    ref_point = np.array([6.0, 6.0])
    pareto_optimal = pareto_costs[is_pareto_efficient(pareto_costs)]
    hv = hypervolume_2d(pareto_optimal, ref_point)
    print(f"  Hypervolume (ref={ref_point}): {hv:.4f}")

    all_costs = np.random.rand(100, 2) * 5
    all_pareto = all_costs[is_pareto_efficient(all_costs)]
    hv_random = hypervolume_2d(all_pareto, ref_point)
    print(f"  Hypervolume of random set: {hv_random:.4f}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].scatter(costs[:, 0], costs[:, 1], c='lightblue', alpha=0.5, label='All points')
    axes[0].scatter(costs[pareto_mask, 0], costs[pareto_mask, 1], c='red', s=80, label='Pareto front')
    axes[0].step(sorted(costs[pareto_mask, 0]), sorted(costs[pareto_mask, 1], reverse=True),
                 where='post', color='red', alpha=0.5)
    axes[0].set_xlabel('f₁'); axes[0].set_ylabel('f₂')
    axes[0].set_title('Pareto Front')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    axes[1].scatter(pareto_costs[:, 0], pareto_costs[:, 1], c='blue', s=60, label='Weighted sum')
    if len(eps_points) > 0:
        eps_costs = np.array([[f1(p), f2(p)] for p in eps_points])
        axes[1].scatter(eps_costs[:, 0], eps_costs[:, 1], c='green', s=60, marker='s', label='ε-constraint')
    axes[1].set_xlabel('f₁ = (x-1)² + (y-2)²')
    axes[1].set_ylabel('f₂ = (x+1)² + (y-1)²')
    axes[1].set_title('Pareto Front via Scalarization')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/29_multi_objective.png', dpi=100)
    print(f"\nPlot saved to /tmp/29_multi_objective.png")

if __name__ == "__main__":
    main()
