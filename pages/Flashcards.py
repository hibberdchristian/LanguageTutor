import streamlit as st
import streamlit_authenticator as stauth
import scripts.database as db
import json
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

# Load the flashcards
flashcards = json.loads(db.extract_flashcards_from_database(st.session_state.username))

def display_flashcards_content(flashcards):
    # Initialize the session state
    if "flashcard_session_state" not in st.session_state:
        st.session_state.flashcard_session_state = {"index": 0}
    
    # Get the current index from the session state
    index = st.session_state.flashcard_session_state["index"]
    
    # Create a Streamlit form to handle navigation
    if len(flashcards) == 0:
        st.write('Create some flashcards to get started!')
        return
    else:
        with st.form(key="navigation_form"):
            st.write(f"Word: {flashcards[index]['word']}")
            definition = st.expander("Show definition")
            definition.write(f"{flashcards[index]['definition']}")
            col1, col2, col3= st.columns([1,1,10])
            with col1:
                previous_button = st.form_submit_button("👈")
            with col2:
                next_button = st.form_submit_button("👉")
    
    # Check if the user clicked "Previous" or "Next"
    if previous_button or next_button:
        if previous_button:
            index -= 1
        elif next_button:
            index += 1
        
        # Check if we've reached the end of the flashcards or the beginning
        if index >= len(flashcards):
            index = 0
        elif index < 0:
            index = len(flashcards) - 1
        
        st.session_state.flashcard_session_state = {"index": index}
        # Reload the app to display the next element
        st.experimental_rerun()

# Create the Streamlit app with a form
def main():
    st.title("🃏 Flashcards")
    display_flashcards_content(flashcards)

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.write(f'Welcome *{st.session_state["name"]}*',)
    main()
elif st.session_state["authentication_status"] == False:
    st.sidebar.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.sidebar.warning('Please enter your username and password')