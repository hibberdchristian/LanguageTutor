import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import scripts.transcript as ts
import scripts.database as db
from youtube_transcript_api import YouTubeTranscriptApi
import scripts.test as test
import scripts.utilities as utilities
import yaml
import re
from yaml import SafeLoader
with open ("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

st.set_page_config(layout = "wide")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'sidebar')

if 'video' not in st.session_state:
    st.session_state.video = ''
if 'audio' not in st.session_state:
    st.session_state.audio = None
if 'article' not in st.session_state:
    st.session_state.article = ''

container = st.container()
col1, col2 = st.columns([4,2])

home_title = "🧘 Flow Language Learning"
container.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=5>Beta</font></span>""",unsafe_allow_html=True)
container.markdown("""\n""")
container.markdown("Welcome to Flow Language Learning! We are here to support you all the way on your journey to fluency. "
            "Flow take real-world content such as Videos, Podcasts, and Blogs and integrates them into an immersive learning environment. "
            "Got questions, need a few example sentences? Ask our AI Language Tutor Flow 👋")
container.markdown("""\n""")

def main():

    container.markdown("#### Get started!")
    container.markdown("Select one of the following multimedia to get started!")
    with container:
        selected = option_menu(
                menu_title=None,
                options=["Video", "Audio", "Written"],
                icons=["camera-video", "mic", "pen"],
                default_index=0,
                orientation="horizontal",
            )

    if selected == 'Video':
        # Get YouTube video ID
        video_url = col1.text_input("Enter YouTube Video URL", value=st.session_state.video)
        video_id = utilities.extract_video_id(video_url)
        st.session_state.video = video_url

        if video_url:
            # Embed Video on Page
            col1.video(f"{st.session_state.video}")
            # Get the transcript
            raw_transcript = YouTubeTranscriptApi.get_transcript(video_id, preserve_formatting=True)
            transcript = ts.parse_transcript(raw_transcript)
            create_classroom(transcript)
    
    if selected == 'Audio':
        # Upload audio file
        audio = col1.file_uploader("Upload an Audio File", type=["mp3"])
        st.session_state.audio = audio

        if audio:  
            # Embed Audio Player on Page
            audio_bytes = audio.read()
            col1.audio(audio_bytes, format='audio/wav')

            # Present the Transcript
            transcript = ts.transcribe_audio(audio)
            create_classroom(transcript)

    if selected == 'Written':
        # Get Article URL
        article_url = col1.text_input("Enter Article URL", value=st.session_state.article)
        st.session_state.article = article_url

        if article_url:
            # Embed Article on Page
            transcript = ts.scrape_article(article_url)
            create_classroom(transcript)

def create_classroom(transcript):
        
    expander = col1.expander('Full Transcript')
    expander.write(transcript)

    # Present a Summary
    col2.markdown("""\n""")
    col2.markdown("#### Summary")
    summary = ts.summarize(transcript)
    col2.markdown(summary)

    # Present the Difficult Words
    zipf = test.zipf_value(db.check_user_score(st.session_state.username))
    rare_words = ts.extract_rare_words(transcript, zipf["lower"], zipf["upper"])
    if rare_words:
        col2.markdown("#### Words")
        for rare_word in rare_words:
            expander = col2.expander(f"{rare_word.word}")
            expander.write(f"**Definition**: {rare_word.definition}")
            create_flashcard = expander.button(":red[Create Flashcard]", key={rare_word.word})
            if create_flashcard:
                result = db.save_flashcard(st.session_state.username, rare_word.word)
                if result == "success":
                    expander.success(f"Flashcard for '{rare_word.word}' created!")
                elif result == "exist":
                    expander.warning(f"Flashcard for '{rare_word.word}' already exists.")
                else:
                    expander.error("Failed to create flashcard.")


    st.divider()
    # Present the Test
    test_questions_list = test.generate_comprehension_test(transcript)
    st.markdown("#### Comprehension Test")
    for i, question in enumerate(test_questions_list):
        with st.expander(f"Question {i+1}: {question['Question']}"):
            answer = st.text_input('Answer', key=i, placeholder='Input your answer', label_visibility="hidden")
            if answer:
                st.markdown(test.mark_comprehension_answer(answer, question['Answer']))
                st.markdown(f"Model Answer: {question['Answer']}")

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.write(f'Welcome *{st.session_state["name"]}*',)
    main()
elif st.session_state["authentication_status"] == False:
    st.sidebar.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.sidebar.warning('Please enter your username and password')