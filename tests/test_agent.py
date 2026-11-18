from app.agent_loop import run_agent_loop
from app.tools import (
    check_dpiit_eligibility,
    get_scheme_details,
    submit_dpiit_application,
)


def test_check_dpiit_eligibility_eligible():
    result = check_dpiit_eligibility(
        entity_type="Private Limited Company",
        incorporation_year=2024,
        annual_turnover_cr=2.5,
        is_innovative=True,
        current_year=2026,
    )
    assert result["is_eligible"] is True
    assert result["years_active"] == 2
    assert len(result["recommended_benefits"]) > 0


def test_check_dpiit_eligibility_ineligible_entity():
    result = check_dpiit_eligibility(
        entity_type="Sole Proprietorship",
        incorporation_year=2024,
        annual_turnover_cr=0.5,
        is_innovative=True,
        current_year=2026,
    )
    assert result["is_eligible"] is False
    assert result["criteria"]["entity_type_valid"] is False


def test_check_dpiit_eligibility_ineligible_age():
    result = check_dpiit_eligibility(
        entity_type="Private Limited Company",
        incorporation_year=2012,
        annual_turnover_cr=5.0,
        is_innovative=True,
        current_year=2026,
    )
    assert result["is_eligible"] is False
    assert result["criteria"]["age_under_10_years"] is False


def test_get_scheme_details_known():
    res = get_scheme_details("seed_fund")
    assert res["found"] is True
    assert "Startup India Seed Fund Scheme" in res["scheme"]["name"]


def test_submit_dpiit_application():
    res = submit_dpiit_application(
        startup_name="Test Robotics Pvt Ltd",
        entity_type="Private Limited Company",
        founder_name="Pooja Sharma",
        email="pooja@testrobotics.com",
    )
    assert res["status"] == "success"
    assert "DPIIT-APP-" in res["application"]["application_id"]


def test_hand_written_agent_loop():
    res = run_agent_loop("Check eligibility: LLP incorporated in 2025 with 1 cr turnover")
    assert "check_dpiit_eligibility" in res["tool_calls"]
    assert "ELIGIBLE" in res["answer"]


def test_agent_endpoint_approval_flow(client):
    # Trigger sensitive application tool -> should ask for approval
    req1 = {"query": "Please submit my application for DPIIT registration"}
    r1 = client.post("/agent", json=req1)
    assert r1.status_code == 200
    data1 = r1.json()
    assert data1["status"] == "needs_approval"
    thread_id = data1["thread_id"]

    # Confirm approval with thread_id -> should execute and complete
    req2 = {
        "query": "Confirming my submission",
        "thread_id": thread_id,
        "approved": True,
    }
    r2 = client.post("/agent", json=req2)
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["status"] == "completed"
    assert "Approved & Submitted" in data2["response"]
