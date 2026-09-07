import numpy as np
import sounddevice as sd
import tkinter as tk
from tkinter import ttk

# --- REAL-TIME AUDIO ENGINE ---
SAMPLE_RATE = 48000
current_freq = 50.0     # Default starting frequency
current_db = -24.0      # Default starting amplitude (safe low volume)
phase = 0.0             # Tracks the sine wave phase to prevent popping
is_playing = False

def audio_callback(outdata, frames, time, status):
    """Generates continuous audio chunk-by-chunk in real time."""
    global phase
    
    if not is_playing:
        outdata.fill(0)
        return
        
    # Convert dB to linear voltage multiplier
    amp = 10.0 ** (current_db / 20.0)
    
    # Calculate the continuous phase for this exact chunk of time
    phase_increment = 2 * np.pi * current_freq / SAMPLE_RATE
    phases = phase + np.arange(frames) * phase_increment
    
    # Generate the sine wave
    wave = np.sin(phases) * amp
    
    # Save the last phase point for the next chunk (modulo 2pi keeps the math stable)
    phase = (phases[-1] + phase_increment) % (2 * np.pi)
    
    # Output identical wave to Left and Right channels for the TDA2030A
    outdata[:, 0] = wave
    outdata[:, 1] = wave

# Start the audio stream in the background
stream = sd.OutputStream(channels=2, callback=audio_callback, samplerate=SAMPLE_RATE)
stream.start()

# --- GUI DASHBOARD ---
def update_frequency(val):
    """Converts a 0-100 linear slider into a 20Hz-2000Hz logarithmic scale."""
    global current_freq
    slider_val = float(val)
    # Logarithmic mapping function
    current_freq = 20.0 * (100.0 ** (slider_val / 100.0))
    freq_label.config(text=f"Frequency: {current_freq:.1f} Hz")

def update_amplitude(val):
    global current_db
    current_db = float(val)
    db_label.config(text=f"Amplitude: {current_db:.1f} dBFS")

def toggle_audio():
    global is_playing
    is_playing = not is_playing
    if is_playing:
        play_btn.config(text="STOP TONE", style="Stop.TButton")
    else:
        play_btn.config(text="START TONE", style="Start.TButton")

# Build the Window
root = tk.Tk()
root.title("Stethoscope Acoustic Calibration")
root.geometry("450x300")
root.configure(padx=20, pady=20)

style = ttk.Style()
style.configure("Start.TButton", font=("Arial", 12, "bold"), foreground="green")
style.configure("Stop.TButton", font=("Arial", 12, "bold"), foreground="red")

# Frequency Control
freq_label = ttk.Label(root, text="Frequency: 50.0 Hz", font=("Arial", 14))
freq_label.pack(anchor="w", pady=(0, 5))

# Slider from 0 to 100 (mapped to 20-2000Hz log scale in the update function)
freq_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=update_frequency)
freq_slider.set(19.9) # Roughly sets it to 50Hz starting point
freq_slider.pack(fill="x", pady=(0, 20))

# Amplitude Control
db_label = ttk.Label(root, text="Amplitude: -24.0 dBFS", font=("Arial", 14))
db_label.pack(anchor="w", pady=(0, 5))

# Slider from -60dB (silence) to 0dB (max voltage)
db_slider = ttk.Scale(root, from_=-60.0, to=0.0, orient="horizontal", command=update_amplitude)
db_slider.set(-24.0)
db_slider.pack(fill="x", pady=(0, 20))

# Play/Stop Button
play_btn = ttk.Button(root, text="START TONE", style="Start.TButton", command=toggle_audio)
play_btn.pack(fill="x", ipady=10, pady=10)

# Cleanly close the audio stream when exiting the window
def on_closing():
    stream.stop()
    stream.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()