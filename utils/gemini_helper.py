import os
import streamlit as st
import google.generativeai as genai

MODEL_NAME = "models/gemini-1.5-flash"

def generate_response(prompt: str) -> str:
    """
    Genera respuesta usando la API Key de los Secrets de Streamlit.
    """
    # Solo busca de forma interna en Secrets o Env Vars
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "⚠️ Error: API Key no encontrada en los Secrets del servidor."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🤖 Error: {str(e)}"
