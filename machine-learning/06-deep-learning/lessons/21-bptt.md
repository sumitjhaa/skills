# 06.21 BPTT (Backpropagation Through Time)

BPTT applies backpropagation to recurrent neural networks by unrolling the computation graph through time steps.

## Unrolling

An RNN for T time steps is equivalent to a T-layer feedforward network where each layer shares the same weights:

```
h_t = tanh(W_h · h_{t-1} + W_x · x_t + b)
y_t = W_y · h_t + b_y
```

Unrolled:
```
x₁ → h₁ → x₂ → h₂ → ... → x_T → h_T
     ↓           ↓               ↓
     y₁          y₂              y_T
```

## Forward Pass (Unrolled)

For t = 1 to T:
1. Compute h_t from x_t and h_{t-1}
2. Store all h_t for backward pass
3. Compute loss at each step (or final step)

## Backward Pass

Process T steps in reverse:

∂L/∂h_t = ∂L_t/∂h_t + ∂L/∂h_{t+1} · ∂h_{t+1}/∂h_t

Gradient flows through time — and through the same W_h matrix at each step.

## Vanishing/Exploding Gradients

The repeated multiplication by W_h causes:

- **Vanishing**: ||W_h|| < 1 → gradients decay to 0
- **Exploding**: ||W_h|| > 1 → gradients grow exponentially

Truncated BPTT: limit backprop to K steps to control this.

## Truncated BPTT

1. Process T steps forward
2. Backpropagate only K steps back
3. Carry hidden state forward (detach gradients)

## Computational Cost

- Memory: O(T · hidden_size) — all hidden states stored
- Time: O(T) forward + O(T) backward

## Gradient Clipping

Essential for RNN training. Clip gradient norm to a maximum value (e.g., 5.0).
