# 06.22 RNN / LSTM / GRU

Recurrent networks process sequences by maintaining a hidden state updated at each time step.

## Vanilla RNN

h_t = tanh(W_h · h_{t-1} + W_x · x_t + b)

Simple but suffers from vanishing/exploding gradients. Can't capture long-range dependencies.

## LSTM (Long Short-Term Memory)

Three gates control information flow:

- **Forget gate**: f_t = σ(W_f · [h_{t-1}, x_t] + b_f)
- **Input gate**: i_t = σ(W_i · [h_{t-1}, x_t] + b_i)
- **Output gate**: o_t = σ(W_o · [h_{t-1}, x_t] + b_o)
- **Cell update**: c̃_t = tanh(W_c · [h_{t-1}, x_t] + b_c)
- **Cell state**: c_t = f_t ⊙ c_{t-1} + i_t ⊙ c̃_t
- **Hidden state**: h_t = o_t ⊙ tanh(c_t)

The cell state c_t acts as a gradient highway — information flows through with only element-wise multiplication, preventing vanishing gradients.

## GRU (Gated Recurrent Unit)

Simplified LSTM with two gates:

- **Reset gate**: r_t = σ(W_r · [h_{t-1}, x_t] + b_r)
- **Update gate**: z_t = σ(W_z · [h_{t-1}, x_t] + b_z)
- **New hidden**: h̃_t = tanh(W_h · [r_t ⊙ h_{t-1}, x_t] + b_h)
- **Hidden state**: h_t = (1 - z_t) ⊙ h_{t-1} + z_t ⊙ h̃_t

Fewer parameters than LSTM. Often comparable performance.

## Comparison

| Cell | Parameters | Gates | Vanishing Grad | Complexity |
|------|-----------|-------|----------------|------------|
| RNN | 3·d² | 0 | Severe | O(d²) |
| LSTM | 4·d² | 3 | Mitigated | O(4d²) |
| GRU | 3·d² | 2 | Mitigated | O(3d²) |

## Bidirectional RNN

Process sequence forward and backward, concatenate hidden states:

h_t = [h_t^fwd; h_t^bwd]

Accesses both past and future context. Used in BERT, ELMo.

## Stacked RNNs

Multiple RNN layers where h^{l}_t feeds into h^{l+1}_t. Increases model capacity.
