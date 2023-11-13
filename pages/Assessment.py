import streamlit as st
import json
import sqlite3
from scripts.test import cefr_score

# # Connect to the database
# conn = sqlite3.connect('database.db')
# cursor = conn.cursor()

# # Create the employees table if it doesn't exist
# cursor.execute('''CREATE TABLE IF NOT EXISTS employees
#                   (id INTEGER PRIMARY KEY, name TEXT, salary REAL)''')

# # Define the data for the new row
# name = 'John Doe'
# salary = 5000

# # Insert the data into the table
# cursor.execute("INSERT INTO employees (name, salary) VALUES (?, ?)", (name, salary))

# # Commit the changes to the database
# conn.commit()

# # Close the cursor and the connection
# cursor.close()
# conn.close()

# Load the quiz
file_path = "resources/assessment.json"

with open(file_path, "r") as json_file:
    quiz = json.load(json_file)

# Define a function to run the quiz
def run_quiz():
    # Initialize the score and question index
    score = 0
    question_idx = 0
    
    # Initialize the session state
    if "quiz_session_state" not in st.session_state:
        st.session_state.quiz_session_state = {"score": 0, "question_idx": 0}
    
    # Get the current state from the session state
    score = st.session_state.quiz_session_state["score"]
    question_idx = st.session_state.quiz_session_state["question_idx"]
    
    # Create a Streamlit form to display the quiz
    form = st.form(key="quiz_form")
    form.write(f"Question {question_idx+1}: {quiz[question_idx]['question']}")
    selected_option = form.radio("Select your answer:", quiz[question_idx]["options"])
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
            st.session_state.quiz_session_state = None
        else:
            st.session_state.quiz_session_state = {"score": score, "question_idx": question_idx}
            # Reload the app to load the next question
            st.experimental_rerun()

# Create the Streamlit app with a form
def main():
    st.title("🇬🇧 Level Assessment")
    run_quiz()
    st.write(st.session_state)
    
if __name__ == "__main__":
    main()