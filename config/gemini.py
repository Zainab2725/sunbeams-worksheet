import streamlit as st
from google import genai

MODEL_NAME = "gemini-2.5-flash"

def get_client():
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to Streamlit Cloud Secrets."
        )
    return genai.Client(api_key=api_key)
