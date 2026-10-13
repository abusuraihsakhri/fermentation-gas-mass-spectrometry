"""Reference cases and validation for the dry off-gas molar balance."""
import math
import pytest
from offgas_analyzer.calculations import calculate_offgas


def test_inert_balance_and_rates():
    result = calculate_offgas(100, 0.21, 0.0, 0.16, 0.04)
    assert result["outlet_flow_mmol_min"] == pytest.approx(98.75)
    assert result["our_mmol_min"] == pytest.approx(5.2)
    assert result["cer_mmol_min"] == pytest.approx(3.95)
    assert result["rq"] == pytest.approx(3.95 / 5.2)
    assert result["warnings"] == []


def test_unadjusted_o2_and_co2_zero_exchange():
    result = calculate_offgas(50, 0.21, 0.0004, 0.21, 0.0004)
    assert result["our_mmol_min"] == pytest.approx(0)
    assert result["cer_mmol_min"] == pytest.approx(0)
    assert result["rq"] is None


@pytest.mark.parametrize("kwargs", [
    {"inlet_flow_mmol_min": 0},
    {"inlet_flow_mmol_min": float("nan")},
    {"inlet_flow_mmol_min": float("inf")},
    {"inlet_o2": -0.1},
    {"outlet_co2": 1.0},
    {"inlet_o2": 0.8, "inlet_co2": 0.3},
    {"outlet_o2": 0.9, "outlet_co2": 0.2},
    {"inlet_o2": True},
])
def test_invalid_inputs(kwargs):
    values = dict(inlet_flow_mmol_min=100, inlet_o2=0.21, inlet_co2=0.0004,
                  outlet_o2=0.17, outlet_co2=0.04)
    values.update(kwargs)
    with pytest.raises(ValueError):
        calculate_offgas(**values)


def test_nonpositive_oxygen_uptake_has_no_rq():
    result = calculate_offgas(100, 0.17, 0.0, 0.21, 0.01)
    assert result["our_mmol_min"] < 0
    assert result["rq"] is None
    assert result["warnings"]
