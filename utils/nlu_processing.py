from transformers import pipeline

# Initialize transformer NLU pipeline
nlu_pipeline = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

def parse_user_intent(audio_file):
    """
    Convert speech to text and detect intent.
    """
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
    
    result = nlu_pipeline(text)[0]
    intent = result['label']
    entities = {}  # Extend with NER if needed
    return intent, entities
