import os
import google.generativeai as genai
try:
    from google.colab import userdata
    HAS_COLAB_USERDATA = True
except ImportError:
    HAS_COLAB_USERDATA = False

# Usamos el nombre calificado del modelo para evitar errores 404
MODEL_NAME = "models/gemini-1.5-flash"

def generate_response(prompt: str, user_api_key: str = None) -> str:
    """
    Genera una respuesta usando la API de Gemini.
    Prioridad de API Key: 
    1. Clave pasada por parámetro (desde la UI)
    2. Variable de entorno (Streamlit Secrets/OS)
    3. Google Colab Secrets (si aplica)
    """
    api_key = user_api_key or os.getenv("GEMINI_API_KEY")
    
    if not api_key and HAS_COLAB_USERDATA:
        try:
            api_key = userdata.get('GOOGLE_API_KEY')
        except:
            pass

    if not api_key:
        return "⚠️ Error: No se encontró una API Key válida. Por favor, ingrésala en la configuración."

    try:
        genai.configure(api_key=api_key)
        # Intentamos instanciar el modelo con el nombre corregido
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error en Gemini: {e}")
        return f"🤖 Error técnico: {str(e)}"
