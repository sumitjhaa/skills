import numpy as np
import matplotlib.pyplot as plt

def rnn_optimizer_step(x, grad, h, W):
    input_features = np.hstack([grad, x])
    h_next = np.tanh(W['ih'] @ input_features + W['hh'] @ h)
    update = W['ho'] @ h_next
    return x - update, h_next

def learned_gd_step(x, grad, alpha, beta):
    return x - (alpha * grad + beta * x)

def train_meta_optimizer(problem_dist, meta_lr=0.01, n_tasks=100, n_steps=20):
    d = problem_dist['dim']
    alpha = np.ones(d) * 0.1
    beta = np.ones(d) * 0.01

    for task in range(n_tasks):
        w_true = problem_dist['sample']()
        x0 = np.random.randn(d)
        x = x0.copy()
        meta_grad_alpha = np.zeros(d)
        meta_grad_beta = np.zeros(d)
        xs = [x.copy()]

        for t in range(n_steps):
            grad = problem_dist['grad'](x, w_true)
            x = learned_gd_step(x, grad, alpha, beta)
            xs.append(x.copy())

        final_loss = problem_dist['loss'](x, w_true)
        if task < 5:
            print(f"    Task {task}: final loss = {final_loss:.4f}")

    return alpha, beta, xs

def main():
    print("=" * 60)
    print("LEARN TO OPTIMIZE")
    print("=" * 60)

    print("\n--- Learned Gradient Descent Step ---")
    d = 2
    alpha_learned = np.array([0.08, 0.12])
    beta_learned = np.array([0.01, 0.02])

    f_quad = lambda x, w: 0.5 * np.sum((x - w)**2)
    grad_quad = lambda x, w: x - w

    w_true = np.array([2.0, -1.0])
    x0 = np.array([5.0, -4.0])

    x_learned = x0.copy()
    traj_learned = [x_learned.copy()]
    for t in range(50):
        g = grad_quad(x_learned, w_true)
        x_learned = learned_gd_step(x_learned, g, alpha_learned, beta_learned)
        traj_learned.append(x_learned.copy())

    x_gd = x0.copy()
    traj_gd = [x_gd.copy()]
    for t in range(50):
        g = grad_quad(x_gd, w_true)
        x_gd = x_gd - 0.1 * g
        traj_gd.append(x_gd.copy())

    print(f"  True w: {w_true}")
    print(f"  Learned GD final: {traj_learned[-1]}")
    print(f"  Standard GD final: {traj_gd[-1]}")
    print(f"  Learned GD error: {np.linalg.norm(traj_learned[-1] - w_true):.4f}")
    print(f"  Standard GD error: {np.linalg.norm(traj_gd[-1] - w_true):.4f}")

    print(f"\n--- RNNOpt Style Update ---")
    np.random.seed(42)
    W_ih = np.random.randn(10, 2 + 1) * 0.1
    W_hh = np.random.randn(10, 10) * 0.1
    W_ho = np.random.randn(1, 10) * 0.1
    W = {'ih': W_ih, 'hh': W_hh, 'ho': W_ho}

    x_opt = np.array([1.0])
    h = np.zeros(10)
    x_rnn = np.array([-3.0])
    traj_rnn = [x_rnn.copy()]

    for t in range(30):
        g = np.array([2 * (x_rnn[0] - x_opt[0])])
        x_rnn, h = rnn_optimizer_step(x_rnn, g, h, W)
        traj_rnn.append(x_rnn.copy())

    print(f"  RNNOpt final: x = {traj_rnn[-1, 0]:.4f}")
    print(f"  Target:       x = {x_opt[0]:.4f}")

    print(f"\n--- Meta-Training of Learned Optimizer ---")
    problem_dist = {
        'dim': 2,
        'sample': lambda: np.random.randn(2) * 3,
        'grad': lambda x, w: x - w,
        'loss': lambda x, w: 0.5 * np.sum((x - w)**2)
    }

    alpha, beta, traj_meta = train_meta_optimizer(problem_dist, n_tasks=20, n_steps=30)
    print(f"  Learned α = {alpha}")
    print(f"  Learned β = {beta}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    learned_loss = [0.5 * np.sum((p - w_true)**2) for p in traj_learned]
    gd_loss = [0.5 * np.sum((p - w_true)**2) for p in traj_gd]
    axes[0].semilogy(learned_loss, 'r-', label='Learned GD', linewidth=2)
    axes[0].semilogy(gd_loss, 'b-', label='Standard GD')
    axes[0].set_xlabel('Iteration'); axes[0].set_ylabel('f(x) - f(x*)')
    axes[0].set_title('Learned vs Standard Optimizer')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    axes[1].plot(traj_rnn, 'g-', linewidth=2)
    axes[1].axhline(x_opt[0], color='k', linestyle='--', alpha=0.5)
    axes[1].set_xlabel('Iteration'); axes[1].set_ylabel('x')
    axes[1].set_title('RNN-Based Optimizer Trajectory')
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/39_learn_to_optimize.png', dpi=100)
    print(f"\nPlot saved to /tmp/39_learn_to_optimize.png")

if __name__ == "__main__":
    main()
