import streamlit as st
import streamlit_authenticator as stauth
import json
from scripts.test import cefr_score
import scripts.database as db
import yaml
from yaml import SafeLoader
with open ("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

st.set_page_config(layout="wide")
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

# Load the quiz
file_path = "resources/assessment.json"

with open(file_path, "r") as json_file:
    quiz = json.load(json_file)

# Define a function to run the quiz
def run_quiz():
    # Initialize the score and question index
    score = 0
    question_idx = 0
    existing_score = db.check_user_score(st.session_state.username)

    # Check if the quiz is finished
    if existing_score:
        st.write(f"You completed the Assessment!")
        st.write(f"We estimate you're at CEFR level {cefr_score(existing_score)}")
        retake_button = st.button("Retake")
        if retake_button:
            db.remove_user_score(st.session_state.username)
            st.session_state.quiz_session_state = {"score": 0, "question_idx": 0}
            st.experimental_rerun()
        else:
            return
    
    # Initialize the session state
    if "quiz_session_state" not in st.session_state:
        st.session_state.quiz_session_state = {"score": 0, "question_idx": 0}
    
    # Get the current state from the session state
    score = st.session_state.quiz_session_state["score"]
    question_idx = st.session_state.quiz_session_state["question_idx"]
    
    # Create a Streamlit form to display the quiz
    form = st.form(key="quiz_form")
    form.write(f"Question {question_idx+1}: {quiz[question_idx]['question']}")
    selected_option = form.radio("Select your answer:", quiz[question_idx]["options"], index=None)
    submitted = form.form_submit_button("Next")
    
    # Check if the answer is correct
    if submitted:
        if selected_option == quiz[question_idx]["answer"]:
            score += 2.5
        
        # Increment the question index
        question_idx += 1

        # Check if we've reached the end of the quiz
        if question_idx >= len(quiz):
            st.write(f"We estimate you're at CEFR level {cefr_score(score)}")
            db.write_score_to_database(st.session_state.username, score)
            st.session_state.quiz_session_state = {"score": 0, "question_idx": 0}
        else:
            st.session_state.quiz_session_state = {"score": score, "question_idx": question_idx}
            # Reload the app to load the next question
            st.experimental_rerun()

# Create the Streamlit app with a form
def main():
    st.title("🇬🇧 Level Assessment")
    run_quiz()
    
if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.write(f'Welcome *{st.session_state["name"]}*',)
    main()
elif st.session_state["authentication_status"] == False:
    st.sidebar.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.sidebar.warning('Please enter your username and password')