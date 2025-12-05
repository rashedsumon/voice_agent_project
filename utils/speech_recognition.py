import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import numpy as np
import wavio
import os

# Create assets folder if it doesn't exist
os.makedirs("assets", exist_ok=True)

def record_audio(fs=44100):
    """
    Record audio from the browser using Streamlit WebRTC.
    Returns path to the WAV file.
    """
    st.write("Click Start to begin recording and Stop when done.")

    audio_file = "assets/recorded.wav"

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
    )

    if st.button("Stop Recording"):
        webrtc_ctx.stop()
        if processor.frames:
            # Ensure all frames are same length
            audio_data = np.hstack(processor.frames)
            wavio.write(audio_file, audio_data, fs, sampwidth=2)
            st.success(f"Audio saved to {audio_file}")
            return audio_file
        else:
            st.warning("No audio recorded.")
            return None
