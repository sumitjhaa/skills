"""04.17 Fourier and wavelet analysis."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, ifft
from scipy.signal import spectrogram, find_peaks

np.random.seed(42)

fs = 1000.0
T = 2.0
n = int(fs * T)
t = np.linspace(0, T, n, endpoint=False)

f1, f2, f3 = 10.0, 50.0, 120.0
x = (np.sin(2*np.pi*f1*t) + 0.5*np.sin(2*np.pi*f2*t) + 0.3*np.sin(2*np.pi*f3*t)
     + 0.2*np.random.randn(n))

X = fft(x)
freqs = fftfreq(n, 1/fs)
X_mag = np.abs(X[:n//2])

t_chirp = np.linspace(0, 1, 1000)
chirp = np.sin(2*np.pi * (50 + 100*t_chirp) * t_chirp)
f_chirp, t_chirp_sg, Sxx = spectrogram(chirp, fs=1000, nperseg=100)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].plot(t[:500], x[:500], "b-", lw=1)
axes[0, 0].set_xlabel("Time (s)")
axes[0, 0].set_ylabel("Amplitude")
axes[0, 0].set_title("Signal: 10Hz + 50Hz + 120Hz + noise")
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(freqs[:n//2], X_mag, "r-", lw=1.5)
for f_val in [f1, f2, f3]:
    axes[0, 1].axvline(f_val, color="k", ls="--", alpha=0.5)
axes[0, 1].set_xlabel("Frequency (Hz)")
axes[0, 1].set_ylabel("|FFT|")
axes[0, 1].set_title("Fourier Spectrum")
axes[0, 1].set_xlim(0, 200)
axes[0, 1].grid(True, alpha=0.3)

res_idx = np.argsort(X_mag)[-5:]
peak_freqs = freqs[res_idx]
peak_mags = X_mag[res_idx]
axes[0, 2].bar(peak_freqs, peak_mags, width=2, alpha=0.7)
axes[0, 2].set_xlabel("Frequency (Hz)")
axes[0, 2].set_ylabel("Magnitude")
axes[0, 2].set_title("Top 5 Frequency Peaks")
axes[0, 2].grid(True, axis="y", alpha=0.3)

axes[1, 0].pcolormesh(t_chirp_sg, f_chirp, 10*np.log10(Sxx + 1e-10), shading="gouraud",
                      cmap="viridis")
axes[1, 0].set_xlabel("Time (s)")
axes[1, 0].set_ylabel("Frequency (Hz)")
axes[1, 0].set_title("Spectrogram: 50→150 Hz Chirp")
axes[1, 0].set_ylim(0, 200)

snr = np.linspace(0.01, 2, 30)
freq_errors = []
for s in snr:
    x_noisy = (np.sin(2*np.pi*f1*t) + s * np.random.randn(n))
    X_noisy = fft(x_noisy)
    peak_idx = np.argmax(np.abs(X_noisy[:n//2]))
    freq_errors.append(abs(freqs[peak_idx] - f1))
axes[1, 1].plot(snr, freq_errors, "o-", lw=2)
axes[1, 1].set_xlabel("Noise level (σ)")
axes[1, 1].set_ylabel("Frequency error (Hz)")
axes[1, 1].set_title("FFT Peak Estimation vs Noise")
axes[1, 1].grid(True, alpha=0.3)

x_recon = np.zeros_like(x)
n_harmonics = [1, 2, 5, 10, 20, 50]
recon_errors = []
for k in n_harmonics:
    X_copy = np.zeros_like(X)
    idx = np.argsort(np.abs(X))[::-1][:k]
    X_copy[idx] = X[idx]
    x_recon = ifft(X_copy).real
    recon_errors.append(np.mean((x_recon - np.sin(2*np.pi*f1*t) -
                                  0.5*np.sin(2*np.pi*f2*t) -
                                  0.3*np.sin(2*np.pi*f3*t))**2))
axes[1, 2].plot(n_harmonics, recon_errors, "o-", lw=2)
axes[1, 2].set_xlabel("Top k Fourier coefficients")
axes[1, 2].set_ylabel("Reconstruction MSE\n(noiseless signal)")
axes[1, 2].set_title("Signal Compression via FFT")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/17-fourier-wavelet.png")
plt.close()

print("=" * 60)
print("FOURIER AND WAVELET ANALYSIS")
print("=" * 60)
print(f"\nSignal: sin(2π·{f1}t) + 0.5·sin(2π·{f2}t) + 0.3·sin(2π·{f3}t) + noise")
print(f"  Sampling rate: {fs} Hz, Duration: {T}s, Samples: {n}")

print(f"\nFFT peak detection:")
peak_idx_sorted = np.argsort(X_mag)[-5:][::-1]
for idx in peak_idx_sorted:
    print(f"  {freqs[idx]:.1f} Hz: magnitude = {X_mag[idx]:.1f}")

print(f"\nSignal reconstruction with top k coefficients:")
for k in [1, 2, 5, 10]:
    print(f"  k={k:2d}: MSE = {recon_errors[n_harmonics.index(k)]:.6f}")

print(f"\nUncertainty principle: Δt·Δf ≥ 1/(4π)")
print(f"  Short window → good time resolution, poor frequency resolution")
print(f"  Long window → good frequency resolution, poor time resolution")
print(f"The spectrogram trades off time vs frequency resolution.")
