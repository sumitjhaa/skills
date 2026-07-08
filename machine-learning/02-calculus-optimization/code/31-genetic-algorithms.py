import numpy as np
import matplotlib.pyplot as plt

def tournament_selection(population, fitness, k=3):
    idx = np.random.choice(len(population), k, replace=False)
    best_idx = idx[np.argmin(fitness[idx])]
    return population[best_idx].copy()

def sbx_crossover(p1, p2, eta=15):
    n = len(p1)
    c1, c2 = p1.copy(), p2.copy()
    for i in range(n):
        if np.random.rand() < 0.5:
            u = np.random.rand()
            beta = (2*u)**(1/(eta+1)) if u <= 0.5 else (1/(2*(1-u)))**(1/(eta+1))
            c1[i] = 0.5 * ((1 + beta) * p1[i] + (1 - beta) * p2[i])
            c2[i] = 0.5 * ((1 - beta) * p1[i] + (1 + beta) * p2[i])
    return c1, c2

def polynomial_mutation(y, pm=0.1, eta=20):
    x = y.copy()
    for i in range(len(x)):
        if np.random.rand() < pm:
            u = np.random.rand()
            delta = (2*u)**(1/(eta+1)) - 1 if u < 0.5 else 1 - (2*(1-u))**(1/(eta+1))
            x[i] += delta
    return x

def genetic_algorithm(f, bounds, n_pop=50, n_gen=100, pm=0.1, pc=0.9):
    dim = bounds.shape[0]
    pop = np.random.uniform(bounds[:, 0], bounds[:, 1], (n_pop, dim))
    fitness = np.array([f(ind) for ind in pop])
    best_fit = [fitness.min()]

    for gen in range(n_gen):
        new_pop = []
        while len(new_pop) < n_pop:
            p1 = tournament_selection(pop, fitness)
            p2 = tournament_selection(pop, fitness)
            if np.random.rand() < pc:
                c1, c2 = sbx_crossover(p1, p2)
            else:
                c1, c2 = p1.copy(), p2.copy()
            c1 = polynomial_mutation(c1, pm)
            c2 = polynomial_mutation(c2, pm)
            new_pop.extend([c1, c2])

        pop = np.array(new_pop[:n_pop])
        fitness = np.array([f(ind) for ind in pop])
        best_fit.append(fitness.min())

    best_idx = np.argmin(fitness)
    return pop[best_idx], fitness[best_idx], np.array(best_fit)

def cma_es_simple(f, x0, sigma0=0.5, n_iter=100, popsize=None):
    n = len(x0)
    m = x0.copy()
    sigma = sigma0
    C = np.eye(n)
    popsize = popsize or 4 + int(3 * np.log(n))
    traj = [m.copy()]

    for t in range(n_iter):
        A = np.linalg.cholesky(C)
        z = np.random.randn(popsize, n)
        x = m + sigma * z @ A.T
        fitness = np.array([f(xi) for xi in x])
        idx = np.argsort(fitness)
        x = x[idx]
        z = z[idx]

        weights = np.log(popsize + 0.5) - np.log(np.arange(1, popsize + 1))
        weights = weights / weights.sum()
        m = m + sigma * (weights @ z) @ A.T
        traj.append(m.copy())

    return np.array(traj)

def main():
    print("=" * 60)
    print("GENETIC ALGORITHMS & CMA-ES")
    print("=" * 60)

    print("\n--- Genetic Algorithm on Rastrigin ---")
    rastrigin = lambda x: 10*len(x) + np.sum(x**2 - 10*np.cos(2*np.pi*x))
    bounds = np.array([[-5, 5]] * 2)
    x_best, f_best, history = genetic_algorithm(rastrigin, bounds, n_pop=100, n_gen=100)
    print(f"  Best solution: x={x_best}")
    print(f"  Best fitness:  {f_best:.4f}")
    print(f"  Expected minimum: 0 at (0, 0)")

    print(f"\n--- GA on Rosenbrock ---")
    rosenbrock = lambda x: (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2
    x_best_r, f_best_r, hist_r = genetic_algorithm(rosenbrock, bounds, n_pop=100, n_gen=50)
    print(f"  Best solution: x={x_best_r}")
    print(f"  Best fitness:  {f_best_r:.6f}")

    print(f"\n--- CMA-ES on Sphere Function ---")
    sphere = lambda x: np.sum(x**2)
    x0 = np.array([5.0, 3.0, -2.0])
    traj_cma = cma_es_simple(sphere, x0, sigma0=0.5, n_iter=50)
    print(f"  Starting: f({x0}) = {sphere(x0)}")
    print(f"  Final: f({traj_cma[-1]}) = {sphere(traj_cma[-1]):.6f}")

    print(f"\n--- CMA-ES on Rosenbrock ---")
    dims = [2, 5, 10]
    for d in dims:
        rosen_d = lambda x: np.sum([100*(x[i+1]-x[i]**2)**2 + (1-x[i])**2 for i in range(d-1)])
        x0_d = np.random.randn(d) * 2
        traj_cma_r = cma_es_simple(rosen_d, x0_d, sigma0=0.3, n_iter=80)
        print(f"  d={d:2d}: final f={rosen_d(traj_cma_r[-1]):.4e}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].semilogy(history, 'b-', linewidth=2, label='GA')
    axes[0].set_xlabel('Generation'); axes[0].set_ylabel('Best Fitness')
    axes[0].set_title('Genetic Algorithm: Rastrigin')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    cma_loss = [np.sum(p**2) for p in traj_cma]
    axes[1].semilogy(cma_loss, 'r-', linewidth=2, label='CMA-ES')
    axes[1].set_xlabel('Iteration'); axes[1].set_ylabel('Fitness')
    axes[1].set_title('CMA-ES: Sphere Function')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/31_genetic_algorithms.png', dpi=100)
    print(f"\nPlot saved to /tmp/31_genetic_algorithms.png")

if __name__ == "__main__":
    main()
