import os
import streamlit as st
import google.generativeai as genai

# --- MODELO GEMINI ---
# Modelo recomendado para Streamlit + apps académicas
MODEL_NAME = "gemini-1.5-flash"


def generate_response(prompt: str) -> str:
    """
    Genera una respuesta usando Gemini API.
    """

    # --- OBTENER API KEY ---
    api_key = (
        st.secrets.get("GEMINI_API_KEY")
        or os.getenv("GEMINI_API_KEY")
    )

    # --- VALIDAR API KEY ---
    if not api_key:
        return (
            "⚠️ Error: No se encontró la API Key de Gemini.\n\n"
            "Verifica tu archivo secrets.toml o variables de entorno."
        )

    try:

        # --- CONFIGURAR GEMINI ---
        genai.configure(api_key=api_key)

        # --- CREAR MODELO ---
        model = genai.GenerativeModel(
            model_name=MODEL_NAME
        )

        # --- PROMPT ENGINEERING ---
        system_prompt = f"""
        Actúa como un ingeniero senior especialista en:

        - Ingeniería de producción
        - Ingeniería de yacimientos
        - Step Rate Tests
        - Well Testing
        - Artificial Lift
        - Sanding analysis
        - Nodal analysis
        - Reservoir surveillance

        Responde de manera:
        - técnica
        - clara
        - profesional
        - académica
        - estructurada

        Consulta del usuario:
        {prompt}
        """

        # --- GENERAR RESPUESTA ---
        response = model.generate_content(
            system_prompt
        )

        # --- VALIDAR RESPUESTA ---
        if not response:
            return "⚠️ Gemini no generó una respuesta."

        if not hasattr(response, "text"):
            return "⚠️ La respuesta del modelo llegó vacía."

        return response.text

    except Exception as e:

        error_msg = str(e)

        # --- ERRORES COMUNES ---
        if "404" in error_msg:
            return (
                f"🤖 Error 404:\n\n"
                f"El modelo '{MODEL_NAME}' no fue encontrado.\n\n"
                f"Verifica:\n"
                f"- nombre del modelo\n"
                f"- cuota disponible\n"
                f"- permisos de Gemini API"
            )

        elif "API_KEY_INVALID" in error_msg:
            return (
                "🔑 Error de autenticación.\n\n"
                "La API Key de Gemini es inválida."
            )

        elif "quota" in error_msg.lower():
            return (
                "📉 Has excedido la cuota gratuita de Gemini API."
            )

        return f"🤖 Error inesperado:\n\n{error_msg}"
