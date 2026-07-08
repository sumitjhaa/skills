"""
07.24 MCMC for Deep Learning: Metropolis-Hastings, HMC, SGLD.
"""
import numpy as np
import matplotlib.pyplot as plt


def target_log_p(x):
    """Bimodal target: mixture of Gaussians."""
    return np.log(0.3 * np.exp(-0.5 * ((x[..., 0] + 2)**2 + x[..., 1]**2) / 0.5) +
                  0.7 * np.exp(-0.5 * ((x[..., 0] - 2)**2 + x[..., 1]**2) / 0.5))


class MetropolisHastings:
    def __init__(self, step_size=0.5):
        self.step_size = step_size

    def sample(self, x_init, n_samples=1000):
        samples = [x_init]
        for _ in range(n_samples):
            x_curr = samples[-1]
            x_prop = x_curr + self.step_size * np.random.randn(*x_curr.shape)
            log_accept = target_log_p(x_prop) - target_log_p(x_curr)
            if np.log(np.random.rand()) < log_accept:
                samples.append(x_prop)
            else:
                samples.append(x_curr)
        return np.array(samples)


class HMC:
    """Hamiltonian Monte Carlo."""
    def __init__(self, eps=0.1, L=10):
        self.eps = eps
        self.L = L

    def grad_log_p(self, x):
        eps_fd = 1e-4
        grad = np.zeros_like(x)
        for i in range(x.shape[-1]):
            xp = x.copy()
            xm = x.copy()
            xp[..., i] += eps_fd
            xm[..., i] -= eps_fd
            grad[..., i] = (target_log_p(xp) - target_log_p(xm)) / (2 * eps_fd)
        return grad

    def sample(self, x_init, n_samples=500):
        samples = [x_init]
        for _ in range(n_samples):
            q = samples[-1].copy()
            p = np.random.randn(*q.shape)
            p0 = p.copy()
            p -= 0.5 * self.eps * self.grad_log_p(q)
            for _ in range(self.L - 1):
                q += self.eps * p
                p -= self.eps * self.grad_log_p(q)
            q += self.eps * p
            p -= 0.5 * self.eps * self.grad_log_p(q)
            p = -p
            log_accept = target_log_p(q) - target_log_p(samples[-1]) - 0.5 * (p @ p - p0 @ p0)
            if np.log(np.random.rand()) < log_accept:
                samples.append(q)
            else:
                samples.append(samples[-1])
        return np.array(samples)


class SGLD:
    """Stochastic Gradient Langevin Dynamics."""
    def __init__(self, lr=0.01):
        self.lr = lr

    def sample(self, x_init, n_steps=1000):
        x = x_init.copy()
        samples = [x]
        for t in range(n_steps):
            eps_t = self.lr / (1 + t * 0.01)
            grad = np.random.randn(*x.shape)  # simulated gradient
            noise = np.sqrt(2 * eps_t) * np.random.randn(*x.shape)
            x = x + eps_t * grad + noise
            samples.append(x)
        return np.array(samples)


if __name__ == "__main__":
    np.random.seed(42)
    x_init = np.array([0.0, 0.0])

    print("=== Metropolis-Hastings ===")
    mh = MetropolisHastings(step_size=0.5)
    mh_samples = mh.sample(x_init, 2000)

    print("=== HMC ===")
    hmc = HMC(eps=0.1, L=10)
    hmc_samples = hmc.sample(x_init, 500)

    print("=== SGLD ===")
    sgld = SGLD(lr=0.1)
    sgld_samples = sgld.sample(x_init, 2000)

    plt.figure(figsize=(14, 4))
    plt.subplot(131)
    plt.scatter(mh_samples[:, 0], mh_samples[:, 1], s=5, alpha=0.3)
    plt.title(f'MH ({len(mh_samples)} samples)')
    plt.subplot(132)
    plt.scatter(hmc_samples[:, 0], hmc_samples[:, 1], s=5, alpha=0.3)
    plt.title(f'HMC ({len(hmc_samples)} samples)')
    plt.subplot(133)
    plt.scatter(sgld_samples[:, 0], sgld_samples[:, 1], s=5, alpha=0.3)
    plt.title(f'SGLD ({len(sgld_samples)} samples)')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/mcmc.png')
    plt.close()
    print("Saved mcmc.png")
