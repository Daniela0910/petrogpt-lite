import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
# Add the 'utils' directory to the Python path
sys.path.insert(0, './utils')
from utils.gemini_helper import generate_response
from utils.calculations import (
    calculate_api_gravity, 
    calculate_drawdown, 
    calculate_productivity_index, 
    calculate_pressure_gradient
)
from utils.srt_analyzer import process_srt_data, plot_srt

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PetroGPT Lite", page_icon="🛢️", layout="wide")

# --- OPTIMIZACIÓN CON CACHÉ ---
@st.cache_resource
def get_ai_response_cached(prompt: str) -> str:
    return generate_response(prompt)

def render_sidebar():
    with st.sidebar:
        st.title("📌 PetroGPT Info")
        st.info("Asistente modular para ingeniería de petróleos.")

def tab_chat_tecnico():
    st.header("🤖 Chat Técnico IA")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for msg in st.session_state.messages:
        st.chat_message(msg['role']).write(msg['content'])
    if prompt := st.chat_input("Consulta..."):
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        st.chat_message("user").write(prompt)
        with st.spinner("Consultando..."):
            res = get_ai_response_cached(prompt)
            st.session_state.messages.append({'role': 'assistant', 'content': res})
            st.chat_message("assistant").write(res)

def tab_calculadoras():
    st.header("🔢 Calculadoras Técnicas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("🛢️ Gravedad API"):
            density = st.number_input("Densidad (g/cm³)", 0.1, 2.0, 0.85, key="api_dens")
            if st.button("Calcular API"):
                api = calculate_api_gravity(density)
                st.metric("Resultado", f"{api}° API")

        with st.expander("📉 Drawdown de Presión"):
            pr = st.number_input("Presión de Reservorio (psi)", value=3000.0)
            pwf = st.number_input("Presión Fluyente (psi)", value=2500.0)
            if st.button("Calcular Drawdown"):
                dd = calculate_drawdown(pr, pwf)
                st.metric("Drawdown", f"{dd} psi")

    with col2:
        with st.expander("🚀 Índice de Productividad (PI)"):
            q = st.number_input("Caudal (stb/d)", value=500.0)
            pr_pi = st.number_input("Presión Reservorio (psi)", value=3000.0, key="pi_pr")
            pwf_pi = st.number_input("Presión Fluyente (psi)", value=2500.0, key="pi_pwf")
            if st.button("Calcular PI"):
                pi = calculate_productivity_index(q, pr_pi, pwf_pi)
                if pi:
                    st.metric("PI", f"{pi} stb/d/psi")
                else:
                    st.error("Revisa las presiones (Pr > Pwf)")

        with st.expander("📏 Gradiente de Presión"):
            p_grad = st.number_input("Presión (psi)", value=2000.0)
            tvd = st.number_input("Profundidad TVD (ft)", value=5000.0)
            if st.button("Calcular Gradiente"):
                grad = calculate_pressure_gradient(p_grad, tvd)
                st.metric("Gradiente", f"{(grad if grad else 0)} psi/ft")

def tab_step_rate():
    st.header("📈 Analizador SRT")
    file = st.file_uploader("Sube tu archivo SRT (CSV)", type=['csv'])
    if file:
        df, error = process_srt_data(file)
        if error: st.error(error)
        else:
            c1, c2 = st.columns([1, 2])
            with c1: st.dataframe(df)
            with c2: st.plotly_chart(plot_srt(df), use_container_width=True)

def main():
    render_sidebar()
    t1, t2, t3 = st.tabs(["💬 Chat", "🧮 Cálculos", "📂 SRT"])
    with t1: tab_chat_tecnico()
    with t2: tab_calculadoras()
    with t3: tab_step_rate()

if __name__ == "__main__":
    main()
