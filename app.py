# =========================================
# TAB CALCULADORAS
# =========================================
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

        # -------------------------------------
        # API GRAVITY
        # -------------------------------------
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)

        st.subheader("🛢️ API Gravity Conversion")

        st.caption("""
        Convierte gravedad específica del fluido (Specific Gravity)
        a gravedad API.
        """)

        sg = st.number_input(
            "Specific Gravity (γo)",
            min_value=0.1,
            max_value=2.0,
            value=0.85
        )

        if st.button("Compute API"):

            api, warning = calculate_api_gravity(sg)

            if warning:
                st.warning(warning)

            if api is not None:

                st.metric(
                    "Standard API",
                    f"{api:.2f}°"
                )

            else:
                st.error("Invalid density value.")

        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------------------
        # DRAWDOWN
        # -------------------------------------
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)

        st.subheader("📉 Drawdown Status")

        st.caption("""
        Calcula el drawdown del pozo (Pr - Pwf),
        representando la caída de presión entre
        el yacimiento y el fondo fluyente.
        """)

        pr = st.number_input(
            "Static Pressure Pr (psi)",
            value=3000.0
        )

        pwf = st.number_input(
            "Flowing Pressure Pwf (psi)",
            value=2500.0
        )

        dd, warning = calculate_drawdown(pr, pwf)

        if warning:
            st.warning(warning)

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

        # -------------------------------------
        # PRODUCTIVITY INDEX
        # -------------------------------------
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)

        st.subheader("🚀 Productivity Index (PI)")

        st.caption("""
        Evalúa la capacidad productiva del pozo
        mediante la relación entre tasa de producción
        y drawdown.
        """)

        flow = st.number_input(
            "Daily Rate q (stb/d)",
            value=500.0
        )

        pi_val, warning = calculate_productivity_index(
            flow,
            pr,
            pwf
        )

        if warning:
            st.warning(warning)

        if pi_val is not None:

            st.metric(
                "PI Metric",
                f"{pi_val:.4f} stb/d/psi"
            )

        else:
            st.error("Invalid PI input data.")

        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------------------
        # PRESSURE GRADIENT
        # -------------------------------------
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)

        st.subheader("📏 Vertical Gradient")

        st.caption("""
        Calcula el gradiente de presión vertical
        usando presión observada y TVD.
        """)

        p_grad = st.number_input(
            "Observed Pressure (psi)",
            value=1500.0
        )

        depth = st.number_input(
            "TVD (ft)",
            value=5000.0
        )

        grad, warning = calculate_pressure_gradient(
            p_grad,
            depth
        )

        if warning:
            st.warning(warning)

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
    Genera una curva IPR utilizando
    la ecuación de Vogel para estimar
    el comportamiento de producción
    y la capacidad máxima del pozo.
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

        qmax, warning = calculate_vogel_qmax(
            q_test,
            pr_vogel,
            pwf_vogel
        )

        if warning:
            st.warning(warning)

        if qmax is not None:

            st.metric(
                "Estimated qmax",
                f"{qmax:.2f} stb/d"
            )

            pwf_vals, q_vals, warning = generate_vogel_ipr(
                qmax,
                pr_vogel
            )

            if warning:
                st.warning(warning)

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
