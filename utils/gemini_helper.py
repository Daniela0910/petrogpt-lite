import streamlit as st
from utils.gemini_helper import generate_response

def handle_chat():
    """Gestiona la lógica y la interfaz del chat tcnico."""
    st.header("사 Chat Tcnico IA")

    # Inicializar historial de chat en el estado de la sesión
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar mensajes previos
    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

    # Entrada del usuario
    if prompt := st.chat_input("Consulta tcnica..."):
        # Guardar y mostrar mensaje del usuario
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generar y mostrar respuesta del asistente
        with st.chat_message("assistant"):
            with st.spinner("Consultando a la IA..."):
                try:
                    res = generate_response(prompt)
                    st.markdown(res)
                    st.session_state.messages.append({'role': 'assistant', 'content': res})
                except Exception as e:
                    error_msg = f"사 Error al procesar la respuesta: {str(e)}"
                    st.error(error_msg)
