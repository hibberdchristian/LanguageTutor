import streamlit as st
import streamlit_scrollable_textbox as stx
from youtube_transcript_api import YouTubeTranscriptApi
from wordfreq import zipf_frequency
from PyDictionary import PyDictionary
from scripts.transcript import summarize

col1, col2, col3 = st.columns([4,1,4])

class RareWord:
    def __init__(self, word, definition):
        self.word = word
        self.definition = definition

col1.title("Embedded Media")
    
# Get YouTube video ID from user
video_id = col1.text_input("Enter YouTube Video ID")
    
# Generate YouTube video URL
video_url = f"https://www.youtube.com/watch?v={video_id}"
    
# Display embedded YouTube video and its transcript
if video_id:

    with col1:
        st.video(video_url)

    transcript = YouTubeTranscriptApi.get_transcript(video_id, preserve_formatting=True)
    dictionary = PyDictionary()
    transcript_text = ""
    rare_words = []
    for i, line in enumerate(transcript):

        words = line['text'].split()
        for word in words:
            if(zipf_frequency(word, 'en', wordlist='best') < 2.5):
                rare_words.append(RareWord(word, dictionary.meaning(word)))

        transcript_text += f"{i + 1}. {line['text']}\n"

    summary = summarize(transcript_text)

    with col3:
        st.subheader("Transcript")
        stx.scrollableTextbox(transcript_text, height = 600)
        st.subheader("Summary")
        st.write(summary)

    if rare_words:
        col1.subheader("Rare Words")
        for rare_word in rare_words:
            expander = col1.expander(f"{rare_word.word}")
            expander.write(f"**Definition**: {rare_word.definition}")
            # for key, values in rare_word.definition:
            #     for value in values:
            #         expander.write(f"{key}: {value}")
