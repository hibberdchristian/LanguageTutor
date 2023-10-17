import streamlit as st
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from wordfreq import zipf_frequency
from PyDictionary import PyDictionary
import re
import geograpy

col1, col2, col3 = st.columns([4,1,4])

class RareWord:
    def __init__(self, word, definition):
        self.word = word
        self.definition = definition

col1.title("Embedded Media")

# Get YouTube video ID from user
article_url = col1.text_input("Enter Article URL")

if article_url:
    req = Request(article_url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    dictionary = PyDictionary()

    content = soup.find_all(re.compile('^h[1-6]$|^p$'))
    transcript = ""
    for element in content:
        transcript += f"{element.text} \n\n"

    rare_words = []
    places = geograpy.get_place_context(text=transcript)

    words = transcript.split()
    for word in words:
            if(zipf_frequency(word, 'en', wordlist='best') < 3.5) and dictionary.meaning(word) is not None:
                rare_words.append(RareWord(word, dictionary.meaning(word)))

    if rare_words:
        col3.subheader("Rare Words")
        for rare_word in rare_words:
            expander = col3.expander(f"{rare_word.word}")
            expander.write(f"**Definition**: {rare_word.definition}")

    col1.write(transcript)
    col3.write(places)