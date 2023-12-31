import streamlit as st
from wordfreq import zipf_frequency
from PyDictionary import PyDictionary
from langchain import HuggingFaceHub
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from tempfile import NamedTemporaryFile
import re
import whisper
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from pages.Tutor import generate_response
import json

API_KEY =st.secrets["api_keys"]["huggingface"]

class RareWord:
    def __init__(self, word, definition):
        self.word = word
        self.definition = definition

class NamedEntity:
    def __init__(self, word, entity):
        self.word = word
        self.entity = entity

@st.cache_data
def extract_rare_words(transcript, zipf_lower, zipf_upper):

    rare_words = []
    dictionary = PyDictionary()
    words = transcript.split()
    # Shuffle Words and remove duplicates
    words = list(set(words))
    np.random.shuffle(words)

    for word in words:
        if(zipf_lower <= zipf_frequency(word, 'en', wordlist='best') <= zipf_upper) and dictionary.meaning(word) is not None:
            rare_words.append(RareWord(word, dictionary.meaning(word)))
            # Maximum 5 words per time
            if len(rare_words) >= 4:
                break
                              
    return rare_words

@st.cache_data
def summarize(transcript):
    llm = HuggingFaceHub(repo_id="facebook/bart-large-cnn", model_kwargs={"temperature":0.5}, huggingfacehub_api_token=API_KEY)
    return llm("Please provide a summary of the following transcript: " + transcript) 

def parse_transcript(transcript):
    transcript_text = ""
    for i, line in enumerate(transcript):
        transcript_text += f"{line['text']}\n"
    # Add linebreak after each sentence
    transcript_text = transcript_text.replace(".", ".\n")
    return transcript_text

@st.cache_data
def scrape_article(article_url):
    req = Request(article_url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find_all(re.compile('^h[1-6]$|^p$'))
    transcript = ""
    for element in content:
        transcript += f"{element.text} \n"
    return transcript

@st.cache_data
def transcribe_audio(audio):

    with NamedTemporaryFile(suffix="mp3") as temp:

        temp.write(audio.getvalue())
        temp.seek(0)
        model = whisper.load_model("base")
        result = model.transcribe(temp.name)
        transcript = result["text"]
    
    return transcript

@st.cache_data
def assess_cefr(transcript):
    prompt = "Can you assess the difficulty of the following transcript based on the Common European Framework of Reference for Languages (CEFR): " + \
        transcript + \
        "Your response should be in the form of an undeclared Python List of Dictionaries with one key: language_level" + \
        "In your response just provide the list, nothing else such that I can use the json.loads function to parse it."
    cefr_level = generate_response(prompt, 0.2)
    cefr_level_list = json.loads(cefr_level)
    return cefr_level_list

@st.cache_data
def names_entity_recognition(transcript):

    named_entities = []
    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

    nlp = pipeline("ner", model=model, tokenizer=tokenizer)

    ner_results = nlp(transcript)
    for entity in ner_results:
        score = float(entity['score'])
        word = entity['word']
        # Extract only those with a score of 90 of above
        if score > 0.95 and len(word) > 1 and re.match(r'^\w+$',word) is not None:
            named_entities.append(NamedEntity(entity["word"],entity["entity"]))
            if len(named_entities) >= 3:
                break
    
    return named_entities