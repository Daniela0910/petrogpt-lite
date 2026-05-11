import pandas as pd
import plotly.express as px
import streamlit as st
from typing import Optional, Tuple

def process_srt_data(file) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Lee y valida el archivo CSV del Step Rate Test.
    """
    try:
        df = pd.read_csv(file)
        if df.empty:
            return None, "El archivo está vacío."
        
        required_cols = ['rate', 'pressure']
        if not all(col in df.columns for col in required_cols):
            return None, f"Faltan columnas requeridas. El CSV debe tener: {required_cols}"
        
        return df, None
    except Exception as e:
        return None, f"Error al leer el archivo: {e}"

def plot_srt(df: pd.DataFrame):
    """
    Genera una gráfica interactiva de Presión vs Tasa de inyección.
    """
    fig = px.scatter(
        df, x='rate', y='pressure', 
        title='Análisis Step Rate Test (SRT)',
        labels={'rate': 'Tasa de Inyección (bbl/d)', 'pressure': 'Presión (psi)'},
        trendline="ols",
        template="plotly_white"
    )
    fig.update_traces(marker=dict(size=12, color='red', symbol='circle'))
    return fig
