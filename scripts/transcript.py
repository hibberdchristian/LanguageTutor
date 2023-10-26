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

API_KEY =st.secrets["api_keys"]["huggingface"]

def extract_rare_words(transcript, zipf_value):

    class RareWord:
        def __init__(self, word, definition):
            self.word = word
            self.definition = definition

    rare_words = []
    dictionary = PyDictionary()
    words = transcript.split()
    # Shuffle Words and remove duplicates
    words = list(set(words))
    np.random.shuffle(words)

    for word in words:
        if(zipf_frequency(word, 'en', wordlist='best') < zipf_value) and dictionary.meaning(word) is not None:
            rare_words.append(RareWord(word, dictionary.meaning(word)))
            # Maximum 5 words per time
            if len(rare_words) >= 4:
                break
                              
    return rare_words

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

def transcribe_audio(audio):

    with NamedTemporaryFile(suffix="mp3") as temp:

        temp.write(audio.getvalue())
        temp.seek(0)
        model = whisper.load_model("base")
        result = model.transcribe(temp.name)
        transcript = result["text"]
    
    return transcript

def names_entity_recognition(transcript):

    class NamedEntity:
        def __init__(self, word, entity):
            self.word = word
            self.entity = entity

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