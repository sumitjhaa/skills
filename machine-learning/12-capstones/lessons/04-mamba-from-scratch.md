# Lesson 12.04: Mamba from Scratch + Transformer Comparison

## Project Architecture

Implement the Mamba state-space model (SSM) block from Gu & Dao (2023), train it on a language modeling task, and compare perplexity/efficiency against an equivalent-size transformer.

```
Mamba Block
├── Linear projection (input → 2×D)
├── 1D Convolution (depthwise, causal)
├── SiLU activation
├── SSM Layer (discretized continuous SSM)
│    ├── Discretization: Δ, A, B, C matrices
│    ├── Scan: h_t = A̅ h_{t-1} + B̅ x_t
│    │        y_t = C h_t
│    └── Fast associative scan (parallel)
├── Gate (SiLU on the other branch)
├── Linear projection (D → output)
└── Residual connection

vs.

Transformer Block
├── Multi-Head Attention (O(n²) complexity)
├── Feed-Forward Network
└── Residual + LayerNorm
```

## Design Decisions

### SSM discretization
- Continuous SSM: h' = Ah + Bx, y = Ch
- Discretized with zero-order hold: A̅ = exp(ΔA), B̅ = (ΔA)⁻¹(exp(ΔA) - I) ΔB
- Simplified: A̅ = I + ΔA, B̅ = ΔB (Euler approximation)

### Selective scan
- Parameters Δ, B, C are input-dependent (this is the key Mamba innovation)
- This lets the model "select" which tokens to remember vs. ignore
- Use a parallel associative scan (Hiller's algorithm) for O(n log n) training

### Architecture
- Mamba block: no attention, purely recurrent with parallel training
- Stack M blocks, each with residual connections
- LayerNorm before each block
- Final LayerNorm + LM head

### Comparison metrics
- Perplexity on validation set (same data, same vocab)
- Training speed (tokens/second)
- Memory usage
- Sequence length scaling (wall-clock vs. length)

## Implementation Guide

1. **Implement the selective scan** (parallel prefix sum algorithm)
2. **Implement SSM discretization** (Δ, A, B, C → A̅, B̅)
3. **Implement the SSM layer** (forward pass with scan)
4. **Implement the full Mamba block** (conv + SSM + gating + residual)
5. **Implement the full Mamba model** (stacked blocks + LM head)
6. **Implement the transformer baseline** (same param count)
7. **Train both on a text corpus**
8. **Compare: perplexity, speed, memory, length scaling**
9. **Plot comparative results**

## Key Insights

- Mamba's selective mechanism is what makes it outperform linear attention
- The parallel scan makes training efficient despite the recurrence
- Mamba has O(n) inference vs. transformer's O(n²)
- At small scale, transformers may win; at large scale, Mamba shines
- The convolution before the SSM adds local context processing
