import streamlit_authenticator as stauth

#insert passwords to be hashed -> open terminal and run Streamlit run scripts/hash.py
hashed_passwords = stauth.Hasher([
    'PolyglotP0wer!',
    'LinguaL0ver$',
    'Talk2MeInTongues',
    'VerbNoun123',
    'FluentFiesta!',
    'WordWizard42',
    'LingvoLandmarks',
    'GrammarGuru99',
    'VocabularyVoyage',
    'LinguaLeap@2023',
    'MultilingualMadness',
    'CultureCraver#',
    'LinguaLlama22',
    'WordplayWonder!',
    'LanguageLabyrinth$',
    'SpeechSurfer123',
    'LinguisticJourney',
    'ConverseAndLearn',
    'LexiconLover@',
    'LinguaNova777'
]).generate()
print(hashed_passwords)