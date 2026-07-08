"""
09.11 Knowledge Distillation — Temperature-scaled logit distillation with analysis.
"""
import numpy as np
import matplotlib.pyplot as plt

def softmax(x, T=1.0, axis=-1):
    x = x / T
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / np.sum(e, axis=axis, keepdims=True)

def cross_entropy(logits, labels):
    N, C = logits.shape
    probs = softmax(logits, T=1.0)
    return -np.mean(np.log(probs[np.arange(N), labels] + 1e-10))

def kl_divergence(p, q):
    return np.sum(p * (np.log(p + 1e-10) - np.log(q + 1e-10)), axis=-1)

def distillation_loss(student_logits, teacher_logits, labels, T=4.0, alpha=0.5):
    N, C = student_logits.shape
    teacher_probs = softmax(teacher_logits, T=T)
    student_probs = softmax(student_logits, T=T)
    distill = kl_divergence(teacher_probs, student_probs).mean()
    ce_loss = cross_entropy(student_logits / T, labels)
    loss = (1 - alpha) * ce_loss + alpha * T * T * distill
    return loss, ce_loss, distill

def calibrate_teacher(student_logits, teacher_logits, labels,
                      temps=[1.0, 2.0, 4.0, 6.0, 10.0], alpha=0.5):
    results = []
    for T in temps:
        loss, ce, distill = distillation_loss(
            student_logits, teacher_logits, labels, T=T, alpha=alpha)
        results.append((T, loss, ce, distill))
    return results

def student_training_simulation(n_steps=200, N=32, C=10, T=4.0, alpha=0.5):
    np.random.seed(42)
    teacher_logits = np.random.randn(N, C) * 2.0
    labels = np.random.randint(0, C, size=N)
    student_logits = np.random.randn(N, C) * 0.1
    loss_history = []
    lr = 0.05
    for step in range(n_steps):
        loss, ce, distill = distillation_loss(
            student_logits, teacher_logits, labels, T=T, alpha=alpha)
        loss_history.append((loss, ce, distill))
        grad = np.zeros_like(student_logits)
        teacher_probs = softmax(teacher_logits, T=T)
        student_probs = softmax(student_logits, T=T)
        grad_ce = student_probs - np.eye(C)[labels]
        grad_distill = (student_probs - teacher_probs) / T
        grad = (1 - alpha) * grad_ce + alpha * T * T * grad_distill
        student_logits -= lr * grad
    return student_logits, np.array(loss_history), teacher_logits, labels

if __name__ == "__main__":
    np.random.seed(42)
    print("=== Knowledge Distillation ===\n")

    N, C = 32, 10
    student_logits = np.random.randn(N, C) * 0.5
    teacher_logits = np.random.randn(N, C) * 3.0
    labels = np.random.randint(0, C, size=N)

    loss, ce, distill = distillation_loss(student_logits, teacher_logits, labels)
    print(f"Total loss:      {loss:.4f}")
    print(f"CE (hard):       {ce:.4f}")
    print(f"Distill (soft):  {distill:.4f}")

    # Temperature sweep
    print("\nTemperature effect on KL divergence:")
    temps = [0.5, 1.0, 2.0, 4.0, 8.0, 16.0]
    for T in temps:
        teacher_soft = softmax(teacher_logits, T=T)
        student_soft = softmax(student_logits, T=T)
        kl = kl_divergence(teacher_soft, student_soft).mean()
        teacher_entropy = -np.sum(teacher_soft * np.log(teacher_soft + 1e-10),
                                  axis=-1).mean()
        print(f"  T={T:5.1f}: KL={kl:.4f}, H(teacher)={teacher_entropy:.4f}")

    # Alpha sweep
    print("\nAlpha effect on loss components:")
    for alpha in [0.0, 0.25, 0.5, 0.75, 1.0]:
        loss_a, ce_a, distill_a = distillation_loss(
            student_logits, teacher_logits, labels, T=4.0, alpha=alpha)
        print(f"  alpha={alpha:.2f}: total={loss_a:.4f}, "
              f"CE={ce_a:.4f}, distill={distill_a:.4f}")

    # Simulate student training via distillation
    print("\nSimulating student training via distillation...")
    student_final, loss_hist, teacher_logits, labels = \
        student_training_simulation(n_steps=150)

    print(f"Student CE before: {cross_entropy(np.random.randn(N, C) * 0.1, labels):.4f}")
    print(f"Student CE after:  {cross_entropy(student_final, labels):.4f}")
    print(f"Teacher CE:        {cross_entropy(teacher_logits, labels):.4f}")

    # Prediction agreement
    teacher_preds = np.argmax(softmax(teacher_logits), axis=1)
    student_preds = np.argmax(softmax(student_final), axis=1)
    agreement = np.mean(teacher_preds == student_preds)
    print(f"Teacher-student prediction agreement: {agreement:.1%}")

    # Visualization
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # Temperature effect
    T_vals = np.array(temps)
    kl_vals = []
    for T in T_vals:
        tp = softmax(teacher_logits, T=T)
        sp = softmax(student_logits, T=T)
        kl_vals.append(kl_divergence(tp, sp).mean())
    kl_vals = np.array(kl_vals)
    axes[0, 0].plot(T_vals, kl_vals, 'o-')
    axes[0, 0].set_xlabel("Temperature T")
    axes[0, 0].set_ylabel("KL(teacher || student)")
    axes[0, 0].set_title("Temperature vs KL Divergence")
    axes[0, 0].grid(True, alpha=0.3)

    # Training simulation
    axes[0, 1].plot(loss_hist[:, 0], label='Total', lw=2)
    axes[0, 1].plot(loss_hist[:, 1], label='CE (hard)', ls='--')
    axes[0, 1].plot(loss_hist[:, 2], label='Distill (soft)', ls=':')
    axes[0, 1].set_xlabel("Training step")
    axes[0, 1].set_ylabel("Loss")
    axes[0, 1].set_title("Student Loss During Distillation")
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Softmax distributions
    sample_idx = 0
    teacher_probs = softmax(teacher_logits[sample_idx:sample_idx + 1], T=1.0).ravel()
    student_before = softmax(np.random.randn(1, C) * 0.1, T=1.0).ravel()
    student_after = softmax(student_final[sample_idx:sample_idx + 1], T=1.0).ravel()
    x_pos = np.arange(C)
    w = 0.25
    axes[0, 2].bar(x_pos - w, teacher_probs, w, label='Teacher', alpha=0.8)
    axes[0, 2].bar(x_pos, student_before, w, label='Student (before)', alpha=0.8)
    axes[0, 2].bar(x_pos + w, student_after, w, label='Student (after)', alpha=0.8)
    axes[0, 2].set_xlabel("Class")
    axes[0, 2].set_ylabel("Probability")
    axes[0, 2].set_title("Output Distribution Comparison")
    axes[0, 2].legend()
    axes[0, 2].grid(True, axis='y', alpha=0.3)

    # Soft vs hard target visualisation
    T_show = 4.0
    teacher_soft = softmax(teacher_logits[:3], T=T_show)
    for i in range(3):
        axes[1, 0].plot(teacher_soft[i], 'o-', lw=1.5, label=f'Ex {i}')
    axes[1, 0].set_xlabel("Class")
    axes[1, 0].set_ylabel("Soft probability")
    axes[1, 0].set_title(f"Teacher Soft Targets (T={T_show})")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Alpha vs loss trade-off
    alphas = np.linspace(0, 1, 11)
    total_losses = []
    ce_losses = []
    distill_losses = []
    for alpha in alphas:
        l, c, d = distillation_loss(student_logits, teacher_logits,
                                     labels, T=4.0, alpha=alpha)
        total_losses.append(l)
        ce_losses.append(c)
        distill_losses.append(d)
    axes[1, 1].plot(alphas, total_losses, 'k-', lw=2, label='Total')
    axes[1, 1].plot(alphas, ce_losses, 'b--', label='CE')
    axes[1, 1].plot(alphas, distill_losses, 'r:', label='Distill')
    axes[1, 1].set_xlabel("Alpha")
    axes[1, 1].set_ylabel("Loss")
    axes[1, 1].set_title("Alpha vs Loss Components")
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    # Teacher confidence vs distillation benefit
    axes[1, 2].hist(np.max(softmax(teacher_logits), axis=1),
                    bins=15, alpha=0.6, label='Teacher')
    axes[1, 2].hist(np.max(softmax(student_final), axis=1),
                    bins=15, alpha=0.6, label='Student')
    axes[1, 2].set_xlabel("Max probability (confidence)")
    axes[1, 2].set_ylabel("Count")
    axes[1, 2].set_title("Confidence Distribution")
    axes[1, 2].legend()
    axes[1, 2].grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig("../../assets/phase09/distillation.png")
    plt.close()
    print("\nFigure saved to distillation.png")

    # Edge cases
    print("\n=== Edge Cases ===")
    N_e, C_e = 4, 5
    s_e = np.zeros((N_e, C_e))
    s_e[np.arange(N_e), np.random.randint(0, C_e, N_e)] = 10.0
    t_e = np.ones((N_e, C_e)) * 2.0
    labels_e = np.random.randint(0, C_e, N_e)
    loss_e, ce_e, dist_e = distillation_loss(s_e, t_e, labels_e)
    print(f"  Extreme logits: loss={loss_e:.4f}, CE={ce_e:.4f}, distill={dist_e:.4f}")

    t_identical = s_e.copy()
    l_e2, _, _ = distillation_loss(s_e, t_identical, labels_e)
    print(f"  Teacher = student: loss={l_e2:.4f}")

    # T=1 should reduce to CE (with alpha=0)
    s_1 = np.random.randn(N_e, C_e) * 0.5
    t_1 = np.random.randn(N_e, C_e) * 2.0
    l_e3, c_e3, d_e3 = distillation_loss(s_1, t_1, labels_e, T=1.0, alpha=0.0)
    ce_direct = cross_entropy(s_1, labels_e)
    print(f"  alpha=0, T=1: loss={l_e3:.4f}, direct CE={ce_direct:.4f}")
