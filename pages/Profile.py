import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np
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

def main():

    chart_data = pd.DataFrame(
        np.random.randint(0, 50, size=(12, 3)),
        columns=["Listening - Audio (hrs)", "Listening - Video (hrs)", "Reading (hrs)"],
        index=['01-Jan','02-Feb','03-Mar','04-Apr','05-May','06-Jun','07-Jul','08-Aug','09-Sep','10-Oct','11-Nov','12-Dec']
        )

    st.title("Profile Page")

    # Display user profile
    st.subheader("User Profile")
    st.write(f"Name: {st.session_state.name}")
    st.write(f"Username: {st.session_state.username}")
    st.write(f"Current Lanaguage Level: 82")
    st.write(f"Bio: Passionate polyglot with an insatiable thirst for linguistic knowledge, constantly exploring new languages and cultures with boundless enthusiasm.")

    st.subheader("Learning Progress")
    st.area_chart(chart_data)

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.write(f'Welcome *{st.session_state["name"]}*',)
    main()
elif st.session_state["authentication_status"] == False:
    st.sidebar.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.sidebar.warning('Please enter your username and password')