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

st.set_page_config(
    page_title="PetroGPT | Professional Engineering Suite",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS AVANZADO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*=\"st-\"] { font-family: 'Inter', sans-serif; color: #1E293B; }
    .stApp { background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%); }
    .saas-card { background-color: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 1.5rem; transition: all 0.3s ease; }
    .saas-card:hover { transform: translateY(-4px); box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.1); border-color: #3B82F6; }
    .main-header { color: #0F172A; font-weight: 700; font-size: 2.25rem; letter-spacing: -0.025em; margin-top: 1rem; }
    .sub-header { color: #64748B; font-weight: 400; font-size: 1.1rem; margin-bottom: 2rem; }
    section[data-testid=\"stSidebar\"] { background-color: #0F172A !important; }
    section[data-testid=\"stSidebar\"] * { color: #F8FAFC !important; }
    .stButton>button { background-color: #2563EB; color: white !important; border-radius: 8px; font-weight: 600; border: none; padding: 0.6rem 1.2rem; width: 100%; transition: background 0.2s; }
    .stButton>button:hover { background-color: #1D4ED8; }
    .stTabs [aria-selected=\"true\"] { background-color: #2563EB !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3662/3662860.png", width=70)
        st.markdown("## PetroGPT <span style='color:#38BDF8'>LITE</span>", unsafe_allow_html=True)
        st.markdown("--- ")
        st.markdown("**Digital Oilfield Suite**")
        st.divider()
        st.write("🟢 System: Operational")
        st.write("🤖 Model: Gemini 1.5 Flash (Free Tier)")

def main():
    render_sidebar()
    t1, t2, t3 = st.tabs(["💬 Engineering Chat", "🔢 Analysis Suite", "📊 SRT Diagnostics"])
    with t1:
        st.markdown("<h1 class='main-header'>AI Technical Assistant</h1>", unsafe_allow_html=True)
        handle_chat()
    with t2:
        st.markdown("<h1 class='main-header'>Analysis & Computation</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class=\"saas-card\">', unsafe_allow_html=True)
            st.subheader("🛢️ API Gravity Conversion")
            sg = st.number_input("Specific Gravity (γo)", 0.1, 2.0, 0.85)
            if st.button("Compute API", key="btn_api"):
                st.metric("Standard API", f"{calculate_api_gravity(sg)}°")
            st.markdown('</div>', unsafe_allow_html=True)
    with t3:
        st.markdown("<h1 class='main-header'>Step Rate Test Analytics</h1>", unsafe_allow_html=True)
        file = st.file_uploader("Drag and drop CSV logs", type=['csv'])
        if file:
            df, err = process_srt_data(file)
            if not err:
                c1, c2 = st.columns([1, 2])
                with c1: st.dataframe(df, use_container_width=True)
                with c2: st.plotly_chart(plot_srt(df), use_container_width=True)

if __name__ == '__main__':
    main()
