# 06.24 CNN Backbones

CNN backbones are the feature extraction foundation for computer vision.

## LeNet-5 (1998)

Layers: Conv(6@5x5) → AvgPool → Conv(16@5x5) → AvgPool → FC(120) → FC(84) → Output(10)

First successful CNN. Used for digit recognition (MNIST). 60K parameters.

## AlexNet (2012)

Conv(96@11x4) → MaxPool → Conv(256@5x5) → MaxPool → Conv(384@3x3) → Conv(384@3x3) → Conv(256@3x3) → MaxPool → FC(4096) → FC(4096) → Output(1000)

First deep CNN to win ImageNet. ReLU, Dropout, Data Augmentation. 60M parameters.

## VGG (2014)

VGG-16: 13 conv layers + 3 FC layers. All 3x3 convolutions (stacked to increase receptive field). Simple, uniform design. 138M parameters. Expensive.

## ResNet (2015)

Introduced residual connections:

y = F(x, {W_i}) + x

Allows training ultra-deep networks (50, 101, 152 layers). Skip connections solve the degradation problem (deeper should not be worse).

ResNet-50: 25M parameters.
ResNet-152: 60M parameters.

## EfficientNet (2019)

Systematically scales depth, width, and resolution using neural architecture search:

depth: d = α^φ
width: w = β^φ
resolution: r = γ^φ

where α·β²·γ² ≈ 2, φ is controlled by compute budget.

EfficientNet-B0: 5.3M parameters, 77.1% top-1 on ImageNet.
EfficientNet-B7: 66M parameters, 84.3% top-1.

## Comparison

| Model | Year | Params | ImageNet Top-1 | Key Innovation |
|-------|------|--------|----------------|----------------|
| LeNet-5 | 1998 | 60K | - | First CNN |
| AlexNet | 2012 | 60M | 63.3% | Deep CNN, ReLU |
| VGG-16 | 2014 | 138M | 74.4% | 3x3 stacks |
| ResNet-50 | 2015 | 25M | 76.0% | Skip connections |
| EfficientNet-B0 | 2019 | 5.3M | 77.1% | Compound scaling |
