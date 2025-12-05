import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import numpy as np
import wavio
import os

# Create assets folder if it doesn't exist
os.makedirs("assets", exist_ok=True)

def record_audio(duration=5, fs=44100):
    """
    Record audio from the browser for a given duration using Streamlit WebRTC.
    Returns path to the WAV file.
    """
    st.write("Recording... Press Stop when done.")

    audio_file = "assets/recorded.wav"
    frames = []

    class AudioProcessor:
        def __init__(self):
            self.frames = []

        def recv_audio(self, frame: av.AudioFrame):
            # Convert to numpy array
            pcm = frame.to_ndarray()
            self.frames.append(pcm)
            return frame

    processor = AudioProcessor()

    webrtc_ctx = webrtc_streamer(
        key="example",
        mode=WebRtcMode.SENDONLY,
        client_settings=ClientSettings(
            media_stream_constraints={"audio": True, "video": False}
        ),
        audio_processor_factory=lambda: processor,
        async_processing=True,
    )

    # Wait until user stops recording
    while webrtc_ctx.state.playing:
        st.sleep(0.1)

    if processor.frames:
        audio_data = np.concatenate(processor.frames, axis=1).T  # Convert to proper shape
        wavio.write(audio_file, audio_data, fs, sampwidth=2)
        st.success(f"Audio saved to {audio_file}")
        return audio_file
    else:
        st.warning("No audio recorded.")
        return None
