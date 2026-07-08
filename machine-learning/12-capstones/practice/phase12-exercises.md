# Phase 12: Practice Exercises

## Extension & Improvement Projects

These exercises extend the 11 capstone projects with additional features, optimizations, and analysis.

---

### Exercise 1: Autograd — Higher-Order Gradients (12.01)

Extend the autograd engine to support higher-order gradients (Hessian-vector products).

**Tasks:**
1. Store the backward graph for the backward pass itself (double backprop)
2. Implement `grad(grad_fn)` to compute second derivatives
3. Test on `f(x) = x^3` at x=2 (should get 12 for second derivative)
4. Use Hessian-vector product for a neural network curvature estimate

**Starter:**
```python
# In your Tensor, add a _backward_graph attribute
# Modify backward() to record operations on gradients
class Tensor:
    def backward(self, retain_graph=False):
        # After computing gradients, store them for potential second-order
        if retain_graph:
            # Don't clear the graph
            pass
```

---

### Exercise 2: Transformer — Flash Attention Simulation (12.02)

Implement a simplified version of Flash Attention that processes attention in blocks to reduce memory.

**Tasks:**
1. Split Q, K, V into blocks along the sequence dimension
2. For each block, compute local attention scores
3. Use online softmax to combine block results correctly
4. Compare memory usage vs. standard attention

**Key insight:** Flash Attention avoids materializing the full T×T attention matrix.

---

### Exercise 3: Diffusion Model — Classifier-Free Guidance (12.03)

Add classifier-free guidance (CFG) to the diffusion model for conditional generation.

**Tasks:**
1. Modify the U-Net to accept conditioning (e.g., class labels)
2. Train with both conditioned and unconditioned paths (drop conditioning 10% of the time)
3. Implement CFG sampling: `ε_θ = ε_θ_uncond + w * (ε_θ_cond - ε_θ_uncond)`
4. Test with different guidance scales (w = 1.0, 3.0, 7.0)
5. Analyze the trade-off between sample quality and diversity

---

### Exercise 4: Mamba — Gated Scan Variant (12.04)

Implement a gated variant of the selective scan that uses a learned gate to control information flow.

**Tasks:**
1. Add a sigmoid gating mechanism to the SSM recurrence
2. Compare: vanilla scan vs. gated scan on a synthetic memorization task
3. Measure: does gating improve long-range dependency handling?
4. Test on the Copying Task (standard benchmark for recurrence)

**Key equations:**
```
Standard:   h_t = A_bar * h_{t-1} + B_bar * x_t
Gated:      g_t = sigmoid(W_g * x_t + b_g)
            h_t = g_t * (A_bar * h_{t-1} + B_bar * x_t) + (1 - g_t) * h_{t-1}
```

---

### Exercise 5: RLHF — Reward Model Ensembling (12.05)

Improve RLHF by using an ensemble of reward models with uncertainty estimation.

**Tasks:**
1. Train 3-5 reward models with different random seeds
2. Use the ensemble mean as the reward signal
3. Use the ensemble variance as an uncertainty estimate
4. Implement uncertainty-weighted PPO (lower weight for high-uncertainty samples)
5. Compare: single reward model vs. ensemble

**Hypothesis:** Ensemble rewards produce more robust alignment with less reward hacking.

---

### Exercise 6: RAG — Hybrid Search with Learned Weights (12.06)

Improve RAG retrieval by learning to weight dense vs. sparse retrieval signals.

**Tasks:**
1. Implement both dense (embeddings) and sparse (BM25-style) retrieval
2. Learn a weighting parameter `α` per query: `score = α * dense + (1-α) * sparse`
3. Use a small MLP to predict `α` from query features
4. Train the MLP to maximize retrieval recall@5
5. Compare: hybrid vs. pure dense vs. pure sparse

**Data:** Use the existing QA pairs with relevance judgments.

---

### Exercise 7: Distributed Training — Communication-Computation Overlap (12.07)

Implement overlapping of communication (AllGather/ReduceScatter) with forward/backward computation.

**Tasks:**
1. Split each layer into chunks
2. While computing layer i, start communicating parameters for layer i+1
3. Implement a simple double-buffering scheme
4. Measure the wall-clock speedup vs. synchronous FSDP
5. Plot: overlap efficiency vs. model size

**Challenge:** Real overlap requires CUDA streams; simulate with threading on CPU.

---

### Exercise 8: AutoML — Neural Architecture Search (12.08)

Add a simple NAS component to the AutoML system using evolutionary search.

**Tasks:**
1. Define a search space: number of layers [1-5], hidden dims [32-256], activation [relu, gelu, tanh]
2. Implement population-based evolution: tournament selection, mutation, crossover
3. Use weight inheritance (warm-start from parent weights)
4. Compare: NAS vs. HPO-only on the same datasets
5. Plot: Pareto frontier of accuracy vs. model size

---

### Exercise 9: Monitoring — Root Cause Analysis (12.09)

Build a root cause analysis system that identifies which features are driving detected drift.

**Tasks:**
1. When PSI exceeds threshold, compute per-feature contribution to the total PSI
2. Rank features by their individual PSI contribution
3. For the top-3 drifted features, compute the feature Attribution score
4. Generate a "drift report" with feature-level analysis
5. Test with selective feature drift (drift only features 1, 3, 5)

**Output example:**
```
Drift detected at batch 22 (PSI=0.35)
Top contributors:
  Feature 0: PSI=0.18 (51.4%) — SHIFT: mean +1.2, std +0.8
  Feature 2: PSI=0.10 (28.6%) — SHIFT: distribution type changed
  Feature 4: PSI=0.05 (14.3%) — SHIFT: increased tail weight
```

---

### Exercise 10: Novel Contribution — Library Packaging (12.11)

Take the adaptive checkpointing system and package it as a proper open-source library.

**Tasks:**
1. Create a `pyproject.toml` with dependencies, metadata, and entry points
2. Organize the code into modules: `adaptive_ckpt/core.py`, `adaptive_ckpt/policy.py`, `adaptive_ckpt/models.py`
3. Write unit tests (>80% coverage) for the checkpointing policy
4. Create a Colab notebook demonstrating the library
5. Add type hints and docstrings to all public APIs
6. Write a README.md with installation, usage, and benchmarks

**Bonus:** Publish to TestPyPI.

---

## Submission Guidelines

For each exercise:
- Include the modified/exended code
- Show before/after metrics (where applicable)
- Write a brief analysis (3-5 sentences) of what you learned

## Grading Rubric

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Correctness | 30% | Implementation produces correct results |
| Analysis | 25% | Thoughtful analysis of results and trade-offs |
| Code quality | 20% | Clean, well-structured, idiomatic code |
| Extension | 15% | Goes beyond minimum requirements |
| Reproducibility | 10% | Others can run and verify results |
