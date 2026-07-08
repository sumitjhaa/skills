# 04.17 Fourier and Wavelet Transforms

## Motivation
Fourier analysis decomposes signals into frequency components; wavelets add localisation in time. Both are essential tools for signal processing, spectral methods in ML, and analysing neural network representations. The Fourier transform is the foundation for convolutional theorems, spectral graph networks, and neural audio synthesis, while wavelets provide sparse multiresolution representations.

## Learning Objectives
- Derive the Fourier series, continuous and discrete Fourier transforms.
- Understand the uncertainty principle and its implications for time-frequency analysis.
- Implement the Fast Fourier Transform (FFT) and wavelet decomposition.
- Apply Fourier features for neural tangent kernels and spectral methods in GNNs.

## Math Foundation

### Fourier Series
Any sufficiently regular periodic function $f$ with period $T$ can be written as:

$$f(t) = \sum_{k=-\infty}^\infty c_k e^{i 2\pi k t / T}$$

where $c_k = \frac{1}{T} \int_0^T f(t) e^{-i 2\pi k t / T} dt$. The Fourier coefficients $c_k$ represent the amplitude and phase of the $k$-th harmonic.

### Continuous Fourier Transform
For non-periodic functions, the Fourier transform and its inverse are:

$$\hat{f}(\omega) = \int_{-\infty}^\infty f(t) e^{-i\omega t} dt$$
$$f(t) = \frac{1}{2\pi} \int_{-\infty}^\infty \hat{f}(\omega) e^{i\omega t} d\omega$$

### Discrete Fourier Transform (DFT)
For a finite sequence $x_0, \dots, x_{N-1}$:

$$X_k = \sum_{n=0}^{N-1} x_n e^{-2\pi i k n / N}, \quad k = 0, \dots, N-1$$

The DFT is $O(N^2)$ naively but $O(N \log N)$ with the FFT (Cooley-Tukey algorithm).

### Key Theorems
- **Parseval/Plancherel**: $\int |f(t)|^2 dt = \frac{1}{2\pi} \int |\hat{f}(\omega)|^2 d\omega$ — energy is conserved.
- **Convolution theorem**: $\widehat{f * g}(\omega) = \hat{f}(\omega) \cdot \hat{g}(\omega)$ — convolution in time = pointwise multiplication in frequency.
- **Uncertainty principle**: $\Delta t \cdot \Delta \omega \ge \frac12$ — cannot simultaneously localise in time and frequency perfectly.

### Wavelet Transform
The continuous wavelet transform (CWT) uses scaled and translated versions of a mother wavelet $\psi$:

$$W_f(a,b) = \frac{1}{\sqrt{|a|}} \int_{-\infty}^\infty f(t) \psi^*\left(\frac{t-b}{a}\right) dt$$

where $a$ is scale (inverse frequency) and $b$ is translation (time localisation). The wavelet must have zero mean: $\int \psi(t) dt = 0$.

### Discrete Wavelet Transform (DWT)
Instead of the CWT, the DWT uses dyadic scales $a = 2^j$ and translates $b = k 2^j$, giving a critically sampled, invertible representation. The DWT is computed via a filter bank of low-pass $h$ and high-pass $g$ filters:

$$c_{j+1}[n] = (c_j * h)[2n] \quad \text{(approximation coefficients)}$$
$$d_{j+1}[n] = (c_j * g)[2n] \quad \text{(detail coefficients)}$$

### Common Wavelet Families
| Wavelet | Properties | Applications |
|---------|-----------|-------------|
| Haar | Discontinuous, orthogonal | Simple edge detection |
| Daubechies (dbN) | Compact support, vanishing moments | Image compression (JPEG 2000) |
| Symlets | Near symmetric, orthogonal | Signal denoising |
| Morlet | Continuous, complex | Time-frequency analysis |
| Mexican Hat | Real, symmetric | CWT visualisation |

## Python Implementation

```python
import numpy as np

def fft_convolve(x, y):
    """Convolution via FFT (O(N log N))."""
    n = len(x) + len(y) - 1
    n_pow2 = 2**int(np.ceil(np.log2(n)))
    X = np.fft.rfft(x, n=n_pow2)
    Y = np.fft.rfft(y, n=n_pow2)
    return np.fft.irfft(X * Y, n=n_pow2)[:n]

def spectrogram(x, fs=1.0, window_size=256, hop_length=128):
    """Compute spectrogram via STFT."""
    n_frames = (len(x) - window_size) // hop_length + 1
    window = np.hanning(window_size)
    S = np.zeros((window_size // 2 + 1, n_frames))
    
    for t in range(n_frames):
        frame = x[t * hop_length : t * hop_length + window_size] * window
        S[:, t] = np.abs(np.fft.rfft(frame))
    
    return S

def haar_dwt(x):
    """Single-level Haar discrete wavelet transform."""
    n = len(x)
    n2 = n // 2
    # low-pass: average (approximation)
    c = (x[0::2] + x[1::2]) / np.sqrt(2)
    # high-pass: difference (detail)
    d = (x[0::2] - x[1::2]) / np.sqrt(2)
    return c, d

def haar_idwt(c, d):
    """Inverse Haar DWT."""
    n = len(c)
    x = np.zeros(2 * n)
    x[0::2] = (c + d) / np.sqrt(2)
    x[1::2] = (c - d) / np.sqrt(2)
    return x

# Example: analyse a chirp signal
t = np.linspace(0, 1, 1000)
x = np.sin(2 * np.pi * (10 + 200 * t) * t)  # chirp from 10 to 210 Hz

# FFT
X_freq = np.fft.rfft(x)
freqs = np.fft.rfftfreq(len(x), d=1/1000)
print(f"Dominant frequency: {freqs[np.argmax(np.abs(X_freq))]:.1f} Hz")

# Wavelet (single level)
x_short = x[:512]  # power of 2
c, d = haar_dwt(x_short)
x_recon = haar_idwt(c, d)
print(f"Wavelet reconstruction error: {np.max(np.abs(x_short - x_recon)):.2e}")
```

## Visualization
Plot the chirp signal, its FFT magnitude spectrum (wide peak from 10-210 Hz), and its spectrogram (time-frequency representation where the frequency ramp is clearly visible). A second panel shows a 3-level wavelet decomposition of an audio signal: the approximation coefficients (low frequencies) and detail coefficients at each level (band-passed high frequencies).

## Connections to Machine Learning

### Spectral Graph Neural Networks
Graph convolution in the spectral domain uses the eigendecomposition of the graph Laplacian $L = U \Lambda U^\top$:

$$x *_\mathcal{G} y = U ((U^\top x) \odot (U^\top y))$$

The Fourier transform on a graph is $U^\top x$, the inverse is $U x$. ChebNet approximates the spectral filter with Chebyshev polynomials of $\Lambda$, avoiding expensive eigendecompositions. GCN simplifies further with a first-order approximation.

### Fourier Features for Neural Tangent Kernels
Rahimi & Recht's random Fourier features approximate the RBF kernel:

$$k(x,y) \approx \frac{2}{m} \sum_{j=1}^m \cos(w_j^\top x + b_j) \cos(w_j^\top y + b_j)$$

where $w_j \sim \mathcal{N}(0, \sigma^{-2} I)$ and $b_j \sim \mathcal{U}[0, 2\pi]$. The neural tangent kernel of an infinite-width network with sinusoidal activations is a shift-invariant kernel with Fourier feature expansion.

### Wavelet Scattering Networks
The scattering transform (Mallat 2012) cascades wavelet decompositions with modulus nonlinearities:

$$Sx = \{x * \phi_J, \|x * \psi_{j_1}\| * \phi_J, \|\|x * \psi_{j_1}\| * \psi_{j_2}\| * \phi_J, \dots\}$$

The scattering coefficients are locally translation-invariant, stable to deformations, and provide excellent representations for audio and texture classification with linear classifiers.

### Neural Audio Synthesis
WaveNet uses dilated causal convolutions as a time-domain model. The FFT-based overlap-add method generates audio efficiently. Neural vocoders (WaveGlow, HiFi-GAN) operate on spectrograms (STFT magnitudes) and use the inverse STFT to reconstruct audio.

## Practical Considerations

### Choosing FFT vs Wavelet
- **FFT**: stationary signals, global frequency content, spectral analysis.
- **STFT**: slowly time-varying signals, short-time stationarity.
- **Wavelet**: non-stationary signals with transients, discontinuities, or multiscale structure.
- **CWT**: fine-grained time-frequency analysis (exploration).
- **DWT**: compression, denoising (critical sampling).

### Computational Complexity
- FFT: $O(N \log N)$.
- DWT: $O(N)$ per level, $O(N)$ total for $J$ levels.
- STFT: $O(N \log N)$ for each window, $O(N \log N \cdot N/K)$ total.

## References
- Mallat, *A Wavelet Tour of Signal Processing*, 3rd ed., Academic Press 2009
- Bracewell, *The Fourier Transform and Its Applications*, 3rd ed., McGraw-Hill 2000
- Cooley & Tukey, "An Algorithm for the Machine Calculation of Complex Fourier Series," *Math. Comp.*, 1965
- Daubechies, *Ten Lectures on Wavelets*, SIAM 1992
- Bruna et al., "Spectral Networks and Deep Locally Connected Networks on Graphs," *ICLR 2014*
