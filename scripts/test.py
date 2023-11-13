import streamlit as st
from sentence_transformers import SentenceTransformer, util
from pages.Tutor import generate_response
import json

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

@st.cache_data
def generate_comprehension_test(transcript):
    prompt = "Can you create 5 simple test questions based on the following transcript: " + \
        transcript + \
        "Your response should be in the form of an undeclared Python List of Dictionaries with 2 keys: Question, Answer." + \
        "In your response just provide the list, nothing else such that I can use the json.loads function to parse it."
    test_questions = generate_response(prompt, 0.2)
    test_questions_list = json.loads(test_questions)
    return test_questions_list

def cefr_score(score):
    if score >= 0 and score <= 45:
        return "A1"
    elif score >= 46 and score <= 60:
        return "A2"
    elif score >= 61 and score <= 75:
        return "B1"
    elif score >= 76 and score <= 90:
        return "B2"
    elif score >= 91 and score <= 100:
        return "C1"
    else:
        return "Invalid range"