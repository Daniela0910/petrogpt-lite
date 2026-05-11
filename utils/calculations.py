from typing import Optional

def calculate_api_gravity(density_g_cm3: float) -> Optional[float]:
    """Calcula la gravedad API a partir de la densidad."""
    try:
        api = (141.5 / density_g_cm3) - 131.5
        return round(api, 2)
    except ZeroDivisionError:
        return None

def calculate_drawdown(reservoir_pressure: float, bottomhole_pressure: float) -> float:
    """
    Calcula el Drawdown (caída de presión).
    Fórmula: Drawdown = Pr - Pwf
    """
    return reservoir_pressure - bottomhole_pressure

def calculate_productivity_index(flow_rate: float, reservoir_pressure: float, bottomhole_pressure: float) -> Optional[float]:
    """
    Calcula el Índice de Productividad (PI).
    Fórmula: PI = q / (Pr - Pwf)
    """
    drawdown = calculate_drawdown(reservoir_pressure, bottomhole_pressure)
    if drawdown <= 0:
        return None
    return round(flow_rate / drawdown, 4)

def calculate_pressure_gradient(pressure: float, tvd: float) -> Optional[float]:
    """
    Calcula el Gradiente de Presión.
    Fórmula: Gradiente = Presión / TVD
    """
    if tvd <= 0:
        return None
    return round(pressure / tvd, 4)
