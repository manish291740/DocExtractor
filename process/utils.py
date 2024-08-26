import pytesseract, os
import spacy
from transformers import pipeline
from django.conf import settings
from .models import AIText

# Load spaCy model for NER at startup
nlp = spacy.load("en_core_web_sm")

# Load Hugging Face pipelines at startup
sentiment_pipeline = pipeline("sentiment-analysis")
classification_pipeline = pipeline("text-classification")

def OCRText(image):
    os.environ[r'TESSDATA_PREFIX'] = settings.TESSDATA_PREFIX
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
    Text = pytesseract.image_to_string(image)
    return Text

def analyze_text_with_ai(text):
    doc = nlp(text)
    ner_results = [{"entity": ent.text, "type": ent.label_} for ent in doc.ents]

    classification = classification_pipeline(text)
    classification_result = {"label": classification[0]['label'], "score": classification[0]['score']}

    sentiment = sentiment_pipeline(text)
    sentiment_result = {"sentiment": sentiment[0]['label'], "score": sentiment[0]['score']}

    results = {
        "NER": ner_results,
        "Classification": classification_result,
        "Sentiment": sentiment_result
    }

    return results
