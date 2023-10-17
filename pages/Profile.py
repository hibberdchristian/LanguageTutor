import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(
    np.random.randint(0, 50, size=(12, 3)),
    columns=["Listening - Audio (hrs)", "Listening - Video (hrs)", "Reading (hrs)"],
    index=['01-Jan','02-Feb','03-Mar','04-Apr','05-May','06-Jun','07-Jul','08-Aug','09-Sep','10-Oct','11-Nov','12-Dec']
    )

# Initialize database connection
conn = st.experimental_connection("mysql",type="sql")

df = conn.query("SELECT * from mytable;", ttl=600)

st.title("Profile Page")

# Display user profile

for user in df.itertuples():
    st.subheader("User Profile")
    st.write(f"Name: {user.name}")
    st.write(f"Email: {user.email}")
    st.write(f"Current Lanaguage Level: {user.language_level}")
    st.write(f"Bio: {user.bio}")

st.subheader("Learning Progress")
st.area_chart(chart_data)