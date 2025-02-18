import whisper

# Load the Whisper model
model = whisper.load_model("base")
print("Model loaded successfully!")

# Transcribe an audio file using raw string notation
result = model.transcribe(r"C:\Users\mohib\Downloads\WhatsApp Audio 2025-02-14 at 16.42.31_8f156670.waptt.mp3")
print("Transcription:", result["text"])
from googletrans import Translator

def translate_to_english(text):
    translator = Translator()

    # Detect the language of the text
    detected_lang = translator.detect(text).lang

    # Translate to English if the text is in Urdu or Punjabi
    if detected_lang in ["ur", "pa"]:  # "ur" for Urdu, "pa" for Punjabi
        translation = translator.translate(text, src=detected_lang, dest="en")
        return translation.text
    else:
        # If the text is already in English or another supported language, return as is
        return text

# Example usage

result["text"]=translate_to_english(result["text"])
import spacy
import dateparser

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def split_into_sentences(text):
    """ Splits text into sentences with improved segmentation rules """
    doc = nlp(text)
    sentences = []
    temp_sentence = []

    for token in doc:
        temp_sentence.append(token.text)
        # Split sentence if punctuation (".", "?", "!") or conjunctions like "and" are found
        if token.text in [".", "?", "!"] or token.dep_ == "cc":
            sentences.append(" ".join(temp_sentence).strip())
            temp_sentence = []

    if temp_sentence:
        sentences.append(" ".join(temp_sentence).strip())  # Add the last sentence

    return sentences

from dateparser.search import search_dates  # ✅ Correct import

def extract_date_time_and_event(sentence):
    """Extracts date and time separately from a sentence"""
    extracted_data = search_dates(sentence)  # ✅ Correct usage
    if extracted_data:
        date_time = extracted_data[0][1]  # Extract the datetime object
        event_text = sentence.replace(extracted_data[0][0], "").strip()
    else:
        date_time = None
        event_text = sentence
    return date_time, event_text
def process_text(text):
    """ Processes text by splitting sentences and extracting date/time """
    sentences = split_into_sentences(text)
    results = []

    for sentence in sentences:
        date_time, event_text = extract_date_time_and_event(sentence)
        results.append({
            "sentence": sentence,
            "date_time": date_time,
            "event_text": event_text
        })

    return results

# ✅ Process the text correctly
results = process_text(result["text"])

# ✅ Print the results
for result1 in results:
    print("Sentence:", result1["sentence"])
    print("Date/Time:", result1["date_time"])
    print("Event Text:", result1["event_text"])
    print("-" * 40)


