import streamlit as st
import whisper
import torch
import spacy
import subprocess
from googletrans import Translator
from dateparser.search import search_dates

# Ensure spaCy language model is installed
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Load Whisper Model
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()
st.success("🎙️ Whisper Model Loaded Successfully!")

# Upload Audio File
uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    # Save file temporarily
    audio_path = "temp_audio.mp3"
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.read())

    # Transcribe Audio
    st.info("Transcribing audio...")
    result = model.transcribe(audio_path)
    transcribed_text = result["text"]
    st.success("✅ Transcription Complete!")
    st.text_area("Transcribed Text", transcribed_text, height=200)

    # Translate Text
    def translate_to_english(text):
        translator = Translator()
        detected_lang = translator.detect(text).lang
        if detected_lang in ["ur", "pa"]:
            translation = translator.translate(text, src=detected_lang, dest="en")
            return translation.text
        return text

    translated_text = translate_to_english(transcribed_text)
    st.subheader("🔠 Translated Text")
    st.write(translated_text)

    # Extract Date & Events
    def extract_date_time_and_event(sentence):
        extracted_data = search_dates(sentence)
        if extracted_data:
            date_time = extracted_data[0][1]
            event_text = sentence.replace(extracted_data[0][0], "").strip()
        else:
            date_time = None
            event_text = sentence
        return date_time, event_text

    extracted_dates = []
    for sentence in translated_text.split("."):
        date_time, event_text = extract_date_time_and_event(sentence)
        if date_time:
            extracted_dates.append({"date_time": date_time, "event_text": event_text})

    st.subheader("📅 Extracted Dates & Events")
    if extracted_dates:
        for item in extracted_dates:
            st.write(f"🗓️ **Date/Time:** {item['date_time']} | 📌 **Event:** {item['event_text']}")
    else:
        st.warning("⚠️ No dates found in the text.")
