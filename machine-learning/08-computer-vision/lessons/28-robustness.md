# 08.28 Robustness

## Learning Objectives
- Understand adversarial attacks (FGSM, PGD) and defences
- Implement data augmentation for distribution shift robustness
- Apply randomised smoothing for certified robustness
- Evaluate on ImageNet-C, ImageNet-R, ImageNet-A

## Adversarial Attacks

### Threat Model
$$\|x' - x\|_p < \epsilon, \quad f(x') \neq y$$

- $\ell_\infty$: Each pixel changes ≤ $\epsilon$
- $\ell_2$: Euclidean distance ≤ $\epsilon$
- $\ell_1$: Sparse perturbations (few pixels changed significantly)

### FGSM (Fast Gradient Sign Method)
Single-step attack:

$$x' = x + \epsilon \cdot \text{sign}(\nabla_x \mathcal{L}(x, y))$$

- $\epsilon = 8/255$ for ImageNet ($\ell_\infty$)
- 100% success rate on standard models

### PGD (Projected Gradient Descent)
Iterative generalisation:

$$x^{t+1} = \text{Proj}_{B(x, \epsilon)} (x^t + \alpha \cdot \text{sign}(\nabla_x \mathcal{L}(x^t, y)))$$

- $\alpha = 2/255$, steps = 7-40
- Stronger attack than FGSM

### CW (Carlini-Wagner)
Optimisation-based:

$$\min_\delta \|\delta\|_p + c \cdot \max(0, f(x+\delta)_y - \max_{j \neq y} f(x+\delta)_j + \kappa)$$

## Defences

### Adversarial Training
Train on adversarial examples:

$$\min_\theta \mathbb{E}_{(x,y) \sim D} \left[ \max_{\|\delta\|_\infty \leq \epsilon} \mathcal{L}(f_\theta(x + \delta), y) \right]$$

- **PGD-AT**: PGD adversarial training (Madry et al.)
- **TRADES**: Trade-off between clean and adversarial accuracy
- **FreeAT**: Free adversarial training (reuse backward pass)

### Input Transformation
- JPEG compression (removes high-frequency perturbations)
- Random resizing + padding
- Feature squeezing: reduce colour bit depth, spatial smoothing

### Certified Defences (Randomised Smoothing)
Construct robust classifier $g$ from base classifier $f$:

$$g(x) = \arg\max_{c \in \mathcal{Y}} \mathbb{P}_\delta(f(x + \delta) = c), \quad \delta \sim \mathcal{N}(0, \sigma^2 I)$$

**Certification**: $g$ is provably robust at $x$ within radius $R$:

$$R = \frac{\sigma}{2} \left(\Phi^{-1}(p_A) - \Phi^{-1}(p_B)\right)$$

- $p_A$: probability of top class
- $p_B$: probability of second class

## Distribution Shift

### Types
| Shift | Description | Example |
|-------|-------------|---------|
| Covariate shift | $P(x)$ changes, $P(y|x)$ same | Different camera |
| Label shift | $P(y)$ changes | New class distribution |
| Concept drift | $P(y|x)$ changes | New definition of "quality" |

### Domain Generalisation
Train on multiple source domains → generalise to unseen target:
- **Domain alignment**: MMD, CORAL (align feature distributions)
- **Meta-learning**: MLDG (meta-learning for domain generalisation)
- **Data augmentation**: Mixup, CutMix, RandAugment

## Code: PGD Adversarial Training

```python
import torch
import torch.nn.functional as F

def pgd_attack(model, x, y, eps=8/255, alpha=2/255, steps=7):
    x_adv = x.clone().detach() + torch.randn_like(x).uniform_(-eps, eps)
    x_adv = torch.clamp(x_adv, 0, 1)
    
    for _ in range(steps):
        x_adv.requires_grad_()
        logits = model(x_adv)
        loss = F.cross_entropy(logits, y)
        grad = torch.autograd.grad(loss, x_adv)[0]
        
        x_adv = x_adv + alpha * grad.sign()
        x_adv = torch.max(torch.min(x_adv, x + eps), x - eps)
        x_adv = torch.clamp(x_adv, 0, 1).detach()
    
    return x_adv

def adversarial_training_step(model, x, y, optimizer, eps=8/255):
    x_adv = pgd_attack(model, x, y, eps=eps)
    logits = model(x_adv)
    loss = F.cross_entropy(logits, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss.item()
```

## Robustness Benchmarks

| Benchmark | Type | Data | Metric | Standard ResNet-50 | Robust ResNet-50 |
|-----------|------|------|--------|-------------------|------------------|
| ImageNet-C | Corruptions | 75 corruptions × 5 severities | mCE | 76.7 | 55.0 |
| ImageNet-R | Renditions | Art, cartoons, sketches | Top-1 | 36.1 | 50.8 |
| ImageNet-A | Adversarial | Natural adversarial examples | Top-1 | 0.0 | 23.1 |
| ImageNet-Sketch | Sketch | Black & white sketches | Top-1 | 24.4 | 36.5 |
| ObjectNet | Pose/context | Controlled backgrounds | Top-1 | 13.5 | 21.6 |

## Practical Considerations
- **Clean vs robust trade-off**: Adversarial training reduces clean accuracy by 5-15%
- **Data augmentation**: More important than architectural changes for distribution shift
- **Transfer of robustness**: Robust models have better feature representations (useful for detection)
- **Evaluation**: Use AutoAttack for reliable adversarial evaluation (not PGD)

## References
- Goodfellow, Shlens, Szegedy, "Explaining and Harnessing Adversarial Examples", ICLR 2015
- Madry, Makelov, Schmidt, Tsipras, Vladu, "Towards Deep Learning Models Resistant to Adversarial Attacks", ICLR 2018
- Hendrycks & Dietterich, "Benchmarking Neural Network Robustness to Common Corruptions and Perturbations", ICLR 2019
- Cohen, Rosenfeld, Kolter, "Certified Adversarial Robustness via Randomized Smoothing", ICML 2019
- Croce, Andriushchenko, et al., "Reliable evaluation of adversarial robustness with an ensemble of diverse parameter-free attacks", ICML 2020
