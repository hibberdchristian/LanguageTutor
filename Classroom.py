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

st.title("🧘 Flow Language Tutor")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm a AI Language Tutor here to help make your language learning experience fun and efficient.\n\
         I'm great at helping to answer those tricky grammer question, coming up with example sentences, or even helping you come up with a study plan!"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            engine = "gpt-35-turbo",
            max_tokens = 500,
            temperature = 0.5,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    st.write(st.session_state.messages)