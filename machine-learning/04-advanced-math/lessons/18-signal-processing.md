# 04.18 Signal Processing: Sampling, Filtering, Spectral Analysis

## Motivation
Signal processing provides tools to acquire, transform, analyse, and interpret real-world measurements. These techniques are critical for preprocessing in time-series ML, audio processing, and inverse problems. Understanding sampling theory, filter design, and spectral estimation is essential for any practitioner working with sensor data, audio, or temporal signals.

## Learning Objectives
- State and apply the Nyquist–Shannon sampling theorem.
- Design and implement digital filters (low-pass, high-pass, band-pass).
- Estimate power spectral density using periodogram and Welch's method.
- Apply Kalman filtering for state estimation in robotics and time series.

## Math Foundation

### Nyquist–Shannon Sampling Theorem
A bandlimited signal $f(t)$ with maximum frequency $f_{\max}$ can be perfectly reconstructed from samples at rate $f_s \ge 2 f_{\max}$:

$$f(t) = \sum_{n=-\infty}^\infty f(nT) \operatorname{sinc}\left(\frac{t - nT}{T}\right)$$

where $T = 1/f_s$ and $\operatorname{sinc}(x) = \sin(\pi x) / (\pi x)$. Violating this condition causes **aliasing**: high frequencies masquerade as low frequencies in the sampled signal.

### Anti-Aliasing
Before sampling, apply a low-pass filter with cutoff $f_c \le f_s/2$ to remove frequencies above the Nyquist frequency. This is essential in all practical data acquisition systems.

### Digital Filters
An LTI digital filter is characterised by its impulse response $h[n]$. The output is the convolution:

$$y[n] = \sum_{k=-\infty}^\infty h[k] x[n-k] \quad \Leftrightarrow \quad Y(\omega) = H(\omega) X(\omega)$$

Common filter types:
- **FIR (Finite Impulse Response)**: $y[n] = \sum_{k=0}^{M} b_k x[n-k]$ — always stable, linear phase possible.
- **IIR (Infinite Impulse Response)**: $y[n] = \sum_{k=0}^{M} b_k x[n-k] - \sum_{k=1}^{N} a_k y[n-k]$ — more efficient but can be unstable.

### Filter Design Methods
| Method | Type | Properties |
|--------|------|-----------|
| Windowed sinc | FIR | Simple, Gibbs phenomenon at transitions |
| Butterworth | IIR | Maximally flat passband, smooth roll-off |
| Chebyshev I | IIR | Equiripple in passband, sharper cutoff |
| Chebyshev II | IIR | Equiripple in stopband, monotonic passband |
| Elliptic | IIR | Equiripple in both, sharpest cutoff for given order |

### Spectral Estimation
The power spectral density (PSD) $S_{xx}(\omega)$ describes how power is distributed across frequencies:

$$S_{xx}(\omega) = \lim_{T \to \infty} \frac{1}{2T} \mathbb{E}[|X_T(\omega)|^2]$$

where $X_T$ is the Fourier transform of a length-$T$ segment.

- **Periodogram**: $\hat{S}_{xx}(\omega) = \frac{1}{N} |\sum_{n=0}^{N-1} x[n] e^{-i\omega n}|^2$ — consistent but high variance.
- **Welch's method**: average periodograms of overlapping, windowed segments — reduces variance at cost of frequency resolution.
- **Multitaper method**: use multiple orthogonal tapers (Slepian sequences) to reduce variance while preserving resolution.

### Kalman Filter
For a linear Gaussian state-space model:

$$x_{t+1} = F_t x_t + B_t u_t + w_t, \quad w_t \sim \mathcal{N}(0, Q_t)$$
$$z_t = H_t x_t + v_t, \quad v_t \sim \mathcal{N}(0, R_t)$$

The Kalman filter recursively estimates the state via:
1. **Predict**: $\hat{x}_{t|t-1} = F_t \hat{x}_{t-1|t-1} + B_t u_t$, $P_{t|t-1} = F_t P_{t-1|t-1} F_t^\top + Q_t$
2. **Update**: $y_t = z_t - H_t \hat{x}_{t|t-1}$ (innovation), $K_t = P_{t|t-1} H_t^\top (H_t P_{t|t-1} H_t^\top + R_t)^{-1}$, $\hat{x}_{t|t} = \hat{x}_{t|t-1} + K_t y_t$, $P_{t|t} = (I - K_t H_t) P_{t|t-1}$

The Kalman filter is the optimal (minimum MSE) estimator for linear Gaussian systems.

## Python Implementation

```python
import numpy as np
from scipy.signal import butter, lfilter, filtfilt, welch, spectrogram

def design_lowpass(cutoff, fs, order=4, filter_type='butter'):
    """Design a low-pass Butterworth filter."""
    nyquist = fs / 2.0
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def apply_filter(x, b, a):
    """Apply zero-phase filter (filtfilt avoids phase shift)."""
    return filtfilt(b, a, x)

def welch_psd(x, fs=1.0, nperseg=256):
    """Power spectral density via Welch's method."""
    f, P = welch(x, fs=fs, nperseg=nperseg)
    return f, P

def kalman_filter_1d(z, F=1.0, H=1.0, Q=0.01, R=0.1, x0=0.0, P0=1.0):
    """1D Kalman filter for tracking a constant (random walk)."""
    n = len(z)
    x_est = np.zeros(n)
    P_est = np.zeros(n)
    x_pred = x0
    P_pred = P0
    
    for t in range(n):
        # predict
        x_pred = F * x_pred
        P_pred = F * P_pred * F + Q
        
        # update
        y = z[t] - H * x_pred
        K = P_pred * H / (H * P_pred * H + R)
        x_pred = x_pred + K * y
        P_pred = (1 - K * H) * P_pred
        
        x_est[t] = x_pred
        P_est[t] = P_pred
    
    return x_est, P_est

# Example: filter noisy sine wave
np.random.seed(42)
fs = 1000.0
t = np.linspace(0, 1, int(fs))
x = np.sin(2 * np.pi * 5 * t)  # 5 Hz sine
noise = 0.3 * np.random.randn(len(t))
xn = x + noise

# Design and apply low-pass filter
b, a = design_lowpass(10, fs, order=5)
x_filtered = apply_filter(xn, b, a)
print(f"SNR before: {10*np.log10(np.var(x)/np.var(noise)):.1f} dB")
print(f"SNR after: {10*np.log10(np.var(x)/np.var(x_filtered-x)):.1f} dB")

# PSD estimation
f, Pxx = welch_psd(xn, fs)
print(f"Peak frequency: {f[np.argmax(Pxx)]:.1f} Hz (true: 5 Hz)")
```

## Visualization
Plot the noisy sine wave and the filtered version — the filter removes high-frequency noise while preserving the 5 Hz signal. A second panel shows the PSD estimate via Welch's method: the 5 Hz peak is clearly visible above the noise floor. A third panel shows the Kalman filter tracking a random walk trajectory with noisy observations, with uncertainty bands ($\pm 2 \sqrt{P_t}$).

## Connections to Machine Learning

### Audio Feature Extraction
The Mel-frequency cepstral coefficients (MFCCs) pipeline:
1. Pre-emphasis (high-pass filter to boost high frequencies).
2. Framing and windowing (Hanning window).
3. Power spectrum via FFT.
4. Mel filter bank (triangular filters spaced on the Mel scale).
5. Log compression.
6. DCT to decorrelate coefficients.

MFCCs are the standard input representation for speech recognition, speaker identification, and audio classification.

### Time-Series Preprocessing
Signal processing techniques are essential ML preprocessing steps:
- **Detrending**: remove linear/quadratic trends via high-pass filtering or polynomial subtraction.
- **Denoising**: wavelet thresholding (soft/hard), Wiener filtering, or PCA-based denoising.
- **Resampling**: change sampling rate while avoiding aliasing (low-pass filter + decimation).
- **Normalisation**: $z$-score, min-max scaling, or robust scaling per segment.

### Sensor Fusion in Robotics
The extended Kalman filter (EKF) and unscented Kalman filter (UKF) fuse:
- IMU (accelerometer, gyroscope) measurements at high frequency.
- GPS measurements at low frequency.
- Visual odometry or LIDAR scans.

These provide smooth, accurate state estimates critical for autonomous navigation.

### Inverse Problems in Imaging
Many imaging inverse problems (deblurring, super-resolution, inpainting) are regularised by signal processing priors:
- **Total variation denoising**: $\min_x \frac12\|y - x\|^2 + \lambda \|\nabla x\|_1$.
- **Wiener deconvolution**: optimal inverse filter for linear degradation with known noise.
- **Plug-and-play priors**: replace the denoising step in iterative algorithms with a CNN denoiser.

## Practical Considerations

### Filter Implementation
- **Zero-phase filtering** (`scipy.signal.filtfilt`): apply the filter forward then backward, eliminating phase distortion. Essential for time-series analysis but not real-time.
- **Causal filtering** (`scipy.signal.lfilter`): real-time capable but introduces phase shift.
- **Numerical stability**: high-order IIR filters can be unstable; factor into second-order sections (SOS).

### Choosing Spectral Estimation Method
- **Periodogram**: fast, but high variance; only use for long, stationary signals.
- **Welch**: good default; trade-off: window size controls resolution vs. variance.
- **Multitaper**: best for short signals; reduces variance without sacrificing resolution.
- **Parametric methods (AR, ARMA)**: high resolution for short signals if model order is correct.

## References
- Oppenheim & Schafer, *Discrete-Time Signal Processing*, 3rd ed., Pearson 2010
- Haykin, *Adaptive Filter Theory*, 5th ed., Pearson 2014
- Welch, "The Use of Fast Fourier Transform for the Estimation of Power Spectra," *IEEE Trans. Audio Electroacoust.*, 1967
- Kalman, "A New Approach to Linear Filtering and Prediction Problems," *J. Basic Eng.*, 1960
- Vetterli, Kovačević, Goyal, *Foundations of Signal Processing*, Cambridge 2014
