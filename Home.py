import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import scripts.transcript as transcript
from youtube_transcript_api import YouTubeTranscriptApi
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

if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.write(f'Welcome *{name}*',)
elif authentication_status == False:
    st.sidebar.error('Username/password is incorrect')
elif authentication_status == None:
    st.sidebar.warning('Please enter your username and password')

language = st.sidebar.selectbox("#### Language", ["English", "中文"])

if language == "English":
    home_title = "🧘 Flow Language Learning"
    st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=5>Beta</font></span>""",unsafe_allow_html=True)
    st.markdown("""\n""")
    st.markdown("Welcome to Flow Language Learning! We here to support you all the way on your journey to fluency. "
                "Flow take real-world content such as Videos, Podcasts, and Blogs and integrates them into an immersive learning environment. "
                "Got questions, need a few example sentences? Ask our AI Language Tutor Flow 👋")
    st.markdown("""\n""")
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
        video_id = col1.text_input("Enter YouTube Video ID")

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
            st.write(named_entities)

            # Present the Test
            prompt = "Can you create 5 simple test questions based on the following transcript: " + \
                parsed_transcript + \
                "Your response should be in the form of an undeclared Python List of Dictionaries with 2 keys: Question, Answer." + \
                "In your response just provide the list, nothing else such that I can use the json.loads function to parse it."
            test_questions = generate_response(prompt, 0.2)
            test_questions_list = json.loads(test_questions)
            st.markdown("#### Test")
            for i, question in enumerate(test_questions_list):
                with st.expander(f"Question {i+1}: {question['Question']}"):
                    st.markdown(question['Answer'])

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

            # Present the Test
            prompt = "Can you create 5 simple test questions based on the following transcript: " + \
                audio_transcript + \
                "Your response should be in the form of an undeclared Python List of Dictionaries with 2 keys: Question, Answer." + \
                "In your response just provide the list, nothing else such that I can use the json.loads function to parse it."
            test_questions = generate_response(prompt, 0.2)
            test_questions_list = json.loads(test_questions)
            st.markdown("#### Test")
            for i, question in enumerate(test_questions_list):
                with st.expander(f"Question {i+1}: {question['Question']}"):
                    st.markdown(question['Answer'])

    if selected == 'Written':
        # Get Article URL
        article_url = col1.text_input("Enter Article URL")

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

            # Present the Test
            prompt = "Can you create 5 simple test questions based on the following transcript: " + \
                article_transcript + \
                "Your response should be in the form of an undeclared Python List of Dictionaries with 2 keys: Question, Answer." + \
                "In your response just provide the list, nothing else such that I can use the json.loads function to parse it."
            test_questions = generate_response(prompt, 0.2)
            test_questions_list = json.loads(test_questions)
            st.markdown("#### Test")
            for i, question in enumerate(test_questions_list):
                with st.expander(f"Question {i+1}: {question['Question']}"):
                    st.markdown(question['Answer'])




# if language ==  '中文':
#     home_title = "AI面试官"
#     home_introduction = "欢迎使用 AI 面试官，它能够通过生成式AI帮助您准备面试。"
#     with st.sidebar:
#         st.markdown('AI面试管 - V0.1.2')
#         st.markdown(""" 
#             #### 领英:
#             [贾皓翔](https://www.linkedin.com/in/haoxiang-jia/)

#             [王梓丞](https://www.linkedin.com/in/todd-wang-5001aa264/)
#             #### 请填写表格，我们非常希望听到您的反馈：
#             [Feedback Form](https://docs.google.com/forms/d/13f4q03bk4lD7sKR7qZ8UM1lQDo6NhRaAKv7uIeXHEaQ/edit)

#             #### 使用的技术：

#             [OpenAI](https://openai.com/)

#             [FAISS](https://github.com/facebookresearch/faiss)

#             [Langchain](https://github.com/hwchase17/langchain)

#                         """)
#     st.markdown(
#         "<style>#MainMenu{visibility:hidden;}</style>",
#         unsafe_allow_html=True
#     )
#     st.image(im, width=100)
#     st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=5>Beta</font></span>""", unsafe_allow_html=True)

#     st.markdown("""\n""")
#     # st.markdown("#### Greetings")
#     st.markdown(
#         "欢迎使用AI面试官！👏AI面试官是一款由生成式人工智能驱动的个人面试官，可以进行模拟面试。您可以上传您的简历或者复制粘贴工作描述，AI面试官会根据您的情况提出定制化的问题。"
#     )
#     st.markdown("""\n""")
#     with st.expander("更新日志"):
#         st.write("""
#             08/13/2023
#             - 修复了当用户输入失败时的报错问题 """)
#     with st.expander("未来计划"):
#         st.write("""
#             - 提供更加稳定和快速的语音交互
#             - 支持全中文的模拟面试 """)
#     st.markdown("""\n""")
#     st.markdown("#### 让我们开始吧!")
#     st.markdown("请选择以下其中一个开始您的面试！")
#     selected = option_menu(
#         menu_title=None,
#         options=["专业评估", "简历评估", "行为评估"],
#         icons=["cast", "cloud-upload", "cast"],
#         default_index=0,
#         orientation="horizontal",
#     )
#     if selected == '专业评估':
#         st.info("""
#                 📚在本次面试中，AI面试官将会根据职位描述评估您的技术能力。
#                 注意: 您回答的最大长度为4097个tokens!
#                 - 每次面试将会持续10到15分钟。
#                 - 您可以通过刷新页面来开始新的面试。
#                 - 您可以选择您喜欢的交互方式(文字/语音)
#                 - 开始介绍您自己吧！ """)
#         if st.button("开始面试!"):
#             switch_page("Professional Screen")
#     if selected == '简历评估':
#         st.info("""
#                 📚在本次面试中，AI面试官将会根据您的简历评估您的过往经历。
#                 注意: 您回答的最大长度为4097个tokens!
#                 - 每次面试将会持续10到15分钟。
#                 - 您可以通过刷新页面来开始新的面试。
#                 - 您可以选择您喜欢的交互方式(文字/语音)
#                 - 开始介绍您自己吧！ """)
#         if st.button("开始面试!"):
#             switch_page("Resume Screen")
#     if selected == '行为评估':
#         st.info("""
#             📚在本次面试中，AI面试官将会根据您的简历评估您的技术能力。
#             注意: 您回答的最大长度为4097个tokens!
#             - 每次面试将会持续10到15分钟。
#             - 您可以通过刷新页面来开始新的面试。
#             - 您可以选择您喜欢的交互方式(文字/语音)
#             - 开始介绍您自己吧！ """)
#         if st.button("开始面试!"):
#             switch_page("Behavioral Screen")
#     st.markdown("""\n""")
#     st.markdown("#### 维基")
#     st.write(
#         '[点击查看常见问题，更新和计划！](https://jiatastic.notion.site/wiki-8d962051e57a48ccb304e920afa0c6a8?pvs=4)')