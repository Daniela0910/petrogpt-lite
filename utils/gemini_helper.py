import os
import streamlit as st
import google.generativeai as genai

# Usamos gemini-1.5-flash: excelente balance entre potencia y gratuidad
MODEL_NAME = "gemini-pro"

def generate_response(prompt: str) -> str:
    """
    Genera respuesta usando la API Key de los Secrets de Streamlit.
    """
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "⚠️ Error: API Key no encontrada en los Secrets del servidor."

    try:
        genai.configure(api_key=api_key)
        for m in genai.list_models():
          print(m.name)
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
             return f"🤖 Error 404: El modelo '{MODEL_NAME}' no fue encontrado. Verifica la disponibilidad en tu región."
        return f"🤖 Error: {error_msg}"

        return f"🤖 Error inesperado:\n\n{error_msg}"
