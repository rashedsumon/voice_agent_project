import speech_recognition as sr
import sounddevice as sd
import numpy as np
import wavio

def record_audio(duration=5, fs=44100):
    """
    Record audio from microphone for given duration.
    Returns path to the WAV file.
    """
    print("Recording...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    audio_file = "assets/recorded.wav"
    wavio.write(audio_file, audio_data, fs, sampwidth=2)
    return audio_file
