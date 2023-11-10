import streamlit as st
import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the employees table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                  (id INTEGER PRIMARY KEY, name TEXT, salary REAL)''')

# Define the data for the new row
name = 'John Doe'
salary = 5000

# Insert the data into the table
cursor.execute("INSERT INTO employees (name, salary) VALUES (?, ?)", (name, salary))

# Commit the changes to the database
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()

# Define the questions and their corresponding answers
questions = [
    {
        'question': 'What is the capital of France?',
        'options': ['Paris', 'London', 'Berlin', 'Rome'],
        'correct_answer': 'Paris'
    },
    {
        'question': 'What is the capital of England?',
        'options': ['Paris', 'London', 'Berlin', 'Rome'],
        'correct_answer': 'London'
    }
]

# Initialize session state variables
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0

# Display the current question
current_question = questions[st.session_state.current_question]
st.write(current_question['question'])

# Display the options as radio buttons
selected_option = st.radio('Select your answer:', current_question['options'])

# Check if the selected option is correct and update the score
if selected_option == current_question['correct_answer']:
    st.session_state.score += 1

# Display the score
st.write(f"Current Score: {st.session_state.score}")

# Button to proceed to the next question
if st.button('Next'):
    # Increment the current question index
    st.session_state.current_question += 1
    
    # Check if all questions have been answered
    if st.session_state.current_question == len(questions):
        # Display the final score
        st.write(f"Final Score: {st.session_state.score}/{len(questions)}")
        # Reset the session state variables for a new test
        st.session_state.current_question = 0
        st.session_state.score = 0