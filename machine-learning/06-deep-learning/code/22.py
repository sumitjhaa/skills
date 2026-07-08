"""06.22 - RNN / LSTM / GRU: Recurrent cells from scratch"""

import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -100, 100)))

def tanh(x):
    return np.tanh(x)


class RNNCell:
    def __init__(self, input_size, hidden_size):
        self.Wxh = np.random.randn(input_size, hidden_size) * 0.01
        self.Whh = np.random.randn(hidden_size, hidden_size) * 0.01
        self.bh = np.zeros(hidden_size)

    def forward(self, x, h_prev):
        return tanh(x @ self.Wxh + h_prev @ self.Whh + self.bh)


class LSTMCell:
    def __init__(self, input_size, hidden_size):
        d = hidden_size
        self.Wf = np.random.randn(input_size + d, d) * 0.01
        self.Wi = np.random.randn(input_size + d, d) * 0.01
        self.Wo = np.random.randn(input_size + d, d) * 0.01
        self.Wc = np.random.randn(input_size + d, d) * 0.01
        self.bf, self.bi, self.bo, self.bc = np.zeros(d), np.zeros(d), np.zeros(d), np.zeros(d)

    def forward(self, x, state):
        h_prev, c_prev = state
        z = np.concatenate([x, h_prev])
        f = sigmoid(z @ self.Wf + self.bf)
        i = sigmoid(z @ self.Wi + self.bi)
        o = sigmoid(z @ self.Wo + self.bo)
        c_tilde = tanh(z @ self.Wc + self.bc)
        c = f * c_prev + i * c_tilde
        h = o * tanh(c)
        return h, (h, c)


class GRUCell:
    def __init__(self, input_size, hidden_size):
        d = hidden_size
        self.Wz = np.random.randn(input_size + d, d) * 0.01
        self.Wr = np.random.randn(input_size + d, d) * 0.01
        self.Wh = np.random.randn(input_size + d, d) * 0.01
        self.bz, self.br, self.bh = np.zeros(d), np.zeros(d), np.zeros(d)

    def forward(self, x, h_prev):
        z = np.concatenate([x, h_prev])
        z_gate = sigmoid(z @ self.Wz + self.bz)
        r_gate = sigmoid(z @ self.Wr + self.br)
        z_reset = np.concatenate([x, r_gate * h_prev])
        h_tilde = tanh(z_reset @ self.Wh + self.bh)
        h = (1 - z_gate) * h_prev + z_gate * h_tilde
        return h


class BidirectionalRNN:
    def __init__(self, input_size, hidden_size):
        self.fwd = LSTMCell(input_size, hidden_size)
        self.bwd = LSTMCell(input_size, hidden_size)

    def forward(self, inputs):
        T = len(inputs)
        h_fwd = np.zeros(self.fwd.Wf.shape[1])
        c_fwd = np.zeros_like(h_fwd)
        fwd_states = []
        for t in range(T):
            h_fwd, (h_fwd, c_fwd) = self.fwd.forward(inputs[t], (h_fwd, c_fwd))
            fwd_states.append(h_fwd)

        h_bwd = np.zeros(self.bwd.Wf.shape[1])
        c_bwd = np.zeros_like(h_bwd)
        bwd_states = []
        for t in range(T - 1, -1, -1):
            h_bwd, (h_bwd, c_bwd) = self.bwd.forward(inputs[t], (h_bwd, c_bwd))
            bwd_states.append(h_bwd)
        bwd_states.reverse()

        return [np.concatenate([f, b]) for f, b in zip(fwd_states, bwd_states)]


if __name__ == "__main__":
    np.random.seed(42)
    input_size, hidden_size = 8, 16

    rnn = RNNCell(input_size, hidden_size)
    lstm = LSTMCell(input_size, hidden_size)
    gru = GRUCell(input_size, hidden_size)

    x = np.random.randn(input_size)
    h = np.zeros(hidden_size)

    h_rnn = rnn.forward(x, h)
    h_lstm, state_lstm = lstm.forward(x, (h, h))
    h_gru = gru.forward(x, h)

    print(f"RNN  cell:  h shape = {h_rnn.shape}")
    print(f"LSTM cell:  h shape = {h_lstm.shape}, c shape = {state_lstm[1].shape}")
    print(f"GRU  cell:  h shape = {h_gru.shape}")

    birnn = BidirectionalRNN(input_size, hidden_size)
    seq = [np.random.randn(input_size) for _ in range(5)]
    bi_states = birnn.forward(seq)
    print(f"\nBidirectional RNN: 5 timesteps, hidden dim = {bi_states[0].shape} (2x{hidden_size})")

    T = 10
    x_seq = [np.random.randn(input_size) for _ in range(T)]
    h, c = np.zeros(hidden_size), np.zeros(hidden_size)
    for t in range(T):
        h, (h, c) = lstm.forward(x_seq[t], (h, c))
        if t < 3 or t >= T - 1:
            print(f"  t={t}: |h|={np.linalg.norm(h):.4f}, |c|={np.linalg.norm(c):.4f}")

    print("\nAll recurrent cells implemented and tested.")
