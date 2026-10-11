import os
import pytest
from pathlib import Path
from backend.agent import agent
from backend.database import (
    init_db,
    save_ticket,
    get_ticket_by_id,
    list_tickets,
    update_ticket_status,
    update_ticket_team,
    delete_ticket,
    get_metrics,
)
from backend.schemas import TicketAnalysisRequest

@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    test_db = tmp_path / "test_maintenance.db"
    monkeypatch.setattr("backend.database.DB_PATH", test_db)
    init_db()
    yield test_db

def test_database_crud_flow():
    # 1. Save ticket
    req = TicketAnalysisRequest(description="Blade pitch error after high wind gust event", asset_type="wind", asset_id="WTG-05")
    analysis = agent.analyze_ticket(req)
    saved = save_ticket(analysis, custom_ticket_id="TEST-T001")

    assert saved.ticket_id == "TEST-T001"
    assert saved.asset_type == "wind"
    assert saved.status == "open"

    # 2. Get ticket by ID
    fetched = get_ticket_by_id("TEST-T001")
    assert fetched is not None
    assert fetched.description == req.description

    # 3. Update status
    updated_status = update_ticket_status("TEST-T001", "in_progress")
    assert updated_status is not None
    assert updated_status.status == "in_progress"

    # 4. Update team assignment
    updated_team = update_ticket_team("TEST-T001", "Wind Turbine Specialists")
    assert updated_team is not None
    assert updated_team.assigned_team == "Wind Turbine Specialists"

    # 5. List tickets
    list_res = list_tickets(asset_type="wind", status="in_progress")
    assert list_res.total >= 1
    assert any(t.ticket_id == "TEST-T001" for t in list_res.tickets)

    # 6. Get Metrics
    metrics = get_metrics()
    assert metrics.total_tickets >= 1
    assert metrics.open_tickets >= 1

    # 7. Delete ticket
    deleted = delete_ticket("TEST-T001")
    assert deleted is True
    assert get_ticket_by_id("TEST-T001") is None
