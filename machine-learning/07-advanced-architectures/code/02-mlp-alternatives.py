"""
07.02 MLP-Mixer & gMLP minimal implementations.
"""
import numpy as np
import matplotlib.pyplot as plt


def gelu(x):
    return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3)))


class MLPMixerLayer:
    def __init__(self, num_patches, hidden_dim, mlp_ratio=4):
        self.norm1_scale = np.ones(hidden_dim)
        self.norm1_bias = np.zeros(hidden_dim)
        self.token_mix_fc1 = np.random.randn(num_patches, mlp_ratio * num_patches) * 0.02
        self.token_mix_fc2 = np.random.randn(mlp_ratio * num_patches, num_patches) * 0.02
        self.norm2_scale = np.ones(hidden_dim)
        self.norm2_bias = np.zeros(hidden_dim)
        self.channel_mix_fc1 = np.random.randn(hidden_dim, mlp_ratio * hidden_dim) * 0.02
        self.channel_mix_fc2 = np.random.randn(mlp_ratio * hidden_dim, hidden_dim) * 0.02

    def layer_norm(self, x, scale, bias):
        mean = x.mean(axis=-1, keepdims=True)
        var = x.var(axis=-1, keepdims=True) + 1e-5
        return scale * (x - mean) / np.sqrt(var) + bias

    def forward(self, x):
        residual = x
        x = self.layer_norm(x, self.norm1_scale, self.norm1_bias)
        x = x @ self.token_mix_fc1
        x = gelu(x)
        x = x @ self.token_mix_fc2
        x = residual + x
        residual = x
        x = self.layer_norm(x, self.norm2_scale, self.norm2_bias)
        x = x @ self.channel_mix_fc1
        x = gelu(x)
        x = x @ self.channel_mix_fc2
        x = residual + x
        return x


class gMLPLayer:
    def __init__(self, d_model, d_ffn, seq_len):
        self.norm_scale = np.ones(d_model)
        self.norm_bias = np.zeros(d_model)
        self.fc_in = np.random.randn(d_model, d_ffn) * 0.02
        self.sgu_proj = np.random.randn(seq_len, seq_len) * 0.02
        self.fc_out = np.random.randn(d_ffn, d_model) * 0.02

    def layer_norm(self, x, scale, bias):
        mean = x.mean(axis=-1, keepdims=True)
        var = x.var(axis=-1, keepdims=True) + 1e-5
        return scale * (x - mean) / np.sqrt(var) + bias

    def forward(self, x):
        residual = x
        x = self.layer_norm(x, self.norm_scale, self.norm_bias)
        x = x @ self.fc_in
        u, v = np.split(x, 2, axis=-1)
        v = v @ self.sgu_proj
        x = u * v
        x = gelu(x)  # gating activation
        x = x @ self.fc_out
        return residual + x


if __name__ == "__main__":
    np.random.seed(42)
    batch, patches, dim = 4, 16, 32
    x = np.random.randn(batch, patches, dim)
    mixer = MLPMixerLayer(patches, dim)
    out_mixer = mixer.forward(x)
    print(f"MLP-Mixer: {x.shape} -> {out_mixer.shape}")

    gmlp = gMLPLayer(dim, dim * 2, patches)
    out_gmlp = gmlp.forward(x)
    print(f"gMLP:      {x.shape} -> {out_gmlp.shape}")

    x_val = np.linspace(-3, 3, 100)
    plt.plot(x_val, gelu(x_val), label='GELU')
    plt.grid(True)
    plt.legend()
    plt.title('GELU activation (used in MLP-mixer/gMLP)')
    plt.savefig('../../assets/phase07/mlp_alternatives.png')
    plt.close()
    print("Saved mlp_alternatives.png")
