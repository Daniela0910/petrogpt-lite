import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from sklearn.linear_model import LinearRegression
from typing import Optional, Tuple


# =========================================================
# CALCULAR INTERSECCIÓN SRT
# =========================================================

def calculate_intersection(
    df: pd.DataFrame
) -> Tuple[Optional[float], Optional[float], Optional[dict]]:

    if len(df) < 4:
        return None, None, None

    df = df.sort_values('rate')

    best_r2 = -1
    best_split = None

    for i in range(2, len(df) - 2):

        d1 = df.iloc[:i+1]
        d2 = df.iloc[i:]

        reg1 = LinearRegression().fit(
            d1[['rate']],
            d1['bottomhole_pressure']
        )

        reg2 = LinearRegression().fit(
            d2[['rate']],
            d2['bottomhole_pressure']
        )

        r2 = (
            reg1.score(d1[['rate']], d1['bottomhole_pressure']) +
            reg2.score(d2[['rate']], d2['bottomhole_pressure'])
        )

        if r2 > best_r2:

            best_r2 = r2

            best_split = (
                i,
                reg1,
                reg2
            )

    if best_split:

        idx, r1, r2 = best_split

        m1 = r1.coef_[0]
        b1 = r1.intercept_

        m2 = r2.coef_[0]
        b2 = r2.intercept_

        if m1 != m2:

            x_int = (b2 - b1) / (m1 - m2)

            y_int = m1 * x_int + b1

            return x_int, y_int, {
                'm1': m1,
                'b1': b1,
                'm2': m2,
                'b2': b2
            }

    return None, None, None


# =========================================================
# CÁLCULO DE PRESIÓN HIDROSTÁTICA
# =========================================================

def calculate_hydrostatic_pressure(
    fluid_density_ppg: float,
    tubing_length_ft: float
):

    return 0.052 * fluid_density_ppg * tubing_length_ft


# =========================================================
# CÁLCULO DE FRICCIÓN
# =========================================================

def calculate_friction_pressure(
    rate_bpm: float,
    tubing_id_in: float,
    tubing_length_ft: float,
    viscosity_cp: float
):

    if tubing_id_in <= 0:
        return 0

    friction = (
        0.0001 *
        viscosity_cp *
        tubing_length_ft *
        (rate_bpm ** 1.85) /
        (tubing_id_in ** 4.8655)
    )

    return friction


# =========================================================
# PROCESAMIENTO SRT
# =========================================================

def process_srt_data(
    file,
    fluid_density_ppg: float,
    tubing_length_ft: float,
    tubing_id_in: float,
    viscosity_cp: float
):

    try:

        df = pd.read_csv(file)

        if df.empty:
            return None, "Archivo vacío."

        required_cols = ['rate', 'pressure']

        if not all(col in df.columns for col in required_cols):
            return None, "El CSV debe contener columnas: rate y pressure"

        # =================================================
        # PRESIÓN HIDROSTÁTICA
        # =================================================

        hydrostatic_pressure = calculate_hydrostatic_pressure(
            fluid_density_ppg,
            tubing_length_ft
        )

        df['hydrostatic_pressure'] = hydrostatic_pressure

        # =================================================
        # PRESIÓN DE FRICCIÓN
        # =================================================

        df['friction_pressure'] = df['rate'].apply(
            lambda q: calculate_friction_pressure(
                rate_bpm=q,
                tubing_id_in=tubing_id_in,
                tubing_length_ft=tubing_length_ft,
                viscosity_cp=viscosity_cp
            )
        )

        # =================================================
        # PRESIÓN DE FONDO
        # =================================================

        df['bottomhole_pressure'] = (
            df['pressure'] +
            df['hydrostatic_pressure'] +
            df['friction_pressure']
        )

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
        x='rate',
        y='bottomhole_pressure',
        title='Step Rate Test Analysis'
    )

    if x_int is not None and lines is not None:

        x1 = np.array([
            df['rate'].min(),
            x_int
        ])

        y1 = lines['m1'] * x1 + lines['b1']

        fig.add_trace(
            go.Scatter(
                x=x1,
                y=y1,
                mode='lines',
                name='Matrix Trend'
            )
        )

        x2 = np.array([
            x_int,
            df['rate'].max()
        ])

        y2 = lines['m2'] * x2 + lines['b2']

        fig.add_trace(
            go.Scatter(
                x=x2,
                y=y2,
                mode='lines',
                name='Fracture Trend'
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[x_int],
                y=[y_int],
                mode='markers',
                name=f'Fracture Pressure = {round(y_int,1)} psi',
                marker=dict(
                    size=14,
                    symbol='x'
                )
            )
        )

    fig.update_layout(

        template="plotly_white",

        xaxis_title="Injection Rate",

        yaxis_title="Bottomhole Pressure (psi)"
    )

    return fig
