from typing import Optional, Tuple
import numpy as np


# ==========================================
# HELPER DE VALIDACIÓN
# ==========================================

def validate_range(
    value: float,
    min_value: float,
    max_value: float,
    variable_name: str
) -> Optional[str]:
    """
    Valida si un valor está dentro de un rango físico razonable.
    """

    if value < min_value or value > max_value:
        return (
            f"{variable_name} fuera de rango físico "
            f"razonable ({min_value} - {max_value})."
        )

    return None


# ==========================================
# PROPIEDADES DE FLUIDOS
# ==========================================

def calculate_api_gravity(
    density_g_cm3: float
) -> Tuple[Optional[float], Optional[str]]:
    """
    Calcula gravedad API.

    Fórmula:
        API = (141.5 / SG) - 131.5
    """

    if density_g_cm3 <= 0:
        return None, (
            "La densidad debe ser mayor que 0 g/cm³."
        )

    warning = validate_range(
        density_g_cm3,
        0.5,
        1.5,
        "Densidad"
    )

    api = (141.5 / density_g_cm3) - 131.5

    return round(api, 2), warning


# ==========================================
# ANÁLISIS DE PRODUCCIÓN
# ==========================================

def calculate_drawdown(
    reservoir_pressure: float,
    bottomhole_pressure: float
) -> Tuple[Optional[float], Optional[str]]:
    """
    Calcula Drawdown del pozo.

    Fórmula:
        DD = Pr - Pwf
    """

    if reservoir_pressure <= 0:
        return None, (
            "La presión de yacimiento debe ser mayor que 0 psi."
        )

    if bottomhole_pressure < 0:
        return None, (
            "La presión de fondo fluyente no puede ser negativa."
        )

    if bottomhole_pressure > reservoir_pressure:
        return None, (
            "La presión de fondo fluyente no puede ser "
            "mayor que la presión de yacimiento."
        )

    warning = validate_range(
        reservoir_pressure,
        100,
        20000,
        "Presión de yacimiento"
    )

    drawdown = reservoir_pressure - bottomhole_pressure

    return round(drawdown, 2), warning


def calculate_productivity_index(
    flow_rate: float,
    reservoir_pressure: float,
    bottomhole_pressure: float
) -> Tuple[Optional[float], Optional[str]]:
    """
    Calcula Productivity Index (PI).

    Fórmula:
        PI = q / (Pr - Pwf)
    """

    if flow_rate < 0:
        return None, (
            "La tasa de producción no puede ser negativa."
        )

    drawdown, error = calculate_drawdown(
        reservoir_pressure,
        bottomhole_pressure
    )

    if drawdown is None:
        return None, error

    if drawdown <= 0:
        return None, (
            "El drawdown debe ser mayor que cero."
        )

    pi = flow_rate / drawdown

    warning = None

    if pi > 50:
        warning = (
            "El PI calculado es muy alto. "
            "Verifica presiones y tasa de producción."
        )

    return round(pi, 4), warning


# ==========================================
# PRESIÓN Y GRADIENTES
# ==========================================

def calculate_pressure_gradient(
    pressure: float,
    tvd: float
) -> Tuple[Optional[float], Optional[str]]:
    """
    Calcula gradiente de presión.

    Fórmula:
        Gradiente = P / TVD
    """

    if pressure < 0:
        return None, (
            "La presión no puede ser negativa."
        )

    if tvd <= 0:
        return None, (
            "La TVD debe ser mayor que cero."
        )

    gradient = pressure / tvd

    warning = None

    if gradient < 0.1 or gradient > 1.2:
        warning = (
            "El gradiente calculado está fuera "
            "de un rango típico (0.1 - 1.2 psi/ft)."
        )

    return round(gradient, 4), warning


# ==========================================
# IPR VOGEL
# ==========================================

def calculate_vogel_qmax(
    q_test: float,
    reservoir_pressure: float,
    flowing_pressure: float
) -> Tuple[Optional[float], Optional[str]]:
    """
    Calcula qmax usando la ecuación de Vogel.

    Fórmula:
        q/qmax = 1 - 0.2(Pwf/Pr) - 0.8(Pwf/Pr)^2
    """

    if q_test <= 0:
        return None, (
            "La tasa de prueba debe ser mayor que cero."
        )

    if reservoir_pressure <= 0:
        return None, (
            "La presión de yacimiento debe ser mayor que cero."
        )

    if flowing_pressure < 0:
        return None, (
            "La presión fluyente no puede ser negativa."
        )

    if flowing_pressure >= reservoir_pressure:
        return None, (
            "La presión fluyente debe ser menor "
            "que la presión de yacimiento."
        )

    denominator = (
        1
        - 0.2 * (flowing_pressure / reservoir_pressure)
        - 0.8 * ((flowing_pressure / reservoir_pressure) ** 2)
    )

    if denominator <= 0:
        return None, (
            "La ecuación Vogel produjo un denominador inválido."
        )

    qmax = q_test / denominator

    warning = None

    if qmax > 100000:
        warning = (
            "El qmax calculado es extremadamente alto. "
            "Verifica unidades y datos de entrada."
        )

    return round(qmax, 2), warning


def generate_vogel_ipr(
    qmax: float,
    reservoir_pressure: float,
    points: int = 25
) -> Tuple[Optional[np.ndarray], Optional[list], Optional[str]]:
    """
    Genera datos para construir curva IPR Vogel.

    Returns:
        pwf_values : np.ndarray
        q_values   : list
        warning    : str
    """

    if qmax <= 0:
        return None, None, (
            "qmax debe ser mayor que cero."
        )

    if reservoir_pressure <= 0:
        return None, None, (
            "La presión de yacimiento debe ser mayor que cero."
        )

    if points <= 1:
        return None, None, (
            "El número de puntos debe ser mayor que 1."
        )

    pwf_values = np.linspace(
        0,
        reservoir_pressure,
        points
    )

    q_values = []

    for pwf in pwf_values:

        q = qmax * (
            1
            - 0.2 * (pwf / reservoir_pressure)
            - 0.8 * ((pwf / reservoir_pressure) ** 2)
        )

        q_values.append(round(q, 2))

    warning = None

    if reservoir_pressure > 20000:
        warning = (
            "La presión de yacimiento es muy alta. "
            "Verifica unidades."
        )

    return pwf_values, q_values, warning
