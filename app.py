import streamlit as st
import pandas as pd
import sys
import os

# Configuración de rutas para módulos
sys.path.insert(0, os.path.abspath('./utils'))

from utils.chat_handler import handle_chat
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
        st.info("Asistente modular para ingeniería de petróleos.")
        st.divider()
        st.caption("Seguridad: API Key vía Secrets configurada.")

def tab_calculadoras():
    st.header("🔢 Calculadoras Técnicas")
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("🛢️ Gravedad API", expanded=True):
            density = st.number_input("Densidad (g/cm³)", 0.1, 2.0, 0.85, key="api_dens")
            if st.button("Calcular API"):
                st.metric("Resultado", f"{calculate_api_gravity(density)}° API")
        with st.expander("📉 Drawdown"):
            pr_dd = st.number_input("Presión Yacimiento (psi)", value=3000.0, key="pr_dd_calc")
            pwf_dd = st.number_input("Presión Fluyente (psi)", value=2500.0, key="pwf_dd_calc")
            st.metric("Drawdown", f"{calculate_drawdown(pr_dd, pwf_dd)} psi")

    with col2:
        with st.expander("🚀 Índice de Productividad (PI)", expanded=True):
            q = st.number_input("Caudal (stb/d)", value=500.0)
            pi = calculate_productivity_index(q, 3000.0, 2500.0)
            st.metric("PI", f"{pi} stb/d/psi")

def tab_step_rate():
    st.header("📈 Analizador SRT")
    file = st.file_uploader("Subir CSV", type=['csv'])
    if file:
        df, err = process_srt_data(file)
        if not err:
            c1, c2 = st.columns([1, 2])
            with c1: st.dataframe(df, use_container_width=True, height=450)
            with c2: st.plotly_chart(plot_srt(df), use_container_width=True)

def main():
    render_sidebar()
    t1, t2, t3 = st.tabs(["💬 Chat Técnico", "🧮 Cálculos", "📉 Analizador SRT"])
    with t1: handle_chat()
    with t2: tab_calculadoras()
    with t3: tab_step_rate()

if __name__ == '__main__':
    main()
