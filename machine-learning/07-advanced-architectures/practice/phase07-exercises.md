# Phase 07 Exercises: Advanced Architectures & Frontier Models

## Exercise 1: Implement a minimal KAN with B-splines

**Theory:** Explain how Kolmogorov-Arnold Networks differ from MLPs in terms of the learnable functions. Why might spline-based activation on edges be more interpretable than fixed activations on nodes?

**Coding:** Implement a Kolmogorov-Arnold Network using B-spline basis functions. Train it to fit `y = sin(2πx) + 0.1 * noise` with 50 data points. Compare with a standard MLP of similar capacity.

## Exercise 2: Neural ODE for spiral classification

**Theory:** Derive the adjoint sensitivity method for Neural ODEs. Why is the memory cost of the adjoint method O(1) with respect to the number of ODE steps, compared to O(N) for backpropagating through the solver?

**Coding:** Implement a Neural ODE that learns a continuous transformation from a 2D Gaussian to a spiral distribution. Use Euler's method for the ODE solver and adjoint sensitivity for gradients.

## Exercise 3: PINN for the 1D wave equation

**Theory:** Explain the components of the PINN loss function: PDE residual, boundary conditions, and initial conditions. Why is the wave equation a second-order PDE, and what does the characteristic speed c represent?

**Coding:** Solve the 1D wave equation `u_tt = c² u_xx` with a PINN. Use initial conditions `u(x,0) = sin(πx)` and boundary conditions `u(0,t) = u(1,t) = 0`. Visualize the solution over time.

## Exercise 4: DEQ for pixel-level regression

**Theory:** Explain how Deep Equilibrium Models use fixed-point iteration to implicitly define a layer. What is the key advantage of DEQs over explicit-depth networks in terms of memory and representational capacity?

**Coding:** Implement a Deep Equilibrium Model for image denoising. Use a fixed-point iteration layer with Anderson acceleration. Compare convergence speed with simple fixed-point iteration.

## Exercise 5: SIREN for image representation

**Theory:** Why does the sinusoidal activation function in SIREN allow it to represent high-frequency signals better than ReLU-based networks? What is the role of the frequency scaling factor ω₀?

**Coding:** Use a SIREN (sinusoidal representation network) to represent a grayscale image. Train it to map pixel coordinates (x,y) to intensity. Visualize the reconstruction quality vs training time.

## Exercise 6: Custom Mamba block (selective SSM)

**Theory:** Explain the key innovation in Mamba-style selective state space models: how do input-dependent parameters (B, C) enable content-aware reasoning? Why can't standard SSMs perform this selection?

**Coding:** Implement a simplified Mamba-style selective state space model. Include the input-dependent selection mechanism (B and C become functions of input). Test on a synthetic long-range dependency task.

## Exercise 7: DDPM on a 2D dataset

**Theory:** Derive the variational lower bound for diffusion models. Explain why the reverse process can be interpreted as predicting the noise ε rather than the image x₀ directly.

**Coding:** Implement a Denoising Diffusion Probabilistic Model on a 2D mixture of Gaussians (4 modes at (±2, ±2)). Visualize the reverse diffusion process and generate 1000 samples. Compute the coverage of all modes.

## Exercise 8: Normalizing flow for density estimation

**Theory:** Explain the change-of-variables formula and why normalizing flows require the Jacobian determinant to be tractable. Why are affine coupling layers designed to have a triangular Jacobian?

**Coding:** Implement a Real NVP normalizing flow with at least 4 affine coupling layers. Train it on a 2D "moon" dataset (two interleaving half circles). Visualize the learned density by sampling and by plotting the log-density on a grid.

## Exercise 9: Contrastive learning on synthetic data

**Theory:** Explain the InfoNCE loss and its relationship to mutual information maximization. Why does SimCLR require a projection head, and what happens if you remove it?

**Coding:** Implement SimCLR-style contrastive learning on synthetic data. Use random noise augmentations. Train an encoder and visualize the learned embeddings with t-SNE. Show that positive pairs cluster together.

## Exercise 10: MCMC for Bayesian neural network posterior

**Theory:** Explain why Hamiltonian Monte Carlo produces better samples for BNN posteriors than random-walk Metropolis-Hastings. What role does the leapfrog integrator play in preserving the Hamiltonian?

**Coding:** Implement a 2-layer Bayesian neural network and sample the posterior over weights using HMC. Visualize the predictive distribution with uncertainty bands (mean ± 2 std) on a 1D regression task.

## Exercise 11: Neural Architecture Search with DARTS

**Theory:** Explain how DARTS relaxes the discrete architecture search to a continuous optimization problem. What is the bilevel optimization formulation, and how are architecture weights trained alongside network weights?

**Coding:** Implement a simplified DARTS search space with 4 operations (identity, tanh, ReLU, sigmoid). Search for the best cell architecture on a synthetic regression task. Show how architecture weights evolve during training.

## Exercise 12: Reproduce a simple paper result

**Theory:** Describe the scientific method for reproducing ML results: what constitutes a successful reproduction? How do you handle missing hyperparameters or ambiguous experimental details in papers?

**Coding:** Find a recent ML paper with an open-source implementation and a clear, simple result (e.g., "Mamba outperforms Transformer on long-range arena tasks with sequence length 4096"). Reproduce the core experiment at smaller scale, document discrepancies, and report whether the trend matches.

## Exercise 13: Energy-Based Models (EBMs)

**Theory:** Explain how EBMs define a probability distribution through an energy function and the Boltzmann distribution. Why is the partition function intractable, and how do contrastive divergence and score matching address this?

**Coding:** Implement contrastive divergence to train an EBM on 2D data from a mixture of Gaussians. Sample from the learned model using Langevin dynamics. Visualize the learned energy landscape.

## Exercise 14: GAN with Gradient Penalty (WGAN-GP)

**Theory:** Derive the Wasserstein-1 distance and explain why the Lipschitz constraint is necessary for the WGAN objective. Why is gradient penalty preferred over weight clipping for enforcing the Lipschitz constraint?

**Coding:** Implement a WGAN-GP on a 2D dataset (8 Gaussian modes arranged in a circle). Train the generator and discriminator, track the Wasserstein distance estimate, and visualize generated samples.

## Bonus Challenge: Implement a hybrid SSM-Attention model

Implement a Jamba-style hybrid model that interleaves Mamba layers and attention layers. Compare perplexity vs sequence length for pure attention, pure SSM, and hybrid variants on a character-level language modeling task.

**Theory:** Discuss the trade-offs: attention provides unbounded context but quadratic cost; SSMs offer linear scaling but limited recall. How does the hybrid approach balance these?
