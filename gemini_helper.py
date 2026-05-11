import os
import google.generativeai as genai
from typing import Optional

# --- CONFIGURACIÓN DEL MODELO ---
# Puedes cambiarlo a 'gemini-1.5-pro' si necesitas más potencia
MODEL_NAME = "gemini-1.5-flash"

def generate_response(prompt: str) -> str:
    """
    Se conecta a la API de Google Gemini y genera una respuesta basada en el prompt.
    
    Args:
        prompt (str): La pregunta o comando del usuario.
        
    Returns:
        str: La respuesta de la IA o un mensaje de error amigable.
    """
    # 1. Obtener la API Key desde las variables de entorno
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return "⚠️ Error: No se encontró la GEMINI_API_KEY. Asegúrate de configurarla en los secretos de Streamlit o variables de entorno."

    try:
        # 2. Configurar la SDK
        genai.configure(api_key=api_key)
        
        # 3. Inicializar el modelo
        model = genai.GenerativeModel(MODEL_NAME)
        
        # 4. Generar contenido
        response = model.generate_content(prompt)
        
        # 5. Retornar el texto de la respuesta
        return response.text
        
    except Exception as e:
        # Manejo de errores profesional para principiantes
        print(f"Error interno: {e}")
        return "🤖 Lo siento, tuve un problema al procesar tu solicitud. Por favor, intenta de nuevo en unos momentos."
