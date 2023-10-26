import streamlit as st
from sentence_transformers import SentenceTransformer, util

@st.cache_data
def mark_comprehension_answer(answer, model_answer):
    
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    emb1 = model.encode(answer)
    emb2 = model.encode(model_answer)

    # Calculate the Cosine Similarity
    cos_sim = util.cos_sim(emb1, emb2)
    
    # Convert tensor to an integer score out of 100
    score = int(float(cos_sim[0][0]) * 100)
    
    # Generate reponse
    if score > 60:
        response = f"Great job! You scored {score}% 😍"
    elif score >= 40 and score <= 60:
        response = f"Not bad! You scored {score}% 😎"
    else:
        response = f"Not quite right! You scored {score}% 🙊"
    
    return response