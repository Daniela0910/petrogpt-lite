import os
import streamlit as st
import google.generativeai as genai

# =========================
# CONFIGURACIÓN DEL MODELO
# =========================

MODEL_NAME = "models/gemini-2.5-flash"

# =========================
# CONFIGURACIÓN DE API
# =========================

api_key = ("AIzaSyAuLS7hyP8IE6qLkrQbmGfT8WP5nM4wHeI")

if api_key:
    genai.configure(api_key=api_key)

# =========================
# LISTAR MODELOS DISPONIBLES
# =========================

def list_available_models():

    try:
        models = genai.list_models()

        available = []

        for model in models:

            # Solo modelos que soportan generateContent
            if "generateContent" in model.supported_generation_methods:
                available.append(model.name)

        return available

    except Exception as e:
        return [f"Error obteniendo modelos: {str(e)}"]

# =========================
# GENERAR RESPUESTA
# =========================

def generate_response(prompt: str) -> str:

    if not api_key:
        return "⚠️ API Key no encontrada."

    try:

        model = genai.GenerativeModel(MODEL_NAME)

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        error_msg = str(e)

        if "404" in error_msg:
            return f"""
❌ Modelo no encontrado.

Modelo actual:
{MODEL_NAME}

Modelos disponibles:
{list_available_models()}
"""

        return f"❌ Error Gemini:\n\n{error_msg}"
