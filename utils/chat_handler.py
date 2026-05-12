import streamlit as st
from utils.gemini_helper import generate_response

def handle_chat():
    """Gestiona la interfaz y lógica del chat técnico."""
    st.header("🤖 Chat Técnico IA")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

    if prompt := st.chat_input("Consulta técnica..."):
      st.session_state.messages.append({'role': 'user', 'content': prompt})
      with st.chat_message("user"):
          st.markdown(prompt)

      with st.chat_message("assistant"):
          with st.spinner("Consultando..."):
              try:
                  res = generate_response(prompt)
                  st.markdown(res)
                  st.session_state.messages.append({'role': 'assistant', 'content': res})
              except Exception as e:
                  st.error(f"❌ Error en el chat: {str(e)}")
