"""LSTM and GRU — advanced recurrent networks."""
import torch
import torch.nn as nn


print("=== LSTM & GRU ===\n")

seq_len, batch_size, input_size, hidden_size = 10, 4, 8, 16
x = torch.randn(seq_len, batch_size, input_size)
print(f"Input shape: {x.shape}")

lstm = nn.LSTM(input_size, hidden_size, batch_first=False)
lstm_out, (lstm_h, lstm_c) = lstm(x)
print(f"LSTM(8 → 16):")
print(f"  Output shape: {lstm_out.shape}")
print(f"  Hidden h: {lstm_h.shape}, Cell c: {lstm_c.shape}")

gru = nn.GRU(input_size, hidden_size, batch_first=False)
gru_out, gru_h = gru(x)
print(f"\nGRU(8 → 16):")
print(f"  Output shape: {gru_out.shape}")
print(f"  Hidden shape: {gru_h.shape}")

print(f"\nStacked LSTM (2 layers):")
stacked = nn.LSTM(input_size, hidden_size, num_layers=2, dropout=0.2, batch_first=True)
x_bf = torch.randn(batch_size, seq_len, input_size)
out, (h, c) = stacked(x_bf)
print(f"  Output shape: {out.shape}")
print(f"  Hidden shape: {h.shape} (2 layers)")

print(f"\nLSTM params: {sum(p.numel() for p in lstm.parameters()):,}")
print(f"GRU params:  {sum(p.numel() for p in gru.parameters()):,}")
print("\nGRU has fewer params (no cell state) but similar performance.")
