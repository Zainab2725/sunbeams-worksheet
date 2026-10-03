import streamlit as st

DEFAULTS = {
    "material_analysis": None,
    "worksheet": None,
    "answer_key": None,
    "flashcards": None,
    "quiz": None,
    "revision_notes": None,
    "resource_history": [],
    "uploaded_names": [],
    "quiz_answers": {},
}

def init_session():
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value.copy() if isinstance(value, (list, dict)) else value
