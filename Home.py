import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import scripts.transcript as transcript
from youtube_transcript_api import YouTubeTranscriptApi
import scripts.test as test
import yaml
from yaml import SafeLoader
with open ("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)
from pages.Tutor import generate_response
import json

st.set_page_config(layout = "wide")

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
    st.session_state.audio = ''
if 'article' not in st.session_state:
    st.session_state.article = ''

home_title = "🧘 Flow Language Learning"
st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=5>Beta</font></span>""",unsafe_allow_html=True)
st.markdown("""\n""")
st.markdown("Welcome to Flow Language Learning! We are here to support you all the way on your journey to fluency. "
            "Flow take real-world content such as Videos, Podcasts, and Blogs and integrates them into an immersive learning environment. "
            "Got questions, need a few example sentences? Ask our AI Language Tutor Flow 👋")
st.markdown("""\n""")

def main():

    st.markdown("#### Get started!")
    st.markdown("Select one of the following multimedia to get started!")
    selected = option_menu(
            menu_title= None,
            options=["Video", "Audio", "Written"],
            icons = ["camera-video", "mic", "pen"],
            default_index=0,
            orientation="horizontal",
        )
    
    col1, col2 = st.columns([4,2])

    if selected == 'Video':
        # Get YouTube video ID
        video_id = col1.text_input("Enter YouTube Video ID", value=st.session_state.video)
        st.session_state.video = video_id

        if video_id:
            # Embed Video on Page
            col1.video(f"https://www.youtube.com/watch?v={video_id}")

            # Present the Transcript
            video_transcript = YouTubeTranscriptApi.get_transcript(video_id, preserve_formatting=True)
            parsed_transcript = transcript.parse_transcript(video_transcript)
            with st.expander("Full Transcript"):
                st.markdown(parsed_transcript)

            # Present a Summary
            col2.markdown("""\n""")
            col2.markdown("#### Summary")
            video_summary = transcript.summarize(parsed_transcript)
            col2.markdown(video_summary)

            # Present the Difficult Words
            rare_words = transcript.extract_rare_words(parsed_transcript, 3.5)
            if rare_words:
                col2.markdown("#### Words")
                for rare_word in rare_words:
                    expander = col2.expander(f"{rare_word.word}")
                    expander.write(f"**Definition**: {rare_word.definition}")

            # Present Named Entities
            named_entities = transcript.names_entity_recognition(parsed_transcript)
            if named_entities:
                col2.markdown("#### Pronouns")
                for entity in named_entities:
                    expander = col2.expander(f"{entity.word}")
                    expander.write(f"**Type**: {entity.entity}")

            # Present the Test
            prompt = "Can you create 5 simple test questions based on the following transcript: " + \
                parsed_transcript + \
                "Your response should be in the form of an undeclared Python List of Dictionaries with 2 keys: Question, Answer." + \
                "In your response just provide the list, nothing else such that I can use the json.loads function to parse it."
            test_questions = generate_response(prompt, 0.2)
            test_questions_list = json.loads(test_questions)
            st.markdown("#### Comprehension Test")
            for i, question in enumerate(test_questions_list):
                with st.expander(f"Question {i+1}: {question['Question']}"):
                    answer = st.text_input('Answer', key=i, placeholder='Input your answer', label_visibility="hidden")
                    if answer:
                        st.markdown(test.mark_comprehension_answer(answer, question['Answer']))
                        st.markdown(f"Model Answer: {question['Answer']}")

    if selected == 'Audio':
        # Upload audio file
        audio = col1.file_uploader("Upload an Audio File", type=["mp3"])

        if audio:
            # Embed Audio Player on Page
            audio_bytes = audio.read()
            col1.audio(audio_bytes, format='audio/wav')

            # Present the Transcript
            audio_transcript = transcript.transcribe_audio(audio)
            with col1.expander("Full Transcript"):
                st.markdown(audio_transcript)

            # Present a Summary
            col2.markdown("""\n""")
            col2.markdown("#### Summary")
            audio_summary = transcript.summarize(audio_transcript)
            col2.markdown(audio_summary)

            # Present the Difficult Words
            rare_words = transcript.extract_rare_words(audio_transcript, 3.5)
            if rare_words:
                col2.markdown("#### Words")
                for rare_word in rare_words:
                    expander = col2.expander(f"{rare_word.word}")
                    expander.write(f"**Definition**: {rare_word.definition}")

            # Present Named Entities
            named_entities = transcript.names_entity_recognition(audio_transcript)
            if named_entities:
                col2.markdown("#### Pronouns")
                for entity in named_entities:
                    expander = col2.expander(f"{entity.word}")
                    expander.write(f"**Type**: {entity.entity}")

            # Present the Test
            prompt = "Can you create 5 simple test questions based on the following transcript: " + \
                audio_transcript + \
                "Your response should be in the form of an undeclared Python List of Dictionaries with 2 keys: Question, Answer." + \
                "In your response just provide the list, nothing else such that I can use the json.loads function to parse it."
            test_questions = generate_response(prompt, 0.2)
            test_questions_list = json.loads(test_questions)
            st.markdown("#### Comprehension Test")
            for i, question in enumerate(test_questions_list):
                with st.expander(f"Question {i+1}: {question['Question']}"):
                    answer = st.text_input('Answer', key=i, placeholder='Input your answer', label_visibility="hidden")
                    if answer:
                        st.markdown(test.mark_comprehension_answer(answer, question['Answer']))
                        st.markdown(f"Model Answer: {question['Answer']}")

    if selected == 'Written':
        # Get Article URL
        article_url = col1.text_input("Enter Article URL", value=st.session_state.article)
        st.session_state.article = article_url


        if article_url:
            # Embed Article on Page
            article_transcript = transcript.scrape_article(article_url)
            col1.markdown(article_transcript)

            # Present a Summary
            col2.markdown("""\n""")
            col2.markdown("#### Summary")
            article_summary = transcript.summarize(article_transcript)
            col2.markdown(article_summary)

            # Present the Difficult Words
            rare_words = transcript.extract_rare_words(article_transcript, 3.5)
            if rare_words:
                col2.markdown("#### Words")
                for rare_word in rare_words:
                    expander = col2.expander(f"{rare_word.word}")
                    expander.write(f"**Definition**: {rare_word.definition}")

            # Present Named Entities
            named_entities = transcript.names_entity_recognition(article_transcript)
            if named_entities:
                col2.markdown("#### Pronouns")
                for entity in named_entities:
                    expander = col2.expander(f"{entity.word}")
                    expander.write(f"**Type**: {entity.entity}")

            # Present the Test
            prompt = "Can you create 5 simple test questions based on the following transcript: " + \
                article_transcript + \
                "Your response should be in the form of an undeclared Python List of Dictionaries with 2 keys: Question, Answer." + \
                "In your response just provide the list, nothing else such that I can use the json.loads function to parse it."
            test_questions = generate_response(prompt, 0.2)
            test_questions_list = json.loads(test_questions)
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