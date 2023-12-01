import streamlit_authenticator as stauth

#insert passwords to be hashed -> open terminal and run Streamlit run scripts/hash.py
hashed_passwords = stauth.Hasher([
    'PolyglotPro123!'
]).generate()
print(hashed_passwords)