"""Dry off-gas molar balance for fermentation process measurements.

Gas fractions must be dry, dimensionless mole fractions at comparable
measurement conditions. The unmeasured gas remainder is assumed inert and
conserved (e.g. N2/Ar). Gas flow is expressed in mmol/min.
"""
import math
from typing import Any, Dict


def calculate_offgas(
    inlet_flow_mmol_min: float,
    inlet_o2: float,
    inlet_co2: float,
    outlet_o2: float,
    outlet_co2: float,
) -> Dict[str, Any]:
    """Calculate OUR, CER and RQ using an inert-gas corrected outlet flow.

    OUR and CER are net mmol/min for the complete vessel gas stream,
    not volumetric rates normalized to broth volume.
    """
    fields = {
        "inlet_flow_mmol_min": inlet_flow_mmol_min,
        "inlet_o2": inlet_o2,
        "inlet_co2": inlet_co2,
        "outlet_o2": outlet_o2,
        "outlet_co2": outlet_co2,
    }
    for name, value in fields.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{name} must be a finite number")
    if inlet_flow_mmol_min <= 0:
        raise ValueError("inlet_flow_mmol_min must be greater than zero")
    for name in ("inlet_o2", "inlet_co2", "outlet_o2", "outlet_co2"):
        if not 0 <= fields[name] <= 1:
            raise ValueError(f"{name} must be a fraction between 0 and 1")

    inert_in = 1 - inlet_o2 - inlet_co2
    inert_out = 1 - outlet_o2 - outlet_co2
    if inert_in <= 0 or inert_out <= 0:
        raise ValueError("inlet and outlet O2 + CO2 fractions must each be less than 1")

    outlet_flow = inlet_flow_mmol_min * inert_in / inert_out
    our = inlet_flow_mmol_min * inlet_o2 - outlet_flow * outlet_o2
    cer = outlet_flow * outlet_co2 - inlet_flow_mmol_min * inlet_co2
    warnings = []
    if our <= 0:
        warnings.append("Net oxygen uptake is zero or negative; RQ is undefined.")
    if cer < 0:
        warnings.append("Net carbon dioxide evolution is negative; check conditions and sensor calibration.")

    return {
        "outlet_flow_mmol_min": outlet_flow,
        "our_mmol_min": our,
        "cer_mmol_min": cer,
        "rq": cer / our if our > 0 else None,
        "warnings": warnings,
    }
