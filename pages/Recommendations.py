import streamlit as st
import streamlit_authenticator as stauth
import scripts.test as test
import scripts.database as db
import json
import yaml
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

# Get the current userslanguage level
if 'language_level' not in st.session_state:
    st.session_state.language_level = test.cefr_score(db.check_user_score(st.session_state.username))

def content_feed():
    # Extract content of the same level
    contents = json.loads(db.extract_content_from_database(st.session_state.language_level))

    # Check if data exists
    if len(contents) > 0:
        for content in contents:
            st.subheader(content['type'])
            st.write(content['url'])
            expander = st.expander("Content Sample")
            expander.write(content['transcript'][:1000] + '...')
            
            st.write('---')
    else:
        st.write('Error: No recommendations found.')

# Create the Streamlit app with a form
def main():
    st.title('👍 Recommended Learning Content')
    content_feed()

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.write(f'Welcome *{st.session_state["name"]}*',)
    main()
elif st.session_state["authentication_status"] == False:
    st.sidebar.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.sidebar.warning('Please enter your username and password')