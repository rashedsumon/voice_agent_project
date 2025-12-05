import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import numpy as np
import wavio
import os
import threading
import time

# Create assets folder if it doesn't exist
os.makedirs("assets", exist_ok=True)

def record_audio(duration=5, fs=44100):
    """
    Record audio from the browser for a fixed duration using Streamlit WebRTC.
    Returns path to the WAV file.
    """
    st.write(f"Recording audio for {duration} seconds...")

    audio_file = "assets/recorded.wav"
    frames = []

    class AudioProcessor:
        def __init__(self):
            self.frames = []

        def recv_audio(self, frame: av.AudioFrame):
            pcm = frame.to_ndarray()
            self.frames.append(pcm)
            return frame

    processor = AudioProcessor()

    webrtc_ctx = webrtc_streamer(
        key="audio-recorder",
        mode=WebRtcMode.SENDONLY,
        client_settings=ClientSettings(
            media_stream_constraints={"audio": True, "video": False}
        ),
        audio_processor_factory=lambda: processor,
        async_processing=True,
        desired_playing_state=True,
    )

    # Wait for the specified duration
    start_time = time.time()
    while time.time() - start_time < duration:
        st.sleep(0.1)

    # Stop the WebRTC streamer
    webrtc_ctx.stop()

    # Process recorded frames
    if processor.frames:
        audio_data = np.concatenate(processor.frames, axis=1).T  # Proper shape for wavio
        wavio.write(audio_file, audio_data, fs, sampwidth=2)
        st.success(f"Audio saved to {audio_file}")
        return audio_file
    else:
        st.warning("No audio recorded.")
        return None

# Example usage in Streamlit
if st.button("Record Audio"):
    record_audio(duration=5)
