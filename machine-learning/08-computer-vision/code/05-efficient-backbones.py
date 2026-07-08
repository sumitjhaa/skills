"""08.05 Efficient backbones: MobileNet, ShuffleNet, EfficientNet."""
import numpy as np
import matplotlib.pyplot as plt

class DepthwiseSeparableConv:
    def __init__(self, in_channels, out_channels, kernel_size=3):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.params_depthwise = in_channels * kernel_size * kernel_size
        self.params_pointwise = in_channels * out_channels
        self.total_params = self.params_depthwise + self.params_pointwise

    def params_standard(self):
        return self.in_channels * self.out_channels * self.kernel_size * self.kernel_size

    def ratio(self):
        return self.total_params / self.params_standard()

def mbconv_params(in_c, out_c, expand_ratio=6, kernel_size=3):
    expanded_c = in_c * expand_ratio
    params = (in_c * expanded_c * 1 * 1 +
              expanded_c * kernel_size * kernel_size +
              expanded_c * out_c * 1 * 1)
    standard = in_c * out_c * kernel_size * kernel_size
    return params, standard

in_channels_list = [16, 32, 64, 128, 256]
ratios = []
for c in in_channels_list:
    conv = DepthwiseSeparableConv(c, c * 2)
    ratios.append(conv.ratio())

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].bar(range(len(in_channels_list)), ratios,
               tick_label=in_channels_list, alpha=0.7)
axes[0, 0].set_xlabel("Input channels")
axes[0, 0].set_ylabel("Parameter ratio\n(depthwise / standard)")
axes[0, 0].set_title("Depthwise Separable Conv\nParameter Efficiency")
axes[0, 0].grid(True, axis="y", alpha=0.3)

in_c = 64
out_c_list = [32, 64, 128, 256, 512]
mb_params, std_params = [], []
for o in out_c_list:
    p, s = mbconv_params(in_c, o, expand_ratio=6)
    mb_params.append(p)
    std_params.append(s)
axes[0, 1].plot(out_c_list, mb_params, "o-", lw=2, label="MBConv")
axes[0, 1].plot(out_c_list, std_params, "s--", lw=2, label="Standard Conv")
axes[0, 1].set_xlabel("Output channels")
axes[0, 1].set_ylabel("Parameters")
axes[0, 1].set_title("MBConv vs Standard Conv\nParameter Count")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

width_mult = np.linspace(0.25, 2.0, 20)
params_w = [(64 * w) * (128 * w) * 3 * 3 for w in width_mult]
flops_w = [(64 * w) * (128 * w) * 3 * 3 * 7 * 7 for w in width_mult]
axes[0, 2].plot(width_mult, params_w / params_w[0], "r-", lw=2, label="Params (rel)")
axes[0, 2].plot(width_mult, flops_w / flops_w[0], "b--", lw=2, label="FLOPs (rel)")
axes[0, 2].set_xlabel("Width multiplier α")
axes[0, 2].set_ylabel("Relative cost")
axes[0, 2].set_title("EfficientNet: Width Scaling")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

depths = np.arange(1, 10)
params_d = [d * 64 * 128 * 3 * 3 for d in depths]
flops_d = [d * 64 * 128 * 3 * 3 * 7 * 7 for d in depths]
axes[1, 0].plot(depths, params_d / params_d[0], "r-", lw=2, label="Params (rel)")
axes[1, 0].plot(depths, flops_d / flops_d[0], "b--", lw=2, label="FLOPs (rel)")
axes[1, 0].set_xlabel("Depth multiplier ϕ")
axes[1, 0].set_ylabel("Relative cost")
axes[1, 0].set_title("EfficientNet: Depth Scaling")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

resolutions = np.linspace(128, 512, 20, dtype=int)
params_r = [64 * 128 * 3 * 3 * (r/224)**2 for r in resolutions]
flops_r = [64 * 128 * 3 * 3 * r * r * 7 * 7 * (r/224)**2 * (r/224)**2 for r in resolutions]
axes[1, 1].plot(resolutions, params_r / params_r[0], "r-", lw=2, label="Params (rel)")
axes[1, 1].plot(resolutions, flops_r / flops_r[0], "b--", lw=2, label="FLOPs (rel)")
axes[1, 1].set_xlabel("Resolution r")
axes[1, 1].set_ylabel("Relative cost")
axes[1, 1].set_title("EfficientNet: Resolution Scaling")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

compound_scales = np.linspace(0, 2, 20)
ϕ = compound_scales
α, β, γ = 1.2, 1.1, 1.15
params_c = (α**ϕ) * (β**ϕ) * (γ**ϕ)
flops_c = (α**ϕ) * (β**ϕ) * (γ**ϕ)
for i, s in enumerate(compound_scales):
    w = α**s
    d = β**s
    r = γ**s
    params_c[i] = w * d * r
    flops_c[i] = w * d * r**2
axes[1, 2].plot(compound_scales, 64 * 128 * 3 * 3 * params_c, "o-", lw=2, label="Params")
axes[1, 2].plot(compound_scales, 64 * 128 * 3 * 3 * 7 * 7 * flops_c,
               "s--", lw=2, label="FLOPs")
axes[1, 2].set_xlabel("Compound coefficient ϕ")
axes[1, 2].set_ylabel("Relative cost")
axes[1, 2].set_title("EfficientNet: Compound Scaling")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase08/05-efficient-backbones.png")
plt.close()

print("=" * 60)
print("EFFICIENT BACKBONES")
print("=" * 60)
print(f"\nDepthwise Separable Conv (kernel=3, C_in=C_out=64):")
dsc = DepthwiseSeparableConv(64, 64)
std_params = dsc.params_standard()
print(f"  Standard: {std_params:,} params")
print(f"  Depthwise sep: {dsc.total_params:,} params")
print(f"  Ratio: {dsc.ratio():.4f}× (1/C_out + 1/k²)")

print(f"\nMBConv (MobileNetV2-style):")
for o in out_c_list:
    p, s = mbconv_params(64, o)
    print(f"  {64}→{o}: MBConv={p:,}, Standard={s:,}, ratio={p/s:.3f}")

print(f"\nEfficientNet scaling (φ=1):")
print(f"  Width: α^φ = {1.2**1:.2f}")
print(f"  Depth: β^φ = {1.1**1:.2f}")
print(f"  Resolution: γ^φ = {1.15**1:.2f}")

print(f"\nKey architectures:")
print(f"  • MobileNetV1: depthwise separable conv")
print(f"  • MobileNetV2: inverted residuals + linear bottlenecks")
print(f"  • ShuffleNet: channel shuffle + group conv")
print(f"  • EfficientNet: compound scaling (d·w²·r² ~ FLOPS)")
