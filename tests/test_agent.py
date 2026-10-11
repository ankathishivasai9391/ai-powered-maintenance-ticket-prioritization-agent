import pytest
from backend.agent import agent
from backend.schemas import TicketAnalysisRequest

def test_predict_category_inverter():
    cat, label = agent.predict_category("Inverter 4 tripping repeatedly after noon, high temperature alarm visible", "solar")
    assert cat == "inverter_thermal"
    assert "Inverter" in label

def test_predict_category_gearbox():
    cat, label = agent.predict_category("Gearbox vibration has increased for turbine WTG-12 with abnormal noise", "wind")
    assert cat == "gearbox_vibration"

def test_determine_severity_and_priority_critical():
    sev, score, label, explanation, breakdown, indicators, safety, warning = agent.determine_severity_and_priority(
        "Gearbox vibration has increased for turbine WTG-12 with abnormal noise, fire risk", "gearbox_vibration", "wind"
    )
    assert sev == "critical"
    assert score >= 80.0
    assert label == "CRITICAL"
    assert safety is True
    assert warning is not None

def test_rag_find_similar_tickets():
    matches = agent.find_similar_tickets("SCADA data missing for block 3", top_k=2)
    assert len(matches) > 0
    assert matches[0].similarity_score > 0.0

def test_evaluate_benchmark():
    res = agent.evaluate_benchmark()
    assert res["total_labeled_examples"] >= 6
    assert res["category_accuracy"] > 0.5
    assert res["severity_accuracy"] > 0.5
