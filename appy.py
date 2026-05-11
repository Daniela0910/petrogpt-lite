import streamlit as st
import pandas as pd
import plotly.express as px
from utils.gemini_helper import generate_response
from utils.calculations import calculate_api_gravity
from utils.srt_analyzer import process_srt_data, plot_srt

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PetroGPT Lite", page_icon="🛒", layout="wide")

def render_sidebar():
    with st.sidebar:
        st.title("📌 PetroGPT Info")
        st.info("Asistente modular para ingeniería de petróleos.")

def tab_chat_tecnico():
    st.header("🤖 Chat Técnico IA")
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages: st.chat_message(msg['role']).write(msg['content'])
    if prompt := st.chat_input("Consulta..."):
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        st.chat_message("user").write(prompt)
        res = generate_response(prompt)
        st.session_state.messages.append({'role': 'assistant', 'content': res})
        st.chat_message("assistant").write(res)

def tab_calculadoras():
    st.header("🔢 Cálculos")
    density = st.number_input("Densidad (g/cm³)", 0.1, 2.0, 0.85)
    if st.button("Calcular API"):
        api = calculate_api_gravity(density)
        st.metric("Gravedad API", f"{api}°")

def tab_step_rate():
    st.header("📈 Analizador SRT")
    file = st.file_uploader("Sube tu archivo SRT (CSV)", type=['csv'])
    if file:
        df, error = process_srt_data(file)
        if error: st.error(error)
        else:
            col1, col2 = st.columns([1, 2])
            with col1: st.dataframe(df, use_container_width=True)
            with col2: st.plotly_chart(plot_srt(df), use_container_width=True)
            
            if st.button("🦮 Interpretar con IA"):
                with st.spinner("Analizando tendencia..."):
                    prompt = f"Analiza estos datos de Step Rate Test: {df.to_string()}. Identifica visualmente si hay un quiebre de pendiente que indique presión de fractura y da una recomendación técnica breve."
                    st.info(generate_response(prompt))

def main():
    render_sidebar()
    t1, t2, t3 = st.tabs(["💬 Chat", "🧮 Cálculos", "📂 SRT"])
    with t1: tab_chat_tecnico()
    with t2: tab_calculadoras()
    with t3: tab_step_rate()

if __name__ == "__main__": main()
