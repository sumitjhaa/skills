import numpy as np
import matplotlib.pyplot as plt

def svrg(grad_f, grad_fi, data, x0, lr=0.01, epoch_size=100, n_epochs=50):
    x = x0.copy()
    N = len(data)
    trajectory = [x.copy()]
    for epoch in range(n_epochs):
        x_tilde = x.copy()
        mu = grad_f(x_tilde, data)
        for t in range(epoch_size):
            i = np.random.randint(N)
            g = grad_fi(x, data[i]) - grad_fi(x_tilde, data[i]) + mu
            x = x - lr * g
            trajectory.append(x.copy())
    return np.array(trajectory)

def saga(grad_fi, data, x0, lr=0.01, n_epochs=50):
    N = len(data)
    x = x0.copy()
    g_old = [grad_fi(x0, d) for d in data]
    g_mean = np.mean(g_old, axis=0)
    trajectory = [x.copy()]
    for epoch in range(n_epochs):
        for i in np.random.permutation(N):
            g_i = grad_fi(x, data[i])
            g = g_i - g_old[i] + g_mean
            x = x - lr * g
            g_mean += (g_i - g_old[i]) / N
            g_old[i] = g_i
            trajectory.append(x.copy())
    return np.array(trajectory)

def main():
    print("=" * 60)
    print("VARIANCE-REDUCED SGD")
    print("=" * 60)

    print("\n--- Logistic Regression: SVRG and SAGA ---")
    np.random.seed(42)
    n, d = 1000, 20
    X = np.random.randn(n, d)
    w_true = np.random.randn(d) * 0.5
    logits = X @ w_true
    p = 1 / (1 + np.exp(-logits))
    y = (p > 0.5).astype(float) * 2 - 1

    def logistic_loss(w, X, y):
        return np.mean(np.log(1 + np.exp(-y * (X @ w))))

    def grad_full(w, data):
        X, y = data
        p = 1 / (1 + np.exp(-y * (X @ w)))
        return -X.T @ (y * (1 - p)) / len(y)

    def grad_i(w, datum):
        x, yi = datum
        p = 1 / (1 + np.exp(-yi * (x @ w)))
        return -x * yi * (1 - p)

    data = [(X[i], y[i]) for i in range(n)]

    x0 = np.zeros(d)

    print(f"  True w norm: {np.linalg.norm(w_true):.4f}")

    traj_sgd = [x0.copy()]
    x = x0.copy()
    lr = 0.1
    for t in range(2000):
        i = np.random.randint(n)
        x = x - lr * grad_i(x, data[i])
        traj_sgd.append(x.copy())

    traj_svrg = svrg(grad_full, grad_i, data, x0, lr=0.1, epoch_size=n, n_epochs=20)

    traj_saga = saga(grad_i, data, x0, lr=0.1, n_epochs=20)

    losses_sgd = [logistic_loss(w, X, y) for w in traj_sgd[::10]]
    losses_svrg = [logistic_loss(w, X, y) for w in traj_svrg[::10]]
    losses_saga = [logistic_loss(w, X, y) for w in traj_saga[::10]]

    print(f"  SGD final loss:  {losses_sgd[-1]:.6f}")
    print(f"  SVRG final loss: {losses_svrg[-1]:.6f}")
    print(f"  SAGA final loss: {losses_saga[-1]:.6f}")

    print(f"\n--- Gradient Variance Comparison ---")
    x_test = np.random.randn(d) * 0.5
    sgd_grads = [grad_i(x_test, data[i]) for i in range(100)]
    sgd_var = np.var(sgd_grads, axis=0).mean()

    x_tilde = np.random.randn(d) * 0.5
    mu = grad_full(x_tilde, (X, y))
    svrg_grads = []
    for i in range(100):
        g = grad_i(x_test, data[i]) - grad_i(x_tilde, data[i]) + mu
        svrg_grads.append(g)
    svrg_var = np.var(svrg_grads, axis=0).mean()

    print(f"  SGD gradient variance:  {sgd_var:.6f}")
    print(f"  SVRG gradient variance: {svrg_var:.6f}")
    print(f"  Variance reduction:     {(1 - svrg_var/sgd_var)*100:.1f}%")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].plot(losses_sgd, 'b-', label='SGD', alpha=0.7)
    axes[0].plot(losses_svrg, 'r-', label='SVRG', linewidth=2)
    axes[0].plot(losses_saga, 'g-', label='SAGA', linewidth=2)
    axes[0].set_xlabel('Iteration (×10)'); axes[0].set_ylabel('Logistic Loss')
    axes[0].set_title('Convergence Comparison')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    methods = ['SGD', 'SVRG', 'SAGA']
    vars_ = [sgd_var, svrg_var, 0]
    axes[1].bar(methods[:2], vars_[:2], color=['blue', 'red'])
    axes[1].set_ylabel('Avg Gradient Variance')
    axes[1].set_title('Gradient Variance at x*')
    axes[1].grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('../../assets/phase02/21_variance_reduced_sgd.png', dpi=100)
    print(f"\nPlot saved to /tmp/21_variance_reduced_sgd.png")

if __name__ == "__main__":
    main()
