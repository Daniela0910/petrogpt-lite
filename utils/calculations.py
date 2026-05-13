from typing import Optional
import numpy as np

# ==========================================
# PROPIEDADES DE FLUIDOS
# ==========================================

def calculate_api_gravity(density_g_cm3: float) -> Optional[float]:
    """
    Calcula gravedad API a partir de densidad relativa.

    Fórmula:
        API = (141.5 / SG) - 131.5
    """

    if density_g_cm3 <= 0:
        return None

    api = (141.5 / density_g_cm3) - 131.5

    return round(api, 2)


# ==========================================
# ANÁLISIS DE PRODUCCIÓN
# ==========================================

def calculate_drawdown(
    reservoir_pressure: float,
    bottomhole_pressure: float
) -> Optional[float]:
    """
    Calcula Drawdown del pozo.

    Fórmula:
        DD = Pr - Pwf
    """

    if reservoir_pressure <= 0 or bottomhole_pressure < 0:
        return None

    if bottomhole_pressure > reservoir_pressure:
        return None

    drawdown = reservoir_pressure - bottomhole_pressure

    return round(drawdown, 2)


def calculate_productivity_index(
    flow_rate: float,
    reservoir_pressure: float,
    bottomhole_pressure: float
) -> Optional[float]:
    """
    Calcula Productivity Index (PI).

    Fórmula:
        PI = q / (Pr - Pwf)
    """

    if flow_rate < 0:
        return None

    drawdown = calculate_drawdown(
        reservoir_pressure,
        bottomhole_pressure
    )

    if not drawdown or drawdown <= 0:
        return None

    pi = flow_rate / drawdown

    return round(pi, 4)


# ==========================================
# PRESIÓN Y GRADIENTES
# ==========================================

def calculate_pressure_gradient(
    pressure: float,
    tvd: float
) -> Optional[float]:
    """
    Calcula gradiente de presión.

    Fórmula:
        Gradiente = P / TVD
    """

    if pressure < 0 or tvd <= 0:
        return None

    gradient = pressure / tvd

    return round(gradient, 4)

    
    def calculate_vogel_qmax(
    q_test: float,
    reservoir_pressure: float,
    flowing_pressure: float
):
    """
    Calcula qmax usando la ecuación de Vogel.

    Fórmula:
    q/qmax = 1 - 0.2(Pwf/Pr) - 0.8(Pwf/Pr)^2
    """

    if reservoir_pressure <= 0:
        return None

    if flowing_pressure >= reservoir_pressure:
        return None

    denominator = (
        1
        - 0.2 * (flowing_pressure / reservoir_pressure)
        - 0.8 * ((flowing_pressure / reservoir_pressure) ** 2)
    )

    if denominator <= 0:
        return None

    qmax = q_test / denominator

    return round(qmax, 2)


def generate_vogel_ipr(
    qmax: float,
    reservoir_pressure: float,
    points: int = 20
):
    """
    Genera datos para curva IPR Vogel.
    """

    if qmax <= 0 or reservoir_pressure <= 0:
        return None, None

    pwf_values = np.linspace(0, reservoir_pressure, points)

    q_values = []

    for pwf in pwf_values:

        q = qmax * (
            1
            - 0.2 * (pwf / reservoir_pressure)
            - 0.8 * ((pwf / reservoir_pressure) ** 2)
        )

        q_values.append(round(q, 2))

    return pwf_values, q_values
