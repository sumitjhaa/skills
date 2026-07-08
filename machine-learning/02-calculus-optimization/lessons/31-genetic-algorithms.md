# 31. Genetic Algorithms & CMA-ES

## Introduction

Genetic algorithms (GAs) are population-based optimization methods inspired by natural evolution. They use selection, crossover, and mutation to evolve solutions.

## Core Operations

### Selection
Tournament selection: pick k individuals randomly, keep the best.

```python
import numpy as np

def tournament_selection(population, fitness, k=3):
    """Tournament selection."""
    idx = np.random.choice(len(population), k, replace=False)
    best_idx = idx[np.argmin(fitness[idx])]
    return population[best_idx].copy()
```

### Crossover (Recombination)
Simulated binary crossover (SBX) for real-valued genomes:

```python
def sbx_crossover(p1, p2, eta=15):
    """Simulated binary crossover."""
    n = len(p1)
    c1, c2 = p1.copy(), p2.copy()
    for i in range(n):
        if np.random.rand() < 0.5:
            u = np.random.rand()
            beta = (2*u)**(1/(eta+1)) if u <= 0.5 else (1/(2*(1-u)))**(1/(eta+1))
            c1[i] = 0.5 * ((1 + beta) * p1[i] + (1 - beta) * p2[i])
            c2[i] = 0.5 * ((1 - beta) * p1[i] + (1 + beta) * p2[i])
    return c1, c2
```

### Mutation
Polynomial mutation:

```python
def polynomial_mutation(x, pm=0.1, eta=20, bounds=None):
    """Polynomial mutation."""
    y = x.copy()
    for i in range(len(x)):
        if np.random.rand() < pm:
            u = np.random.rand()
            delta = (2*u)**(1/(eta+1)) - 1 if u < 0.5 else 1 - (2*(1-u))**(1/(eta+1))
            if bounds is not None:
                y[i] += delta * (bounds[i, 1] - bounds[i, 0])
    return y
```

## Simple Genetic Algorithm

```python
def genetic_algorithm(f, bounds, n_pop=50, n_gen=100, pm=0.1, pc=0.9):
    """Simple genetic algorithm."""
    dim = bounds.shape[0]
    pop = np.random.uniform(bounds[:, 0], bounds[:, 1], (n_pop, dim))
    fitness = np.array([f(ind) for ind in pop])

    for gen in range(n_gen):
        new_pop = []
        while len(new_pop) < n_pop:
            p1 = tournament_selection(pop, fitness)
            p2 = tournament_selection(pop, fitness)
            if np.random.rand() < pc:
                c1, c2 = sbx_crossover(p1, p2)
            else:
                c1, c2 = p1.copy(), p2.copy()
            c1 = polynomial_mutation(c1, pm, bounds=bounds)
            c2 = polynomial_mutation(c2, pm, bounds=bounds)
            new_pop.extend([c1, c2])

        pop = np.array(new_pop[:n_pop])
        fitness = np.array([f(ind) for ind in pop])

    return pop[np.argmin(fitness)]
```

## CMA-ES (Covariance Matrix Adaptation ES)

CMA-ES adapts the sampling distribution's covariance matrix, making it one of the most powerful derivative-free optimizers:

```python
def cma_es(f, x0, sigma0=0.5, n_iter=100, popsize=None):
    """Simplified CMA-ES."""
    n = len(x0)
    m = x0.copy()
    sigma = sigma0
    C = np.eye(n)
    popsize = popsize or 4 + int(3 * np.log(n))

    for t in range(n_iter):
        # Sample population
        A = np.linalg.cholesky(C)
        z = np.random.randn(popsize, n)
        x = m + sigma * z @ A.T
        fitness = np.array([f(xi) for xi in x])

        # Sort by fitness
        idx = np.argsort(fitness)
        x = x[idx]
        z = z[idx]

        # Update mean (weighted selection)
        weights = np.log(popsize + 0.5) - np.log(np.arange(1, popsize + 1))
        weights = weights / weights.sum()
        m_old = m.copy()
        m = m + sigma * (weights @ z) @ A.T

        # Update covariance (rank-µ update)
        z_w = z[:popsize//2]
        C = C + (1/popsize) * (z_w.T @ np.diag(weights[:popsize//2]) @ z_w - C)

    return m
```

## Applications

- **Neural architecture search**: Evolving network architectures
- **Feature selection**: Finding optimal feature subsets
- **Robotics**: Evolving gaits and controllers
- **Hyperparameter tuning**: Black-box optimization

CMA-ES is considered the state-of-the-art in continuous black-box optimization and is the default solver in many Bayesian optimization frameworks for the inner acquisition optimization.
