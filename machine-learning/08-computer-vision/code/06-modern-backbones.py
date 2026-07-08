"""08.06 Modern backbones: ConvNeXt, RegNet, VAN."""
import numpy as np
import matplotlib.pyplot as plt

class ConvNeXtBlock:
    def __init__(self, dim, kernel_size=7, expand_ratio=4):
        self.dim = dim
        self.kernel_size = kernel_size
        self.expand_ratio = expand_ratio
        self.params = (dim * kernel_size * kernel_size +
                       dim * dim * expand_ratio * 1 * 1 +
                       dim * dim * expand_ratio * 1 * 1)

    def params_convnext(self):
        return self.params

    def params_resnet(self):
        return 2 * self.dim * self.dim * 3 * 3 + self.dim * self.dim * 3 * 3

kernel_sizes = [3, 5, 7, 9, 11, 13]
dim = 256
params_k = [ConvNeXtBlock(dim, k).params_convnext() for k in kernel_sizes]
params_resnet = dim * dim * 3 * 3 + 2 * dim * dim * 3 * 3

ratios_exp = []
for e in [2, 3, 4, 6, 8]:
    ratios_exp.append(ConvNeXtBlock(dim, 7, e).params_convnext())

dimensions = [64, 128, 256, 384, 512]
flops_stage = []
for d in dimensions:
    conv = ConvNeXtBlock(d)
    resnet_conv = dim * dim * 3 * 3 + 2 * dim * dim * 3 * 3
    flops_stage.append(conv.params / (d * d))

n_blocks = [3, 3, 9, 3]
dims_stage = [96, 192, 384, 768]
total_params = sum(ConvNeXtBlock(dims_stage[i]).params * n_blocks[i]
                   for i in range(4))

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].bar(kernel_sizes, params_k, alpha=0.7)
axes[0, 0].axhline(params_resnet, color="r", ls="--", lw=2,
                   label=f"ResNet bottleneck ({params_resnet:,})")
axes[0, 0].set_xlabel("Kernel size")
axes[0, 0].set_ylabel("Parameters per block")
axes[0, 0].set_title("ConvNeXt: Params vs Kernel Size\n(dim=256)")
axes[0, 0].legend()
axes[0, 0].grid(True, axis="y", alpha=0.3)

stages_labels = ["Stem", "S1", "S2", "S3", "S4"]
stages_params = [dims_stage[0]*dims_stage[0]//2] + \
                [ConvNeXtBlock(dims_stage[i]).params * n_blocks[i]
                 for i in range(4)]
axes[0, 1].bar(stages_labels, stages_params, color="steelblue", alpha=0.7)
axes[0, 1].set_ylabel("Parameters")
axes[0, 1].set_title(f"ConvNeXt-T: Stage Params\nTotal ≈ {total_params:,}")
axes[0, 1].grid(True, axis="y", alpha=0.3)

expand_opts = [2, 3, 4, 6, 8]
axes[0, 2].plot(expand_opts, ratios_exp, "o-", lw=2)
axes[0, 2].set_xlabel("Expand ratio")
axes[0, 2].set_ylabel("Parameters per block")
axes[0, 2].set_title("ConvNeXt: Params vs Expand\nRatio (dim=256)")
axes[0, 2].grid(True, alpha=0.3)

regnet_depths = np.arange(10, 50, 5)
regnet_params = [d * d * 3 * 3 * 4 + d * d * 1 * 1 * 2 for d in 64 * (regnet_depths / 30)]
regnet_flops = [p * 14 * 14 for p in regnet_params]
axes[1, 0].plot(regnet_depths, np.array(regnet_params) / 1e6, "o-", lw=2)
axes[1, 0].set_xlabel("Depth (layers)")
axes[1, 0].set_ylabel("Parameters (M)")
axes[1, 0].set_title("RegNet: Params vs Depth")
axes[1, 0].grid(True, alpha=0.3)

dims = np.linspace(32, 512, 50)
linear_ratio = (dims * 7 * 7 + dims * 4 * dims * 1 * 1 + dims * 4 * dims * 1 * 1)
conv_ratio = (dims * 3 * 3 + dims * dims * 1 * 1 * 2)
total_vs_se = linear_ratio + conv_ratio
total_no_se = conv_ratio
axes[1, 1].plot(dims, total_vs_se / 1e6, "b-", lw=2, label="With SE")
axes[1, 1].plot(dims, total_no_se / 1e6, "r--", lw=2, label="Without SE")
axes[1, 1].set_xlabel("Channel dimension")
axes[1, 1].set_ylabel("Parameters (M)")
axes[1, 1].set_title("Effect of Squeeze-and-Excitation")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

models = ["ResNet-50\n25.6M", "ConvNeXt-T\n28.6M", "RegNetY-4G\n21.0M",
          "EfficientNet-B3\n12.0M", "VAN-B2\n26.0M"]
top1 = [76.0, 78.3, 78.4, 77.5, 78.1]
params_m = [25.6, 28.6, 21.0, 12.0, 26.0]
sc = axes[1, 2].scatter(params_m, top1, s=100, c=range(len(models)), cmap="viridis")
for i, m in enumerate(models):
    axes[1, 2].annotate(m.split("\n")[0], (params_m[i], top1[i]),
                        textcoords="offset points", xytext=(5, 5), fontsize=8)
axes[1, 2].set_xlabel("Parameters (M)")
axes[1, 2].set_ylabel("Top-1 acc (ImageNet)")
axes[1, 2].set_title("Efficiency Comparison")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase08/06-modern-backbones.png")
plt.close()

print("=" * 60)
print("MODERN BACKBONES: ConvNeXt, RegNet, VAN")
print("=" * 60)
print(f"\nConvNeXt Block (dim=256, k=7, expand=4):")
tmp = ConvNeXtBlock(256, 7, 4)
print(f"  Parameters: {tmp.params_convnext():,}")
tmp_res = dim * dim * 3 * 3 + 2 * dim * dim * 3 * 3
print(f"  ResNet bottleneck equivalent: {tmp_res:,}")

print(f"\nConvNeXt-Tiny total: ≈{total_params:,} parameters")
print(f"  Stage breakdown:")
for i in range(4):
    stage_p = ConvNeXtBlock(dims_stage[i]).params * n_blocks[i]
    print(f"    Stage {i+1} ({dims_stage[i]}dim, {n_blocks[i]} blocks): {stage_p:,}")

print(f"\nDesign improvements over ResNet:")
print(f"  • 7×7 depthwise conv (large kernel)")
print(f"  • LayerNorm instead of BatchNorm")
print(f"  • GELU activation instead of ReLU")
print(f"  • Inverted bottleneck (expand→project)")
print(f"  • Fewer activation and normalization layers")
print(f"  • Patchify stem (non-overlapping 4×4 conv)")
