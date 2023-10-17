API_KEY ="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"

from wordfreq import zipf_frequency
from PyDictionary import PyDictionary
from langchain import HuggingFaceHub
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from tempfile import NamedTemporaryFile
import re
import whisper

def extract_rare_words(transcript, zipf_value):

    class RareWord:
        def __init__(self, word, definition):
            self.word = word
            self.definition = definition

    rare_words = []
    dictionary = PyDictionary()
    words = transcript.split()
    # Shuffle Words
    np.random.shuffle(words)

    for word in words:
        if(zipf_frequency(word, 'en', wordlist='best') < zipf_value) and dictionary.meaning(word) is not None:
            rare_words.append(RareWord(word, dictionary.meaning(word)))
            # Maximum 5 words per time
            if len(rare_words) > 4:
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