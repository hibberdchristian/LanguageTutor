import openai
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml import SafeLoader
with open ("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_key = "378219d89fce4267ac77cdbc96d3fc1e"
openai.api_base = "https://ai-proxy.lab.epam.com/"

st.set_page_config(layout="wide")

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

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Generate a response from the Google Flan T5 XXL Model
def generate_response(input_text):
    completion = openai.ChatCompletion.create(
        engine = "gpt-35-turbo",
        max_tokens = 500,
        temperature = 0.5,
        messages = [
            {"role": "assistant", "content": "You are a helpful language tutor"},
            {"role": "user", "content": input_text}
        ]
    )
    response = completion.choices[0].message.content
    return response

def chat(input_text):
    # Display user message in chat message container
    st.chat_message("user").markdown(input_text)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": input_text})

    response = generate_response(input_text)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

st.title("💬 Flow Language Tutor")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    chat(prompt)