import streamlit_authenticator as stauth

#insert passwords to be hashed -> open terminal and run Streamlit run scripts/hash.py
hashed_passwords = stauth.Hasher([
    'VerbalVoyage123'
]).generate()
print(hashed_passwords)