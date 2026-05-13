import streamlit as st
from utils.gemini_helper import generate_response

# --- CONFIGURACIÓN DE AVATARES ---
USER_AVATAR = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
AI_AVATAR = "https://cdn-icons-png.flaticon.com/512/4712/4712139.png"


def handle_chat():
    """Interfaz de chat estilo ChatGPT con soporte técnico petrolero."""

    # --- ESTILOS PERSONALIZADOS CHAT ---
    st.markdown("""
        <style>

        .stChatMessage {
            border-radius: 14px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }

        .stChatMessage[data-testid="stChatMessageUser"] {
            background-color: #EFF6FF;
            border: 1px solid #BFDBFE;
        }

        .stChatMessage[data-testid="stChatMessageAssistant"] {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
        }

        .stChatInputContainer {
            border-top: 1px solid #E2E8F0;
            padding-top: 1rem;
        }

        </style>
    """, unsafe_allow_html=True)

    # --- HISTORIAL CHAT ---
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "👋 Hola Ingeniero. Soy **PetroGPT PRO**, "
                    "tu asistente especializado en producción, "
                    "yacimientos, pruebas de pozo y análisis técnico."
                )
            }
        ]

    # --- MOSTRAR HISTORIAL ---
    for msg in st.session_state.messages:

        avatar = USER_AVATAR if msg["role"] == "user" else AI_AVATAR

        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # --- INPUT USUARIO ---
    prompt = st.chat_input(
        "Escribe una consulta técnica..."
    )

    if prompt:

        # Limpieza básica
        prompt = prompt.strip()

        if prompt == "":
            st.warning("Por favor escribe una consulta válida.")
            return

        # --- GUARDAR MENSAJE USER ---
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        # --- MOSTRAR USER ---
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)

        # --- RESPUESTA IA ---
        with st.chat_message("assistant", avatar=AI_AVATAR):

            with st.spinner("🧠 Analizando información técnica..."):

                try:

                    response = generate_response(prompt)

                    # Validación respuesta vacía
                    if not response:
                        response = (
                            "⚠️ El modelo no generó una respuesta válida."
                        )

                    # Mostrar respuesta
                    st.markdown(response)

                    # Guardar respuesta
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })

                except Exception as e:

                    error_msg = f"""
                    ❌ Error en el motor de IA.

                    Detalle técnico:
                    `{str(e)}`
                    """

                    st.error(error_msg)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
