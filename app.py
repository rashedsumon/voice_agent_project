import streamlit as st
from utils.speech_recognition import record_audio
from utils.nlu_processing import parse_user_intent
from utils.task_execution import execute_task
from utils.human_handoff import escalate_to_human
from data_loader import download_call_center_dataset

# Download dataset
dataset_path = download_call_center_dataset()
st.write(f"Dataset ready at: {dataset_path}")

# Streamlit UI
st.title("Conversational Voice Agent")
st.text("Talk to the agent by pressing the record button:")

if st.button("Record Voice"):
    st.info("Recording...")
    audio_file = record_audio()
    st.audio(audio_file, format="audio/wav")

    # NLU processing
    user_intent, entities = parse_user_intent(audio_file)
    st.write(f"Detected Intent: {user_intent}")
    st.write(f"Entities: {entities}")

    # Execute task or escalate
    if user_intent == "escalate":
        response = escalate_to_human(audio_file)
    else:
        response = execute_task(user_intent, entities)

    st.success(f"Agent Response: {response}")
