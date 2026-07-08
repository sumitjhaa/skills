"""06.11 - LR Schedulers: Step, Cosine, OneCycle, Warmup, ReduceOnPlateau"""

import numpy as np
import matplotlib.pyplot as plt


class StepLR:
    def __init__(self, initial_lr=0.1, step_size=30, gamma=0.5):
        self.initial_lr = initial_lr
        self.step_size = step_size
        self.gamma = gamma

    def get_lr(self, epoch):
        return self.initial_lr * self.gamma ** (epoch // self.step_size)


class ExponentialLR:
    def __init__(self, initial_lr=0.1, gamma=0.95):
        self.initial_lr = initial_lr
        self.gamma = gamma

    def get_lr(self, epoch):
        return self.initial_lr * self.gamma ** epoch


class CosineLR:
    def __init__(self, initial_lr=0.1, T=100, eta_min=0):
        self.initial_lr = initial_lr
        self.T = T
        self.eta_min = eta_min

    def get_lr(self, epoch):
        if epoch >= self.T:
            return self.eta_min
        return self.eta_min + 0.5 * (self.initial_lr - self.eta_min) * (1 + np.cos(np.pi * epoch / self.T))


class OneCycleLR:
    def __init__(self, max_lr=0.1, total_steps=100, pct_start=0.3, div_factor=25):
        self.max_lr = max_lr
        self.total_steps = total_steps
        self.pct_start = pct_start
        self.div_factor = div_factor
        self.min_lr = max_lr / div_factor

    def get_lr(self, step):
        if step >= self.total_steps:
            return self.min_lr
        if step < self.pct_start * self.total_steps:
            fraction = step / (self.pct_start * self.total_steps)
            return self.min_lr + (self.max_lr - self.min_lr) * fraction
        else:
            fraction = (step - self.pct_start * self.total_steps) / ((1 - self.pct_start) * self.total_steps)
            return self.max_lr - (self.max_lr - self.min_lr) * fraction


class WarmupLR:
    def __init__(self, initial_lr=0.1, warmup_steps=10):
        self.initial_lr = initial_lr
        self.warmup_steps = warmup_steps

    def get_lr(self, step):
        if step < self.warmup_steps:
            return self.initial_lr * (step + 1) / self.warmup_steps
        return self.initial_lr


class ReduceLROnPlateau:
    def __init__(self, initial_lr=0.1, factor=0.5, patience=5, min_lr=1e-6):
        self.initial_lr = initial_lr
        self.factor = factor
        self.patience = patience
        self.min_lr = min_lr
        self.best_loss = float("inf")
        self.wait = 0
        self.current_lr = initial_lr

    def get_lr(self, loss):
        if loss < self.best_loss:
            self.best_loss = loss
            self.wait = 0
        else:
            self.wait += 1
            if self.wait >= self.patience:
                self.current_lr = max(self.current_lr * self.factor, self.min_lr)
                self.wait = 0
        return self.current_lr


if __name__ == "__main__":
    schedulers = {
        "StepLR": StepLR(initial_lr=0.1, step_size=30, gamma=0.5),
        "ExponentialLR": ExponentialLR(initial_lr=0.1, gamma=0.95),
        "CosineLR": CosineLR(initial_lr=0.1, T=100),
        "OneCycleLR": OneCycleLR(max_lr=0.1, total_steps=100),
        "WarmupLR": WarmupLR(initial_lr=0.1, warmup_steps=10),
    }

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()

    for idx, (name, scheduler) in enumerate(schedulers.items()):
        lrs = []
        for epoch in range(100):
            lrs.append(scheduler.get_lr(epoch))
        axes[idx].plot(lrs, linewidth=2)
        axes[idx].set_title(name)
        axes[idx].set_xlabel("Epoch")
        axes[idx].set_ylabel("Learning Rate")
        axes[idx].grid(True, alpha=0.3)

    rp = ReduceLROnPlateau(initial_lr=0.1, patience=10)
    losses = np.exp(-np.arange(100) / 30) + 0.01 * np.random.randn(100)
    losses[40:] += 0.05
    lrs_rp = []
    for i in range(100):
        lrs_rp.append(rp.get_lr(losses[i]))
    axes[5].plot(lrs_rp, linewidth=2)
    axes[5].set_title("ReduceLROnPlateau")
    axes[5].set_xlabel("Step")
    axes[5].grid(True, alpha=0.3)

    for name, scheduler in schedulers.items():
        print(f"{name:20s}: final LR = {scheduler.get_lr(99):.6f}")

    print(f"{'ReduceLROnPlateau':20s}: final LR = {rp.current_lr:.6f}")
    plt.tight_layout()
    plt.savefig("../../assets/phase06/lr_schedulers.png")
    plt.close()
    print("\nAll LR schedulers implemented and plotted.")
