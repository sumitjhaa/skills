"""RNN basics — simple recurrent network for sequence data."""
import torch
import torch.nn as nn


print("=== RNN Basics ===\n")

seq_len, batch_size, input_size, hidden_size = 10, 4, 8, 16
x = torch.randn(seq_len, batch_size, input_size)
print(f"Input shape (seq, batch, features): {x.shape}")

rnn = nn.RNN(input_size, hidden_size, batch_first=False)
out, h_n = rnn(x)
print(f"\nnn.RNN(8 → 16):")
print(f"  Output shape: {out.shape}")
print(f"  Hidden shape: {h_n.shape}")

rnn_batch_first = nn.RNN(input_size, hidden_size, batch_first=True)
x_bf = torch.randn(batch_size, seq_len, input_size)
out_bf, h_bf = rnn_batch_first(x_bf)
print(f"\nnn.RNN (batch_first=True):")
print(f"  Input shape:  {x_bf.shape}")
print(f"  Output shape: {out_bf.shape}")
print(f"  Hidden shape: {h_bf.shape}")

print(f"\nnn.RNN parameters: {sum(p.numel() for p in rnn.parameters()):,}")

print("\nTypical RNN usage: last hidden state → classifier")
classifier = nn.Linear(hidden_size, 1)
logits = classifier(out[-1])
print(f"  Classifier input: {out[-1].shape}")
print(f"  Classifier output: {logits.shape}")
