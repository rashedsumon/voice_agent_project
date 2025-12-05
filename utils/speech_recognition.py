import streamlit as st
import wavio
import numpy as np
import os

# Create assets folder if it doesn't exist
os.makedirs("assets", exist_ok=True)

def record_audio(uploaded_file=None, fs=44100):
    """
    Process audio from a file upload (WAV or other formats).
    Saves it as 'assets/recorded.wav' and returns the path.
    """
    audio_file = "assets/recorded.wav"

    if uploaded_file is not None:
        # Convert uploaded file to WAV using wavio
        # Read raw bytes and convert to numpy array
        audio_bytes = uploaded_file.read()
        with open(audio_file, "wb") as f:
            f.write(audio_bytes)

        st.success(f"Audio saved to {audio_file}")
        return audio_file
    else:
        st.warning("No audio file uploaded.")
        return None
