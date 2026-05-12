import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
sys.path.insert(0, './utils')
from utils.gemini_helper import generate_response
from utils.calculations import (
    calculate_api_gravity,
    calculate_drawdown,
    calculate_productivity_index,
    calculate_pressure_gradient
)
from utils.srt_analyzer import process_srt_data, plot_srt

st.set_page_config(page_title="PetroGPT Lite", page_icon="🛢️", layout="wide")

def render_sidebar():
    with st.sidebar:
        st.title("📌 PetroGPT Lite")
        st.info("Asistente inteligente interno para ingeniería de petróleos.")
        st.divider()
        st.caption("Acceso seguro: API Key configurada internamente.")

def tab_chat_tecnico():
    st.header("🤖 Chat Técnico IA")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for msg in st.session_state.messages:
        st.chat_message(msg['role']).write(msg['content'])

    if prompt := st.chat_input("Consulta técnica..."):
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        st.chat_message("user").write(prompt)
        with st.spinner("Consultando..."):
            res = generate_response(prompt)
            st.session_state.messages.append({'role': 'assistant', 'content': res})
            st.chat_message("assistant").write(res)

def tab_calculadoras():
    st.header("🔢 Calculadoras Técnicas")
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("🛢️ Gravedad API", expanded=True):
            density = st.number_input("Densidad (g/cm³)", 0.1, 2.0, 0.85, key="api_dens")
            if st.button("Calcular API"):
                st.metric("Resultado", f"{calculate_api_gravity(density)}° API")

        with st.expander("📉 Drawdown"):
            pr_dd = st.number_input("Presión de Yacimiento (psi)", value=3000.0, key="pr_dd")
            pwf_dd = st.number_input("Presión Fluyente (psi)", value=2500.0, key="pwf_dd")
            if st.button("Calcular Drawdown"):
                st.metric("Drawdown", f"{calculate_drawdown(pr_dd, pwf_dd)} psi")

    with col2:
        with st.expander("🚀 Índice de Productividad (PI)", expanded=True):
            q_pi = st.number_input("Caudal (stb/d)", value=500.0, key="q_pi")
            pr_pi = st.number_input("Presión de Yacimiento (psi)", value=3000.0, key="pr_pi")
            pwf_pi = st.number_input("Presión Fluyente (psi)", value=2500.0, key="pwf_pi")
            if st.button("Calcular PI"):
                pi = calculate_productivity_index(q_pi, pr_pi, pwf_pi)
                if pi:
                    st.metric("PI", f"{pi} stb/d/psi")
                else:
                    st.error("El drawdown debe ser mayor a 0")

        with st.expander("📏 Gradiente de Presión"):
            p_grad = st.number_input("Presión (psi)", value=1000.0, key="p_grad")
            tvd_grad = st.number_input("TVD (ft)", value=2000.0, key="tvd_grad")
            if st.button("Calcular Gradiente"):
                grad = calculate_pressure_gradient(p_grad, tvd_grad)
                st.metric("Gradiente", f"{grad} psi/ft")

def tab_step_rate():
    st.header("📈 Analizador SRT")
    file = st.file_uploader("Sube archivo SRT (CSV)", type=['csv'])
    if file:
        df, error = process_srt_data(file)
        if error:
            st.error(error)
        else:
            col_table, col_plot = st.columns([1, 2])
            with col_table:
                st.subheader("📊 Datos de Entrada")
                st.dataframe(df, use_container_width=True, height=450)
            with col_plot:
                st.plotly_chart(plot_srt(df), use_container_width=True)

def main():
    render_sidebar()
    t1, t2, t3 = st.tabs(["💬 Chat Técnico", "🧮 Cálculos", "📈 Analizador SRT"])
    with t1: tab_chat_tecnico()
    with t2: tab_calculadoras()
    with t3: tab_step_rate()

if __name__ == '__main__':
    main()
