import os
import streamlit as st
import google.generativeai as genai

# Configuración de modelos
MODEL_NAME = "models/gemini-1.5-flash"

def generate_response(prompt: str, user_api_key: str = None) -> str:
    """
    Genera una respuesta usando la API de Gemini.
    Busca la API Key en: Manual UI -> Streamlit Secrets -> Env Vars
    """
    # 1. Intentar obtener de la UI, si no, de Streamlit Secrets, si no, de Env Vars
    api_key = user_api_key
    
    if not api_key:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        else:
            api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "⚠️ Error: No se encontró una API Key válida. Configúrala en los Secrets de Streamlit o en la barra lateral."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🤖 Error técnico: {str(e)}"
