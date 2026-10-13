import csv
from fastapi.testclient import TestClient
from agents.api import app
from cli import main as generic_cli
from offgas_analyzer.cli import main as domain_cli

client = TestClient(app)


def test_local_console_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "Operations Console" in response.text


def test_calculation_endpoint():
    response = client.post("/api/offgas/calculate", json={
        "inlet_flow_mmol_min": 100, "inlet_o2": 0.21,
        "inlet_co2": 0, "outlet_o2": 0.16, "outlet_co2": 0.04,
    })
    assert response.status_code == 200
    assert abs(response.json()["rq"] - (3.95 / 5.2)) < 1e-10


def test_calculation_invalid_fraction():
    response = client.post("/api/offgas/calculate", json={
        "inlet_flow_mmol_min": 100, "inlet_o2": 1.1,
        "inlet_co2": 0, "outlet_o2": 0.16, "outlet_co2": 0.04,
    })
    assert response.status_code == 422


def test_domain_calculation_cli(capsys):
    code = domain_cli([
        "calculate", "--flow", "100", "--inlet-o2", "0.21", "--inlet-co2", "0",
        "--outlet-o2", "0.16", "--outlet-co2", "0.04"
    ])
    assert code == 0
    assert '"rq"' in capsys.readouterr().out


def test_cli_batch_false_is_not_truthy(tmp_path):
    source = tmp_path / "input.csv"
    source.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n"
        "A,ONE,12,4,False,NOMINAL\n"
        "B,TWO,12,4,True,NOMINAL\n", encoding="utf-8"
    )
    for handler, name, expected_field in [
        (generic_cli, "generic.csv", "overall_urgency"),
        (domain_cli, "domain.csv", "overall_status"),
    ]:
        destination = tmp_path / name
        assert handler(["batch", "-i", str(source), "-o", str(destination)]) == 0
        with destination.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        assert len(rows) == 2
        assert int(rows[0]["critical_count"]) == 0 if "critical_count" in rows[0] else rows[0]["overall_urgency"] == "ROUTINE"
        assert rows[1][expected_field].startswith("CRITICAL")
