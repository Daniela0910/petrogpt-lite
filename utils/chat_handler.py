import os

# Asegurar que el directorio existe
os.makedirs('utils', exist_ok=True)

# Definimos el contenido del chat con el formato corregido
chat_code = """import streamlit as st
from utils.gemini_helper import generate_response

# Configuración de Avatares
USER_AVATAR = \"https://cdn-icons-png.flaticon.com/512/3135/3135715.png\"
AI_AVATAR = \"https://cdn-icons-png.flaticon.com/512/4712/4712139.png\"

def handle_chat():
    \"\"\"Interfaz de chat estilo ChatGPT con soporte para ingeniería.\"\"\"
    
    # Estilos CSS inyectados para las burbujas
    st.markdown(\"\"\"
        <style>
        .stChatMessage { 
            border-radius: 12px; 
            padding: 1rem; 
            margin-bottom: 0.8rem; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .stChatMessage[data-testid='stChatMessageUser'] { 
            background-color: #F1F5F9; 
            border: 1px solid #E2E8F0; 
        }
        .stChatMessage[data-testid='stChatMessageAssistant'] { 
            background-color: #FFFFFF; 
            border: 1px solid #3B82F6; 
        }
        </style>
    \"\"\", unsafe_allow_html=True)

    if \"messages\" not in st.session_state:
        st.session_state.messages = [
            {\"role\": \"assistant\", \"content\": \"Hola Ingeniero, soy tu asistente **PetroGPT PRO**. ¿Qué análisis técnico realizaremos hoy?\"}
        ]

    for msg in st.session_state.messages:
        avatar = USER_AVATAR if msg[\"role\"] == \"user\" else AI_AVATAR
        with st.chat_message(msg[\"role\"], avatar=avatar):
            st.markdown(msg[\"content\"])

    if prompt := st.chat_input(\"Escribe aquí tu consulta técnica...\"):
        st.session_state.messages.append({\"role\": \"user\", \"content\": prompt})
        with st.chat_message(\"user\", avatar=USER_AVATAR):
            st.markdown(prompt)

        with st.chat_message(\"assistant\", avatar=AI_AVATAR):
            with st.spinner(\"Procesando consulta técnica...\"):
                try:
                    response = generate_response(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({\"role\": \"assistant\", \"content\": response})
                except Exception as e:
                    st.error(f\"Error en el motor de IA: {str(e)}\")
"""

# Escritura segura del archivo
with open('utils/chat_handler.py', 'w', encoding='utf-8') as f:
    f.write(chat_code)

print("✅ Archivo utils/chat_handler.py actualizado con éxito.")
