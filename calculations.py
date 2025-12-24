"""
Calculations extracted from Capacitance.ipynb.

This module contains *pure* functions (no interactive input/print) so it can be
imported by a Streamlit app or any other UI.

Units:
- Area: cm^2
- Distance/gap: mm
- Capacitance outputs: F (and you can convert to pF/nF as needed)
- Voltage: V
- Volume: mL
- Resistance: MΩ
"""

import math

# --- Constants / assumptions ---
EPSILON_0 = 8.854e-12      # Vacuum permittivity [F/m]

# Dielectric constant options (as in the notebook):
EPSILON_R_PLASTIC = 2.5    # Plastic bag (polyethylene-like)
EPSILON_R_GLASS = 7.0      # Glass (wine glass)

# Default used in the notebook at upload time:
EPSILON_R_DEFAULT = EPSILON_R_GLASS

REMAINING_FRACTION = 0.60  # 40% lost => 60% remaining


# --- Script A: Capacitance (parallel plate) ---
def calculate_capacitance(area_cm2: float, distance_mm: float, *, epsilon_r: float = EPSILON_R_DEFAULT) -> float:
    """Return capacitance (F) of an ideal parallel-plate capacitor with dielectric.

    C = ε0 * εr * A / d

    Parameters
    ----------
    area_cm2 : float
        Plate area in cm^2.
    distance_mm : float
        Plate separation in mm.
    epsilon_r : float, optional (keyword-only)
        Relative permittivity of dielectric. Defaults to EPSILON_R_DEFAULT.

    Returns
    -------
    float
        Capacitance in Farads (F).
    """
    if distance_mm <= 0:
        raise ValueError("distance_mm must be > 0")
    if area_cm2 < 0:
        raise ValueError("area_cm2 must be >= 0")
    if epsilon_r <= 0:
        raise ValueError("epsilon_r must be > 0")

    # Unit conversions
    area_m2 = area_cm2 * 1e-4       # cm^2 -> m^2
    distance_m = distance_mm * 1e-3 # mm -> m

    return EPSILON_0 * epsilon_r * area_m2 / distance_m


# --- Script B: Charge density ---
def charge_density(capacitance_pF: float, voltage_V: float, volume_mL: float) -> float:
    """Return charge density in µC/L.

    Q = C * V
    density = Q / volume

    Parameters
    ----------
    capacitance_pF : float
        Capacitance in picoFarads.
    voltage_V : float
        Voltage in Volts.
    volume_mL : float
        Volume of negative plate in milliliters.

    Returns
    -------
    float
        Charge density in microCoulombs per liter (µC/L).
    """
    if volume_mL <= 0:
        raise ValueError("volume_mL must be > 0")
    if capacitance_pF < 0:
        raise ValueError("capacitance_pF must be >= 0")

    # Unit conversions
    capacitance_F = capacitance_pF * 1e-12  # pF -> F
    volume_L = volume_mL * 1e-3            # mL -> L

    charge_C = capacitance_F * voltage_V
    return (charge_C * 1e6) / volume_L     # C -> µC


# --- Script C: RC discharge time (to lose 40% charge) ---
def time_to_lose_40_percent(R_MOhm: float, C_pF: float, *, remaining_fraction: float = REMAINING_FRACTION) -> float:
    """Return time (seconds) for an RC discharge to reach `remaining_fraction`.

    V(t)/V0 = exp(-t/RC)  =>  t = -RC * ln(remaining_fraction)

    Parameters
    ----------
    R_MOhm : float
        Resistance in mega-ohms (MΩ).
    C_pF : float
        Capacitance in pico-farads (pF).
    remaining_fraction : float, optional (keyword-only)
        Fraction remaining (0 < f <= 1). Defaults to 0.60 (i.e., 40% lost).

    Returns
    -------
    float
        Time in seconds.
    """
    if R_MOhm < 0:
        raise ValueError("R_MOhm must be >= 0")
    if C_pF < 0:
        raise ValueError("C_pF must be >= 0")
    if not (0 < remaining_fraction <= 1):
        raise ValueError("remaining_fraction must be in (0, 1]")

    # Unit conversions
    R_ohms = R_MOhm * 1e6     # MΩ -> Ω
    C_farads = C_pF * 1e-12   # pF -> F

    return -R_ohms * C_farads * math.log(remaining_fraction)
