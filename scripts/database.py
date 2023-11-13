import sqlite3

def write_score_to_database(username, score):
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the scores table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS scores
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, score REAL)''')

    # Check if the username already exists in the table
    cursor.execute("SELECT * FROM scores WHERE username = ?", (username,))
    existing_row = cursor.fetchone()

    if existing_row:
        # Update the score for the existing username
        cursor.execute("UPDATE scores SET score = ? WHERE username = ?", (score, username))
    else:
        # Insert a new row with the username and score
        cursor.execute("INSERT INTO scores (username, score) VALUES (?, ?)", (username, score))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and the connection
    cursor.close()
    conn.close()

def check_user_score(username):
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the username exists in the scores table
    cursor.execute("SELECT score FROM scores WHERE username = ?", (username,))
    row = cursor.fetchone()

    # Close the cursor and the connection
    cursor.close()
    conn.close()

    if row:
        return row[0]  # Return the score
    else:
        return False  # No entry found for the username
    
def remove_user_score(username):
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Remove the user's score from the scores table
    cursor.execute("DELETE FROM scores WHERE username = ?", (username,))
    conn.commit()

    # Close the cursor and the connection
    cursor.close()
    conn.close()

def save_flashcard(username, word):
    # Connect to the database and create a cursor
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Create the flashcards table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            word TEXT NOT NULL
        );
    """)

    # Check if the word already exists
    cursor.execute("SELECT id FROM flashcards WHERE username = ? AND word = ?", (username, word))
    result = cursor.fetchone()
    if result is not None:
        # Close the cursor and connection
        cursor.close()
        conn.close()
        return "exist"

    # Insert the new flashcard
    try:
        cursor.execute("INSERT INTO flashcards (username, word) VALUES (?, ?)", (username, word))
        conn.commit()
        return "success"
    except sqlite3.Error:
        conn.rollback()
        return "failure"
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()