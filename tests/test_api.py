import pytest
from fastapi.testclient import TestClient
from backend.app import app
from backend.database import init_db

@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    test_db = tmp_path / "test_api_maintenance.db"
    monkeypatch.setattr("backend.database.DB_PATH", test_db)
    init_db()
    yield test_db

client = TestClient(app)

def test_demo_endpoint():
    response = client.get("/api/demo")
    assert response.status_code == 200
    data = response.json()
    assert data["case_study"] == "AI Agent for Maintenance Ticket Prioritization"
    assert "status" in data

def test_run_endpoint():
    response = client.post("/api/run", json={"text": "Inverter 4 tripping repeatedly after noon"})
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "analysis" in data
    assert data["analysis"]["category"] == "inverter_thermal"

def test_analyze_endpoint():
    payload = {
        "description": "Gearbox vibration has increased for turbine WTG-12 with abnormal noise",
        "asset_type": "wind",
        "asset_id": "WTG-12"
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["severity"] == "critical"
    assert data["priority_label"] == "CRITICAL"
    assert data["assigned_team"] == "Wind Mechanical Maintenance"

def test_create_and_manage_ticket_endpoint():
    payload = {
        "description": "Inspection checklist pending for spillway gate maintenance",
        "asset_type": "hydro",
        "asset_id": "HYD-SP-01"
    }
    # Create ticket
    res_create = client.post("/api/tickets", json=payload)
    assert res_create.status_code == 201
    ticket = res_create.json()
    t_id = ticket["ticket_id"]
    assert ticket["status"] == "open"

    # Get single ticket
    res_get = client.get(f"/api/tickets/{t_id}")
    assert res_get.status_code == 200
    assert res_get.json()["asset_id"] == "HYD-SP-01"

    # Patch status
    res_status = client.patch(f"/api/tickets/{t_id}/status", json={"status": "in_progress"})
    assert res_status.status_code == 200
    assert res_status.json()["status"] == "in_progress"

    # Patch team assignment
    res_team = client.patch(f"/api/tickets/{t_id}/assign", json={"team": "Hydro Maintenance Crew"})
    assert res_team.status_code == 200
    assert res_team.json()["assigned_team"] == "Hydro Maintenance Crew"

    # List tickets
    res_list = client.get("/api/tickets?status=in_progress")
    assert res_list.status_code == 200
    assert res_list.json()["total"] >= 1

    # Delete ticket
    res_del = client.delete(f"/api/tickets/{t_id}")
    assert res_del.status_code == 200

    # Verify deleted
    res_get_del = client.get(f"/api/tickets/{t_id}")
    assert res_get_del.status_code == 404

def test_metrics_endpoint():
    response = client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_tickets" in data
    assert "severity_distribution" in data

def test_evaluation_endpoint():
    response = client.get("/api/evaluation")
    assert response.status_code == 200
    data = response.json()
    assert data["total_labeled_examples"] >= 6
    assert "category_accuracy" in data

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"

