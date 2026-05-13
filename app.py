import streamlit as st
import pandas as pd
import sys
import os
import plotly.graph_objects as go
from utils.srt_analyzer import (
    process_srt_data,
    plot_srt
)

# Configuración de rutas para módulos
sys.path.insert(0, os.path.abspath('./utils'))

from utils.chat_handler import handle_chat

from utils.calculations import (
    calculate_api_gravity,
    calculate_drawdown,
    calculate_productivity_index,
    calculate_pressure_gradient,
    calculate_vogel_qmax,
    generate_vogel_ipr
)

from utils.srt_analyzer import process_srt_data, plot_srt


# --- CONFIGURACIÓN DE PÁGINA ---
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

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        color: #1E293B;
    }

    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
    }

    .saas-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }

    .saas-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.1);
        border-color: #3B82F6;
    }

    .main-header {
        color: #0F172A;
        font-weight: 700;
        font-size: 2.25rem;
        letter-spacing: -0.025em;
        margin-top: 1rem;
    }

    .sub-header {
        color: #64748B;
        font-weight: 400;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
    }

    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    .stButton>button {
        background-color: #2563EB;
        color: white !important;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1.2rem;
        width: 100%;
        transition: background 0.2s;
    }

    .stButton>button:hover {
        background-color: #1D4ED8;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #E2E8F0;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #2563EB !important;
        color: white !important;
    }

    </style>
""", unsafe_allow_html=True)


# --- SESSION STATE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []


# --- SIDEBAR ---
def render_sidebar():

    with st.sidebar:

        st.image(
            "assets/logo_petrogpt.png",
            width=200
        )

        st.markdown(
            "## PetroGPT <span style='color:#38BDF8'>PRO</span>",
            unsafe_allow_html=True
        )

        st.markdown("---")

        st.markdown("**Digital Oilfield Suite**")
        st.caption("Engineering Edition v2.5")
        st.markdown("---")
        
        st.markdown("**PetroGPT PRO**")
        st.caption("""PetroGPT PRO es una plataforma integral de ingeniería digital diseñada para ingenieros de petróleos, producción y yacimientos. La aplicación combina herramientas avanzadas de análisis, cálculos de desempeño de pozos, asistencia técnica con inteligencia artificial y diagnóstico de pruebas de inyección en un único entorno profesional.
                      La plataforma está diseñada con una interfaz moderna inspirada en soluciones de Digital Oilfield utilizadas en la industria energética, ofreciendo herramientas rápidas, confiables y prácticas para apoyar la toma de decisiones en operaciones de producción, yacimientos e inyección.""")
        st.divider()

        st.write("🟢 System: Operational")
        st.write("🤖 Model: Gemini 2.5 Pro")


# --- TAB CALCULADORAS ---
def tab_calculadoras():

    st.markdown(
        "<h1 class='main-header'>Analysis & Computation</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p class='sub-header'>Verified industry standard algorithms for well performance evaluation.</p>",
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    # =========================================
    # COLUMNA 1
    # =========================================
    with c1:

        # --- API ---
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)

        st.subheader("🛢️ API Gravity Conversion")
        st.caption("""
        Convierte gravedad específica del fluido (Specific Gravity) a gravedad API.
        Útil para caracterizar crudos y clasificar la calidad del petróleo.
        """)
        sg = st.number_input(
            "Specific Gravity (γo)",
            min_value=0.1,
            max_value=2.0,
            value=0.85
        )

        if st.button("Compute API"):

            api = calculate_api_gravity(sg)

            if api is not None:
                st.metric("Standard API", f"{api:.2f}°")
            else:
                st.error("Invalid density value.")

        st.markdown('</div>', unsafe_allow_html=True)

        # --- DRAWDOWN ---
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)

        st.subheader("📉 Drawdown Status")
        st.caption("""
        Calcula el drawdown del pozo (Pr - Pwf), representando la caída de presión
        entre el yacimiento y el fondo fluyente del pozo.
        """)
        pr = st.number_input(
            "Static Pressure Pr (psi)",
            value=3000.0
        )

        pwf = st.number_input(
            "Flowing Pressure Pwf (psi)",
            value=2500.0
        )

        dd = calculate_drawdown(pr, pwf)

        if dd is not None:
            st.metric(
                "Differential Pressure",
                f"{dd:.2f} psi"
            )
        else:
            st.error("Invalid pressure data.")

        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================
    # COLUMNA 2
    # =========================================
    with c2:

        # --- PI ---
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)

        st.subheader("🚀 Productivity Index (PI)")
        st.caption("""
        Evalúa la capacidad productiva del pozo mediante la relación entre tasa de producción
        y drawdown. Un PI alto indica mejor desempeño del pozo.
        """)
        flow = st.number_input(
            "Daily Rate q (stb/d)",
            value=500.0
        )

        pi_val = calculate_productivity_index(flow, pr, pwf)

        if pi_val is not None:
            st.metric(
                "PI Metric",
                f"{pi_val:.4f} stb/d/psi"
            )
        else:
            st.error("Invalid PI input data.")

        st.markdown('</div>', unsafe_allow_html=True)

        # --- GRADIENT ---
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)

        st.subheader("📏 Vertical Gradient")
        st.caption("""
        Calcula el gradiente de presión vertical usando presión observada y TVD.
        Útil para análisis hidráulico y evaluación de fluidos.
        """)
        
        p_grad = st.number_input(
            "Observed Pressure (psi)",
            value=1500.0
        )

        depth = st.number_input(
            "TVD (ft)",
            value=5000.0
        )

        grad = calculate_pressure_gradient(p_grad, depth)

        if grad is not None:
            st.metric(
                "Gradient",
                f"{grad:.4f} psi/ft"
            )
        else:
            st.error("Invalid gradient data.")

        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================
    # VOGEL IPR
    # =========================================
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)

    st.subheader("📈 Vogel IPR")
    st.caption("""
    Genera una curva IPR utilizando la ecuación de Vogel para estimar
    el comportamiento de producción y la capacidad máxima del pozo (qmax).
    """)

    pr_vogel = st.number_input(
        "Reservoir Pressure Pr (psi)",
        value=3000.0,
        key="ipr_pr"
    )

    pwf_vogel = st.number_input(
        "Flowing Pressure Pwf (psi)",
        value=1500.0,
        key="ipr_pwf"
    )

    q_test = st.number_input(
        "Test Rate q (stb/d)",
        value=800.0,
        key="ipr_q"
    )

    if st.button("Generate IPR"):

        qmax = calculate_vogel_qmax(
            q_test,
            pr_vogel,
            pwf_vogel
        )

        if qmax is not None:

            st.metric(
                "Estimated qmax",
                f"{qmax:.2f} stb/d"
            )

            pwf_vals, q_vals = generate_vogel_ipr(
                qmax,
                pr_vogel
            )

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=q_vals,
                    y=pwf_vals,
                    mode='lines',
                    name='Vogel IPR'
                )
            )

            fig.update_layout(
                title="IPR Curve",
                xaxis_title="Flow Rate (stb/d)",
                yaxis_title="Bottomhole Pressure (psi)",
                template="plotly_white",
                height=500
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.error("Invalid Vogel input data.")

    st.markdown('</div>', unsafe_allow_html=True)


# --- TAB SRT ---
# --- TAB SRT ---
def tab_step_rate():

    st.markdown(
        "<h1 class='main-header'>Step Rate Test Analytics</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class='sub-header'>
        Convert surface injection pressures to bottomhole pressure
        using hydrostatic and friction corrections.
        </p>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # INPUTS HIDRÁULICOS
    # =====================================================

    st.markdown('<div class="saas-card">', unsafe_allow_html=True)

    st.subheader("⚙️ Well & Fluid Parameters")
    st.caption("""
    Ingrese propiedades del fluido y condiciones de tubería utilizadas para convertir
    presiones de cabeza a presión de fondo mediante correcciones hidráulicas.
    """)

    c1, c2 = st.columns(2)

    with c1:

        fluid_density = st.number_input(
            "Fluid Density (ppg)",
            min_value=1.0,
            value=9.0,
            step=0.1
        )

        tubing_id = st.number_input(
            "Tubing ID (in)",
            min_value=0.5,
            value=2.441,
            step=0.01
        )

    with c2:

        tvd = st.number_input(
            "True Vertical Depth TVD (ft)",
            min_value=100.0,
            value=8500.0,
            step=100.0
        )

        viscosity = st.number_input(
            "Fluid Viscosity (cp)",
            min_value=0.1,
            value=1.0,
            step=0.1
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # CARGA DE ARCHIVO
    # =====================================================

    st.markdown('<div class="saas-card">', unsafe_allow_html=True)

    file = st.file_uploader(
        "Upload SRT CSV File",
        type=['csv']
    )

    st.caption("""
    Required columns:
    - rate
    - pressure

    Example:
    rate,pressure
    1,1200
    2,1350
    3,1500
    """)

    st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # PROCESAMIENTO
    # =====================================================

    if file:

        with st.spinner("Processing SRT data..."):

            df, err = process_srt_data(
            file=file,
            fluid_density_ppg=fluid_density,
            tubing_length_ft=tvd,
            tubing_id_in=tubing_id,
            viscosity_cp=viscosity
        )

        if err:

            st.error(err)

        else:

            # =============================================
            # MÉTRICAS PRINCIPALES
            # =============================================

            st.markdown('<div class="saas-card">', unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Average Hydrostatic Pressure",
                    f"{df['hydrostatic_pressure'].mean():.1f} psi"
                )

            with c2:

                st.metric(
                    "Average Friction Pressure",
                    f"{df['friction_pressure'].mean():.1f} psi"
                )

            with c3:

                st.metric(
                    "Max Bottomhole Pressure",
                    f"{df['bottomhole_pressure'].max():.1f} psi"
                )

            st.markdown('</div>', unsafe_allow_html=True)

            # =============================================
            # TABLA + GRÁFICA
            # =============================================

            col_tab, col_graph = st.columns([1, 2])

            # ---------------------------------------------
            # TABLA
            # ---------------------------------------------

            with col_tab:

                st.markdown(
                    '<div class="saas-card">',
                    unsafe_allow_html=True
                )

                st.subheader("📋 Processed Data")
                st.caption("""
                Tabla procesada del Step Rate Test con correcciones hidrostáticas,
                fricción y cálculo de presión de fondo.
                """)

                st.dataframe(
                    df,
                    use_container_width=True,
                    height=500
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            # ---------------------------------------------
            # GRÁFICA
            # ---------------------------------------------

            with col_graph:

                st.markdown(
                    '<div class="saas-card">',
                    unsafe_allow_html=True
                )

                st.subheader("📈 Bottomhole Pressure Analysis")
                st.caption("""
                Visualización del comportamiento de presión de fondo vs tasa de inyección
                para identificar presión de fractura y cambios de tendencia.
                """)

                fig = plot_srt(df)

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            # =============================================
            # DESCARGA CSV
            # =============================================

            csv = df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="⬇️ Download Processed SRT",
                data=csv,
                file_name="processed_srt.csv",
                mime="text/csv"
            )


# --- MAIN ---
def main():

    render_sidebar()

    t1, t2, t3 = st.tabs([
        "💬 Engineering Chat",
        "🔢 Analysis Suite",
        "📊 SRT Diagnostics"
    ])

    with t1:
         st.markdown(
            """
            <p class='sub-header'>
            Asistente técnico especializado en ingeniería de petróleos, producción,
            yacimientos, pruebas de pozo e inyección.
            </p>
            """,
            unsafe_allow_html=True
        )

        handle_chat()

    with t2:
        tab_calculadoras()

    with t3:
        tab_step_rate()


# --- RUN APP ---
if __name__ == '__main__':
    main()
