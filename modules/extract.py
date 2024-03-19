"""Property extraction module

    This module contains all the methods to extract properties from
    audio samples
"""


import numpy as np


def extract_frequency(audio):
    # Extract frequency from audio using FFT
    samples = np.array(audio.get_array_of_samples())
    fft_result = np.fft.fft(samples)
    frequencies = np.fft.fftfreq(len(samples))
    # Find the peak frequency
    peak_index = np.argmax(np.abs(fft_result))
    peak_frequency = frequencies[peak_index]
    return peak_frequency

def extract_audio_properties(audio):
    # Extract audio properties
    volume = extract_volume(audio)
    frequency = extract_frequency(audio)
    panning = extract_panning(audio)
    return {'volume': volume, 'frequency': frequency, 'panning': panning}

def extract_volume(audio):
    # Extract volume from audio
    return audio.dBFS

def extract_panning(audio):
    # Extract panning from audio samples
    samples = audio.get_array_of_samples()
    left_channel = samples[::2]
    right_channel = samples[1::2]
    panning = sum(right_channel) / sum(left_channel) if sum(left_channel) != 0 else 0
    return max(-1.0, min(panning, 1.0))

def calculate_audio_texture(audio):
    # Calculate audio texture from audio samples
    samples = np.array(audio.get_array_of_samples())
    diff = np.sum(np.abs(np.diff(samples)))
    return diff / (len(samples) - 1) if len(samples) > 1 else 0