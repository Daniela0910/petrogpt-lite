import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Optional, Tuple


# =========================================================
# CÁLCULO DE INTERSECCIÓN (PUNTO DE FRACTURA)
# =========================================================

def calculate_intersection(
    df: pd.DataFrame
) -> Tuple[Optional[float], Optional[float], Optional[dict]]:
    """
    Encuentra el punto de quiebre óptimo entre:
    - Tendencia matriz
    - Tendencia fractura
    """

    if len(df) < 4:
        return None, None, None

    df = df.sort_values("rate")

    best_r2 = -1
    best_split = None

    # Buscar mejor punto de quiebre
    for i in range(2, len(df) - 2):

        d1 = df.iloc[:i + 1]
        d2 = df.iloc[i:]

        reg1 = LinearRegression().fit(
            d1[["rate"]],
            d1["bottomhole_pressure"]
        )

        reg2 = LinearRegression().fit(
            d2[["rate"]],
            d2["bottomhole_pressure"]
        )

        r2_total = (
            reg1.score(d1[["rate"]], d1["bottomhole_pressure"]) +
            reg2.score(d2[["rate"]], d2["bottomhole_pressure"])
        )

        if r2_total > best_r2:

            best_r2 = r2_total

            best_split = (
                i,
                reg1,
                reg2
            )

    if best_split:

        idx, reg1, reg2 = best_split

        m1 = reg1.coef_[0]
        b1 = reg1.intercept_

        m2 = reg2.coef_[0]
        b2 = reg2.intercept_

        # Intersección
        if m1 != m2:

            x_int = (b2 - b1) / (m1 - m2)

            y_int = m1 * x_int + b1

            return x_int, y_int, {
                "m1": m1,
                "b1": b1,
                "m2": m2,
                "b2": b2
            }

    return None, None, None


# =========================================================
# CÁLCULO DE PRESIÓN DE FRICCIÓN
# =========================================================

def calculate_friction_pressure(
    rate_bpd: float,
    tubing_id_in: float,
    tubing_length_ft: float,
    fluid_density_ppg: float,
    viscosity_cp: float
) -> float:
    """
    Estimación simplificada de pérdida por fricción.

    Modelo simplificado tipo Darcy-Weisbach adaptado
    para aplicaciones petroleras.
    """

    if tubing_id_in <= 0:
        return 0

    if tubing_length_ft <= 0:
        return 0

    # Conversión de caudal
    q_ft3_s = rate_bpd * 5.615 / 86400

    # Área tubing
    tubing_id_ft = tubing_id_in / 12

    area = np.pi * (tubing_id_ft ** 2) / 4

    velocity = q_ft3_s / area

    # Factor viscosidad simplificado
    friction_factor = 0.02 + (viscosity_cp / 10000)

    # Presión fricción
    dp = (
        friction_factor
        * tubing_length_ft
        * fluid_density_ppg
        * (velocity ** 2)
        / (25 * tubing_id_ft)
    )

    return round(dp, 2)


# =========================================================
# CONVERSIÓN WHP -> BHP
# =========================================================

def calculate_bottomhole_pressure(
    wellhead_pressure: float,
    tubing_length_ft: float,
    fluid_density_ppg: float,
    friction_pressure: float
) -> float:
    """
    Convierte presión de cabeza a presión de fondo.

    BHP = WHP + Hidrostática + Fricción
    """

    hydrostatic = 0.052 * fluid_density_ppg * tubing_length_ft

    bhp = (
        wellhead_pressure
        + hydrostatic
        + friction_pressure
    )

    return round(bhp, 2)


# =========================================================
# PROCESAMIENTO SRT
# =========================================================

def process_srt_data(
    file,
    tubing_id_in: float,
    tubing_length_ft: float,
    fluid_density_ppg: float,
    viscosity_cp: float
) -> Tuple[Optional[pd.DataFrame], Optional[str]]:

    try:

        df = pd.read_csv(file)

        if df.empty:
            return None, "Archivo vacío."

        # Validar columnas requeridas
        required_cols = ["rate", "pressure"]

        if not all(col in df.columns for col in required_cols):

            return None, (
                "El archivo debe contener columnas:"
                " rate y pressure"
            )

        # =========================================
        # CÁLCULO DE PRESIÓN DE FRICCIÓN
        # =========================================

        friction_list = []
        bhp_list = []

        for _, row in df.iterrows():

            friction = calculate_friction_pressure(
                rate_bpd=row["rate"],
                tubing_id_in=tubing_id_in,
                tubing_length_ft=tubing_length_ft,
                fluid_density_ppg=fluid_density_ppg,
                viscosity_cp=viscosity_cp
            )

            bhp = calculate_bottomhole_pressure(
                wellhead_pressure=row["pressure"],
                tubing_length_ft=tubing_length_ft,
                fluid_density_ppg=fluid_density_ppg,
                friction_pressure=friction
            )

            friction_list.append(friction)
            bhp_list.append(bhp)

        df["friction_pressure"] = friction_list

        df["bottomhole_pressure"] = bhp_list

        return df, None

    except Exception as e:

        return None, str(e)


# =========================================================
# PLOT SRT
# =========================================================

def plot_srt(df: pd.DataFrame):

    x_int, y_int, lines = calculate_intersection(df)

    fig = px.scatter(
        df,
        x="rate",
        y="bottomhole_pressure",
        title="Step Rate Test Analysis"
    )

    # =========================================
    # TENDENCIAS
    # =========================================

    if x_int is not None and lines is not None:

        # Línea matriz
        x1 = np.array([
            df["rate"].min(),
            x_int
        ])

        y1 = (
            lines["m1"] * x1
            + lines["b1"]
        )

        fig.add_trace(
            go.Scatter(
                x=x1,
                y=y1,
                mode="lines",
                name="Matrix Trend",
                line=dict(
                    color="blue",
                    dash="dash"
                )
            )
        )

        # Línea fractura
        x2 = np.array([
            x_int,
            df["rate"].max()
        ])

        y2 = (
            lines["m2"] * x2
            + lines["b2"]
        )

        fig.add_trace(
            go.Scatter(
                x=x2,
                y=y2,
                mode="lines",
                name="Fracture Trend",
                line=dict(
                    color="green",
                    dash="dash"
                )
            )
        )

        # Punto fractura
        fig.add_trace(
            go.Scatter(
                x=[x_int],
                y=[y_int],
                mode="markers",
                name=f"Fracture Pressure = {round(y_int, 1)} psi",
                marker=dict(
                    color="red",
                    size=12,
                    symbol="x"
                )
            )
        )

    # =========================================
    # ESTILO
    # =========================================

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Injection Rate (bbl/d)",
        yaxis_title="Bottomhole Pressure (psi)",
        height=650
    )

    return fig
