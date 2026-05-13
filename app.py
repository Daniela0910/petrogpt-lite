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

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PetroGPT Lite | Education Edition", page_icon="🛢️", layout="wide")

# --- ESTILOS PERSONALIZADOS (Look & Feel Académico) ---
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    .main-header { color: #1E3A8A; font-size: 32px; font-weight: bold; margin-bottom: 10px; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1E3A8A; color: white; }
    .stExpander { background-color: white; border-radius: 10px; border: 1px solid #E5E7EB; }
    </style>
""", unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.title("🎓 PetroGPT Lite")
        st.markdown("**Portal de Aprendizaje e Ingeniería**")
        st.info("Esta herramienta asiste a estudiantes en la resolución de problemas técnicos y análisis de pruebas de pozo.")
        st.divider()
        st.caption("⚙️ Backend: Gemini 1.5 Flash")
        st.caption("🔒 Seguridad: Secrets Activados")

def tab_calculadoras():
    st.markdown("<h2 class='main-header'>🔢 Calculadoras de Ingeniería</h2>", unsafe_allow_html=True)
    st.write("Calcula parámetros críticos de producción y yacimientos con fórmulas estándar.")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("🛢️ Cálculo de Gravedad API", expanded=True):
            density = st.number_input("Densidad Relativa (g/cm³)", 0.1, 2.0, 0.85, help="La densidad relativa del crudo respecto al agua.")
            if st.button("Ejecutar Cálculo API"):
                api = calculate_api_gravity(density)
                st.metric("Gravedad API", f"{api}°", delta_color="normal")
        
        with st.expander("📉 Análisis de Drawdown"):
            pr_dd = st.number_input("Presión de Yacimiento (Pr)", value=3000.0, key="pr_dd_main")
            pwf_dd = st.number_input("Presión Fluyente (Pwf)", value=2500.0, key="pwf_dd_main")
            st.metric("Drawdown (ΔP)", f"{calculate_drawdown(pr_dd, pwf_dd)} psi")

    with col2:
        with st.expander("🚀 Índice de Productividad (PI)", expanded=True):
            q = st.number_input("Caudal de Producción (stb/d)", value=500.0)
            pi = calculate_productivity_index(q, 3000.0, 2500.0)
            st.metric("PI", f"{pi} stb/d/psi", help="Indica la capacidad productiva del pozo.")

def tab_step_rate():
    st.markdown("<h2 class='main-header'>📈 Analizador SRT Profesional</h2>", unsafe_allow_html=True)
    st.write("Sube tus datos de presión vs tasa para identificar la presión de fractura.")
    
    file = st.file_uploader("Cargar archivo de datos (CSV)", type=['csv'])
    if file:
        df, err = process_srt_data(file)
        if not err:
            c1, c2 = st.columns([1, 2])
            with c1: 
                st.markdown("**Vista de Tabla**")
                st.dataframe(df, use_container_width=True, height=400)
            with c2: 
                st.markdown("**Gráfico de Tendencias**")
                st.plotly_chart(plot_srt(df), use_container_width=True)

def main():
    render_sidebar()
    t1, t2, t3 = st.tabs(["💬 Chat con IA", "🧮 Calculadoras", "📊 Análisis SRT"])
    with t1: 
        st.markdown("<h2 class='main-header'>🤖 Asistente Técnico</h2>", unsafe_allow_html=True)
        handle_chat()
    with t2: tab_calculadoras()
    with t3: tab_step_rate()

if __name__ == '__main__':
    main()
