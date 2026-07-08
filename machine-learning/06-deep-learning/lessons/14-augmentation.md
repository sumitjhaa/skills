# 06.14 Augmentation

Data augmentation artificially expands the training set through label-preserving transformations.

## Image Augmentations

- **Flip**: Horizontal (and sometimes vertical) mirroring
- **Rotation**: Random rotation by θ degrees
- **Crop/Resize**: Random crops, often with padding
- **Scale**: Random scaling factors
- **Translate**: Shift image in x/y
- **Shear**: Affine shear transforms

## Color Augmentations

- **Brightness**: Add random offset to pixel values
- **Contrast**: Multiply pixel values by random factor
- **Saturation**: Adjust color intensity
- **Hue**: Shift hue channel
- **Grayscale**: Randomly convert to grayscale

## Noise

- **Gaussian**: Add N(0, σ²) noise
- **Salt & Pepper**: Random black/white pixels
- **Speckle**: Multiplicative noise

## Advanced Techniques

- **Mixup**: Blend two images: x = λ·x₁ + (1-λ)·x₂, y = λ·y₁ + (1-λ)·y₂
- **Cutout**: Remove a random square patch from image
- **CutMix**: Cut patch from one image and paste onto another, blend labels
- **RandAugment**: Randomly apply augmentations from a learned set
- **AutoAugment**: Search for optimal augmentation policy

## Common Practice

For CIFAR-10/100:
- Random horizontal flip
- Random crop with 4px padding
- Cutout (16x16 patch)

For ImageNet:
- RandomResizedCrop (0.08 to 1.0 scale)
- Random horizontal flip
- Color jitter (brightness=0.4, contrast=0.4, saturation=0.4, hue=0.1)

## Implementation

For a NumPy framework, implement augmentations as functions operating on (C, H, W) arrays using scipy.ndimage for affine transforms.
