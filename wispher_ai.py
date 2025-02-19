import streamlit as st
import whisper
import torch
import spacy
import subprocess
from googletrans import Translator
from dateparser.search import search_dates

# ✅ Ensure spaCy language model is installed
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
        return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

# ✅ Load Whisper Model
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()
st.success("🎙️ Whisper Model Loaded Successfully!")

# ✅ Upload Audio File
uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    # Save file temporarily
    audio_path = "temp_audio.mp3"
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.read())

    # ✅ Transcribe Audio
    st.info("Transcribing audio...")
    result = model.transcribe(audio_path)
    transcribed_text = result["text"]
    st.success("✅ Transcription Complete!")
    st.text_area("📜 **Transcribed Text:**", transcribed_text, height=200)

    # ✅ Translate Text to English
    def translate_to_english(text):
        translator = Translator()
        detected_lang = translator.detect(text).lang
        if detected_lang in ["ur", "pa"]:  # Urdu or Punjabi
            translation = translator.translate(text, src=detected_lang, dest="en")
            return translation.text
        return text  # Return as is if already in English

    translated_text = translate_to_english(transcribed_text)
    st.subheader("🔠 **Translated Text (English):**")
    st.write(translated_text)

    # ✅ Extract Multiple Dates & Events
    def extract_dates_and_events(text):
        extracted_data = search_dates(text)  # Returns a list of (text, datetime) tuples
        events = []
        
        if extracted_data:
            for date_text, date_time in extracted_data:
                # Remove the date from the original text to identify event description
                event_text = text.replace(date_text, "").strip()
                events.append({"date_time": date_time, "event_text": event_text})
        
        return events

    extracted_dates = extract_dates_and_events(translated_text)

    # ✅ Display Extracted Dates & Events
    st.subheader("📅 **Extracted Dates & Events**")
    if extracted_dates:
        for item in extracted_dates:
            st.write(f"🗓️ **Date/Time:** {item['date_time']} | 📌 **Event:** {item['event_text']}")
    else:
        st.warning("⚠️ No dates found in the text.")
