# Voice Harmonizer-Using Dataset

An enhanced harmonium synthesizer that uses a dataset of note frequencies for accurate musical note mapping. This version includes a cooldown period to prevent repeated triggers and improves note detection using a CSV-based frequency table ("note_dataset.csv").

**Key features:**
Real-time pitch detection and harmonium synthesis
Note lookup from a custom dataset
Throttled output to reduce duplicate triggers
Background audio generation

**Usage:**
Prepared a CSV file named "note_dataset.csv" with "Note" and "Frequency" columns.
Run the script and provide microphone access.
Detected notes and frequencies will print, and harmonium sounds will play at intervals.

Dependencies: sounddevice, numpy, scipy, aubio, pandas. Install via pip. Press Ctrl+C to stop.
