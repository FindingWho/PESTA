import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Load the data
df = pd.read_csv('heartbeat_data.csv')

# Drop any corrupted rows and convert to numeric
df['adc_value'] = pd.to_numeric(df['adc_value'], errors='coerce')
df = df.dropna()
signal = df['adc_value'].values

# 2. Remove the DC bias (centers the wave exactly at 0)
signal = signal - np.mean(signal)

# 3. Calculate actual sampling rate (total samples / 10 seconds)
fs = len(signal) / 10.0
print(f"Calculated Sampling Rate: {fs:.2f} Hz")

# Create time axis
time = np.linspace(0, 10, len(signal))

# 4. Plotting
# sharex=True physically locks the time axes together
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Top Plot: Raw Waveform (Time Domain)
ax1.plot(time, signal, color='blue', linewidth=0.5)
ax1.set_title('Raw Heartbeat Waveform (Time Domain)')
ax1.set_ylabel('Amplitude (Centered ADC Value)')
ax1.grid(True, alpha=0.3)

# Bottom Plot: Spectrogram
Pxx, freqs, bins, im = ax2.specgram(signal, Fs=fs, NFFT=256, cmap='inferno', noverlap=128)
ax2.set_title('Cardiopulmonary Spectrogram')
ax2.set_xlabel('Time (seconds)')
ax2.set_ylabel('Frequency (Hz)')
ax2.set_ylim(0, 2000) # Cap at the 2000Hz target ceiling

# This shrinks both graphs equally so they align vertically
fig.colorbar(im, ax=[ax1, ax2], label='Intensity (dB)', fraction=0.05, pad=0.04)

# Force the x-axis to start exactly at 0 and end exactly at 10
ax1.set_xlim(0, 10)

plt.savefig('heartbeat_analysis.jpg', dpi=300) 
print("Saved perfectly aligned plot to 'heartbeat_analysis.jpg'")
plt.show()
