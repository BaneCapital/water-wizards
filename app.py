import streamlit as st
import calculations as calc

st.title("Water Wizards – Calculators")

# =========================
# Block 1: Capacitance
# =========================
st.header("1) Capacitance (parallel-plate)")

area_cm2 = st.number_input(
    "Plate area (cm²)",
    min_value=0.0,
    value=10.0,
    step=1.0,
    key="cap_area",
)

gap_mm = st.number_input(
    "Plate gap (mm)",
    min_value=0.000001,
    value=1.000,
    step=0.001,
    format="%.3f",
    key="cap_gap",
)

dielectric = st.selectbox(
    "Dielectric",
    ["Glass (εr = 7.0)", "Plastic bag (εr = 2.5)"],
    key="cap_dielectric",
)
epsilon_r = 7.0 if dielectric.startswith("Glass") else 2.5

try:
    C_F = calc.calculate_capacitance(
        area_cm2=area_cm2,
        distance_mm=gap_mm,
        epsilon_r=epsilon_r,
    )
    C_pF = C_F * 1e12
    C_nF = C_F * 1e9

    st.success("Capacitance calculated")
    st.write(f"Capacitance: {C_F:.3e} F")
    st.write(f"Capacitance: {C_pF:.2f} pF")
    st.write(f"Capacitance: {C_nF:.3f} nF")
    
    if st.button("Use this capacitance in Charge density (Block 2)"):
        st.session_state["dens_C_pF"] = float(C_pF)

    if st.button("Use this capacitance in RC time (Block 3)"):
        st.session_state["rc_C"] = float(C_pF)
    
except Exception as e:
    st.error(f"Capacitance error: {e}")

st.divider()

# =========================
# Block 2: Charge density
# =========================
st.header("2) Charge density")

C2_pF = st.number_input(
    "Capacitance (pF)",
    min_value=0.0,
    value=100.0,
    step=1.0,
    format="%.3f",
    key="dens_C_pF",
)

V_V = st.number_input(
    "Voltage (V)",
    value=1000.0,
    step=10.0,
    key="dens_V",
)

volume_mL = st.number_input(
    "Negative plate volume (mL)",
    min_value=0.000001,
    value=50.0,
    step=1.0,
    key="dens_vol",
)

try:
    density = calc.charge_density(
        capacitance_pF=C2_pF,
        voltage_V=V_V,
        volume_mL=volume_mL,
    )
    st.success("Charge density calculated")
    st.write(f"Charge density: {density:.3f} µC/L")
except Exception as e:
    st.error(f"Charge density error: {e}")

st.divider()

# =========================
# Block 3: RC discharge time
# =========================
st.header("3) RC discharge time")

R_MOhm = st.number_input(
    "Resistance (MΩ)",
    min_value=0.0,
    value=100.0,
    step=1.0,
    key="rc_R",
)

C3_pF = st.number_input(
    "Capacitance (pF)",
    min_value=0.0,
    value=100.0,
    step=1.0,
    format="%.3f",
    key="rc_C",
)

remaining_pct = st.number_input(
    "Remaining charge (%)",
    min_value=0.0,
    max_value=100.0,
    value=60.0,   # default = “lose 40%”
    step=1.0,
    key="rc_remaining_pct",
)
remaining_fraction = remaining_pct / 100.0

try:
    # If your calculations.py doesn't accept remaining_fraction, remove the keyword arg line.
    t_s = calc.time_to_lose_40_percent(
        R_MOhm=R_MOhm,
        C_pF=C3_pF,
        remaining_fraction=remaining_fraction,
    )
    st.success("Discharge time calculated")
    st.write(f"Time to reach {remaining_pct:.1f}% remaining: {t_s:.3f} s")
except TypeError:
    # Fallback if your function signature doesn't accept remaining_fraction
    try:
        t_s = calc.time_to_lose_40_percent(R_MOhm=R_MOhm, C_pF=C3_pF)
        st.success("Discharge time calculated")
        st.write(f"Time to lose 40% of charge: {t_s:.3f} s")
        st.info("Note: your calculations.py doesn't expose a configurable remaining fraction yet.")
    except Exception as e:
        st.error(f"RC time error: {e}")
except Exception as e:
    st.error(f"RC time error: {e}")

