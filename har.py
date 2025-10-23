import sounddevice as sd
import numpy as np
from scipy import signal
import aubio
import threading
import pandas as pd
import time 

# Cooldown to throttle note printing and sound generation
last_play_time = 0
cooldown_secs = 1.0  # Adjust the interval (in seconds) between detections


# Parameters
sample_rate = 44100
buffer_size = 2048
aubio_buffer_size = buffer_size // 2  # 1024
hop_size = aubio_buffer_size // 2     # 512

# Load frequency-note mapping dataset
note_df = pd.read_csv("note_dataset.csv")  # Make sure the CSV is in your working directory
note_list = list(zip(note_df["Note"], note_df["Frequency"]))

# Initialize pitch detector
pitch_detector = aubio.pitch("default", aubio_buffer_size, hop_size, sample_rate)
pitch_detector.set_unit("Hz")
pitch_detector.set_tolerance(0.8)

# Map frequency to nearest note using dataset
def frequency_to_note_from_dataset(frequency):
    if frequency == 0:
        return "No note detected"
    closest_note = min(note_list, key=lambda x: abs(x[1] - frequency))
    return closest_note[0]

# Generate harmonium-like sound using waveforms
def generate_harmonium_sound(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sawtooth_wave = 0.5 * signal.sawtooth(2 * np.pi * frequency * t)
    square_wave = 0.3 * signal.square(2 * np.pi * frequency * t, duty=0.5)
    harmonium_sound = sawtooth_wave + square_wave
    harmonium_sound /= np.max(np.abs(harmonium_sound))
    return harmonium_sound

# Play harmonium tone in a background thread
def play_harmonium(frequency):
    harmonium_sound = generate_harmonium_sound(frequency, 1, sample_rate)
    sd.play(harmonium_sound, sample_rate)

# Real-time audio callback
def audio_callback(indata, frames, time_info, status):
    global last_play_time  # to update it inside callback

    if status:
        print("Error:", status)

    samples = np.mean(indata, axis=1).astype(np.float32)
    samples = samples[:hop_size]
    frequency = pitch_detector(samples)[0]

    current_time = time.time()
    if frequency > 0 and (current_time - last_play_time) > cooldown_secs:
        note = frequency_to_note_from_dataset(frequency)
        print(f"Detected Frequency: {frequency:.2f} Hz → Nearest Note: {note}")
        threading.Thread(target=play_harmonium, args=(frequency,), daemon=True).start()
        last_play_time = current_time

# Start audio stream
try:
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate, blocksize=buffer_size):
        print("🎹 Real-time harmonium synthesis started. Press Ctrl+C to stop.")
        while True:
            sd.sleep(1000)
except KeyboardInterrupt:
    print("\n🛑 Program exited safely.")
