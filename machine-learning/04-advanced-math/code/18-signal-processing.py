"""04.18 Signal processing: filtering, estimation, detection."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, lfilter, savgol_filter, wiener, correlate
from scipy.ndimage import gaussian_filter1d

np.random.seed(42)

fs = 500.0
T = 5.0
n = int(fs * T)
t = np.linspace(0, T, n, endpoint=False)

true_signal = np.sin(2*np.pi*3*t) + 0.5*np.sin(2*np.pi*8*t)
noise = 0.5 * np.random.randn(n)
x_noisy = true_signal + noise

def butter_lowpass(cutoff, fs, order=4):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    return b, a

b, a = butter_lowpass(10.0, fs, order=4)
x_lowpass = filtfilt(b, a, x_noisy)
x_savgol = savgol_filter(x_noisy, window_length=51, polyorder=3)
x_wiener = wiener(x_noisy, mysize=51)
x_gauss = gaussian_filter1d(x_noisy, sigma=2.0)

x_lms = np.zeros_like(x_noisy)
mu_lms = 0.01
w = np.zeros(20)
for i in range(20, len(x_noisy)):
    x_seg = x_noisy[i-20:i]
    x_lms[i] = w @ x_seg
    w += mu_lms * (x_noisy[i] - x_lms[i]) * x_seg

x_corr = correlate(x_noisy, x_noisy, mode="same")
lags = np.arange(-len(x_noisy)//2, len(x_noisy)//2) / fs

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].plot(t[:500], x_noisy[:500], "b-", lw=0.5, alpha=0.5, label="Noisy")
axes[0, 0].plot(t[:500], true_signal[:500], "k-", lw=1.5, label="True signal")
axes[0, 0].set_xlabel("Time (s)")
axes[0, 0].set_ylabel("Amplitude")
axes[0, 0].set_title("Noisy Signal (SNR=2)")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(t[:500], x_lowpass[:500], "r-", lw=1.5, label="Butterworth LP")
axes[0, 1].plot(t[:500], x_savgol[:500], "g-", lw=1.5, label="Savitzky-Golay")
axes[0, 1].plot(t[:500], true_signal[:500], "k--", lw=1, label="True")
axes[0, 1].set_xlabel("Time (s)")
axes[0, 1].set_ylabel("Amplitude")
axes[0, 1].set_title("Filtering Comparison")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

snrs = np.linspace(0.5, 5, 20)
rmse_lp, rmse_sg = [], []
for s in snrs:
    x_n = true_signal + s * np.random.randn(n)
    x_lp = filtfilt(b, a, x_n)
    x_sg = savgol_filter(x_n, 51, 3)
    rmse_lp.append(np.sqrt(np.mean((x_lp - true_signal)**2)))
    rmse_sg.append(np.sqrt(np.mean((x_sg - true_signal)**2)))
axes[0, 2].plot(snrs, rmse_lp, "o-", lw=2, label="Butterworth")
axes[0, 2].plot(snrs, rmse_sg, "s-", lw=2, label="Savitzky-Golay")
axes[0, 2].set_xlabel("Noise level σ")
axes[0, 2].set_ylabel("RMSE")
axes[0, 2].set_title("Filtering Performance vs Noise")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

axes[1, 0].plot(lags, x_corr, "b-", lw=1.5)
peak_idx = np.argmax(x_corr[len(x_noisy)//2:]) + len(x_noisy)//2
axes[1, 0].axvline(lags[peak_idx], color="r", ls="--",
                   label=f"Peak at τ={lags[peak_idx]:.3f}s")
axes[1, 0].set_xlabel("Lag (s)")
axes[1, 0].set_ylabel("Autocorrelation")
axes[1, 0].set_title("Autocorrelation Function")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

t_pulse = np.linspace(0, 1, 1000)
pulse = np.exp(-((t_pulse-0.5)/0.05)**2) * np.cos(2*np.pi*20*(t_pulse-0.5))
t_long = np.linspace(0, 2, 2000)
signal_long = np.zeros(2000)
signal_long[500:1500] = np.random.randn(1000) * 0.3
signal_long[900:1900] += pulse * 0.5
detection = correlate(signal_long, pulse, mode="same")
threshold = 0.5 * np.max(detection)
detections = np.where(detection > threshold)[0]
axes[1, 1].plot(t_long, signal_long, "b-", lw=1, label="Signal")
axes[1, 1].plot(t_long, detection / np.max(detection), "r-", lw=1.5, label="Detection")
for d in detections[::20]:
    axes[1, 1].axvline(t_long[d], color="g", ls="--", alpha=0.3)
axes[1, 1].set_xlabel("Time (s)")
axes[1, 1].set_ylabel("Amplitude")
axes[1, 1].set_title("Pulse Detection via Cross-Correlation")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

N_range = [50, 100, 200, 500, 1000, 2000]
mse_lp_N = []
for N in N_range:
    tn = np.linspace(0, 2, N)
    xn = np.sin(2*np.pi*3*tn) + 0.5*np.sin(2*np.pi*8*tn) + 0.5*np.random.randn(N)
    bn, an = butter_lowpass(10, N/2)
    xf = filtfilt(bn, an, xn)
    mse_lp_N.append(np.sqrt(np.mean((xf - np.sin(2*np.pi*3*tn) -
                                      0.5*np.sin(2*np.pi*8*tn))**2)))
axes[1, 2].loglog(N_range, mse_lp_N, "o-", lw=2)
axes[1, 2].loglog(N_range, 1/np.sqrt(N_range), "--", lw=2, label="O(1/√N)")
axes[1, 2].set_xlabel("N (samples)")
axes[1, 2].set_ylabel("RMSE")
axes[1, 2].set_title("Filtering Error vs Sample Size")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/18-signal-processing.png")
plt.close()

print("=" * 60)
print("SIGNAL PROCESSING: FILTERING & DETECTION")
print("=" * 60)
snr_val = np.var(true_signal) / np.var(noise)
print(f"\nSignal SNR: {snr_val:.4f}")

rmse_lp_now = np.sqrt(np.mean((x_lowpass - true_signal)**2))
rmse_sg_now = np.sqrt(np.mean((x_savgol - true_signal)**2))
rmse_wi = np.sqrt(np.mean((x_wiener - true_signal)**2))
rmse_ga = np.sqrt(np.mean((x_gauss - true_signal)**2))
print(f"\nFiltering RMSE:")
print(f"  Butterworth (fc=10Hz): {rmse_lp_now:.4f}")
print(f"  Savitzky-Golay:        {rmse_sg_now:.4f}")
print(f"  Wiener filter:         {rmse_wi:.4f}")
print(f"  Gaussian filter:       {rmse_ga:.4f}")

print(f"\nPulse detection:")
print(f"  {len(detections)} detections above threshold (t={threshold:.3f})")

print(f"\nKey methods:")
print(f"  • FIR/IIR filtering (Butterworth: maximally flat)")
print(f"  • Savitzky-Golay: polynomial smoothing")
print(f"  • Wiener filter: optimal linear MMSE estimation")
print(f"  • Cross-correlation: matched filtering")
print(f"  • LMS adaptive filter: online gradient descent")
