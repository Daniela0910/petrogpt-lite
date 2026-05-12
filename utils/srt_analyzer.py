import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Optional, Tuple

def calculate_intersection(df: pd.DataFrame) -> Tuple[Optional[float], Optional[float], Optional[dict]]:
    """Encuentra el punto de quiebre óptimo y el intercepto entre dos tendencias."""
    if len(df) < 4: return None, None, None
    
    df = df.sort_values('rate')
    best_r2 = -1
    best_split = None
    
    # Buscar el punto de quiebre que maximice el R^2 combinado
    for i in range(2, len(df) - 2):
        d1, d2 = df.iloc[:i+1], df.iloc[i:]
        reg1 = LinearRegression().fit(d1[['rate']], d1['pressure'])
        reg2 = LinearRegression().fit(d2[['rate']], d2['pressure'])
        r2 = reg1.score(d1[['rate']], d1['pressure']) + reg2.score(d2[['rate']], d2['pressure'])
        if r2 > best_r2:
            best_r2 = r2
            best_split = (i, reg1, reg2)
            
    if best_split:
        idx, r1, r2 = best_split
        m1, b1 = r1.coef_[0], r1.intercept_
        m2, b2 = r2.coef_[0], r2.intercept_
        
        # m1*x + b1 = m2*x + b2  => x(m1-m2) = b2-b1
        if m1 != m2:
            x_int = (b2 - b1) / (m1 - m2)
            y_int = m1 * x_int + b1
            return x_int, y_int, {'m1': m1, 'b1': b1, 'm2': m2, 'b2': b2}
    return None, None, None

def process_srt_data(file) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    try:
        df = pd.read_csv(file)
        if df.empty: return None, "Archivo vacío."
        if not all(c in df.columns for c in ['rate', 'pressure']): return None, "Columnas faltantes."
        return df, None
    except Exception as e: return None, str(e)

def plot_srt(df: pd.DataFrame):
    x_int, y_int, lines = calculate_intersection(df)
    
    fig = px.scatter(df, x='rate', y='pressure', title='Análisis de Presión de Fractura (SRT)')
    
    if x_int and lines:
        # Línea 1 (Matriz)
        x1 = np.array([df['rate'].min(), x_int])
        fig.add_trace(go.Scatter(x=x1, y=lines['m1']*x1+lines['b1'], 
                                 name='Tendencia Matriz', line=dict(color='blue', dash='dash')))
        # Línea 2 (Fractura)
        x2 = np.array([x_int, df['rate'].max()])
        fig.add_trace(go.Scatter(x=x2, y=lines['m2']*x2+lines['b2'], 
                                 name='Tendencia Fractura', line=dict(color='green', dash='dash')))
        # Punto de Intercepto
        fig.add_trace(go.Scatter(x=[x_int], y=[y_int], name=f'Fractura: {round(y_int,1)} psi', 
                                 marker=dict(color='black', size=15, symbol='x')))
        
    fig.update_layout(template="plotly_white", xaxis_title="Tasa (bbl/d)", yaxis_title="Presión (psi)")
    return fig
