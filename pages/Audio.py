import streamlit as st
import streamlit.components.v1 as components
import whisper
from tempfile import NamedTemporaryFile
from wordfreq import zipf_frequency
from PyDictionary import PyDictionary

col1, col2, col3 = st.columns([4,1,4])

class RareWord:
    def __init__(self, word, definition):
        self.word = word
        self.definition = definition

col1.title("Embedded Media")

audio = st.file_uploader("Upload an Audio File", type=["mp3"])

if audio:
    with NamedTemporaryFile(suffix="mp3") as temp:

        audio_bytes = audio.read()
        st.audio(audio_bytes, format='audio/wav')

        temp.write(audio.getvalue())
        temp.seek(0)
        model = whisper.load_model("base")
        result = model.transcribe(temp.name)
        transcript = result["text"]
        col1.write(transcript)

        rare_words = []
        dictionary = PyDictionary()

        words = transcript.split()
        for word in words:
            if(zipf_frequency(word, 'en', wordlist='best') < 3.5) and dictionary.meaning(word) is not None:
                rare_words.append(RareWord(word, dictionary.meaning(word)))

        if rare_words:
            col3.subheader("Rare Words")
            for rare_word in rare_words:
                expander = col3.expander(f"{rare_word.word}")
                expander.write(f"**Definition**: {rare_word.definition}")