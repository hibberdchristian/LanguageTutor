import streamlit as st
import scripts.database as db
import json

# Set up Streamlit layout
st.title('👍 Recommended Learning Content')

# Extract content of the same level
contents = json.loads(db.extract_content_from_database("B2"))

# Check if news data exists
if len(contents) > 0:
    for content in contents:
        st.subheader(content['type'])
        st.write(content['url'])
        expander = st.expander("Content Sample")
        expander.write(content['transcript'][:1000] + '...')
        
        st.write('---')
else:
    st.write('Error: No news articles found in the data.')