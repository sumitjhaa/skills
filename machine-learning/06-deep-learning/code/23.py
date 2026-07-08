"""06.23 - Seq2Seq: Encoder-decoder with attention"""

import numpy as np


def softmax(x, axis=-1):
    e_x = np.exp(x - x.max(axis=axis, keepdims=True))
    return e_x / e_x.sum(axis=axis, keepdims=True)


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
        f = 1 / (1 + np.exp(-(z @ self.Wf + self.bf)))
        i = 1 / (1 + np.exp(-(z @ self.Wi + self.bi)))
        o = 1 / (1 + np.exp(-(z @ self.Wo + self.bo)))
        c_tilde = np.tanh(z @ self.Wc + self.bc)
        c = f * c_prev + i * c_tilde
        h = o * np.tanh(c)
        return h, (h, c)


class Attention:
    def __init__(self, hidden_size):
        self.W_a = np.random.randn(hidden_size, hidden_size) * 0.01
        self.U_a = np.random.randn(hidden_size, hidden_size) * 0.01
        self.v_a = np.random.randn(hidden_size) * 0.01

    def forward(self, h_decoder, encoder_outputs):
        scores = []
        for h_enc in encoder_outputs:
            score = self.v_a @ np.tanh(self.W_a @ h_decoder + self.U_a @ h_enc)
            scores.append(score)
        weights = softmax(np.array(scores))
        context = np.sum(weights[:, None] * np.array(encoder_outputs), axis=0)
        return context, weights


class Seq2Seq:
    def __init__(self, input_size, hidden_size, output_size):
        self.encoder = LSTMCell(input_size, hidden_size)
        self.decoder = LSTMCell(output_size, hidden_size)
        self.attention = Attention(hidden_size)
        self.W_out = np.random.randn(hidden_size * 2, output_size) * 0.01
        self.b_out = np.zeros(output_size)

    def encode(self, inputs):
        h, c = np.zeros(self.encoder.Wf.shape[1]), np.zeros(self.encoder.Wf.shape[1])
        states = []
        for x in inputs:
            h, (h, c) = self.encoder.forward(x, (h, c))
            states.append(h)
        return states, (h, c)

    def decode_step(self, x, h, c, encoder_outputs):
        h, (h, c) = self.decoder.forward(x, (h, c))
        context, weights = self.attention.forward(h, encoder_outputs)
        combined = np.concatenate([h, context])
        y = combined @ self.W_out + self.b_out
        return y, (h, c), weights

    def forward(self, inputs, targets=None, teacher_forcing=True):
        encoder_outputs, (h, c) = self.encode(inputs)
        if targets is not None and teacher_forcing:
            outputs = []
            for t in range(len(targets)):
                x = targets[t] if t > 0 else np.zeros(self.W_out.shape[1])
                y, (h, c), _ = self.decode_step(x, h, c, encoder_outputs)
                outputs.append(y)
            return np.array(outputs)
        else:
            outputs = []
            x = np.zeros(self.W_out.shape[1])
            for t in range(10):
                y, (h, c), _ = self.decode_step(x, h, c, encoder_outputs)
                outputs.append(y)
                x = y
            return np.array(outputs)


if __name__ == "__main__":
    np.random.seed(42)
    model = Seq2Seq(8, 32, 8)
    src = [np.random.randn(8) for _ in range(5)]
    tgt = [np.random.randn(8) for _ in range(7)]

    out_teacher = model.forward(src, targets=tgt, teacher_forcing=True)
    out_free = model.forward(src, teacher_forcing=False)

    print(f"Source length: {len(src)}")
    print(f"Target length: {len(tgt)}")
    print(f"Teacher forcing output: {out_teacher.shape}")
    print(f"Free generation output: {out_free.shape}")

    print(f"\nSample attention weights:")
    _, _, weights = model.decode_step(tgt[0], np.zeros(32), np.zeros(32),
                                       [np.random.randn(32) for _ in range(5)])
    print(f"  Attention over {len(weights)} encoder states: {np.round(weights, 3)}")

    print("\nSeq2Seq with attention implemented and tested.")
