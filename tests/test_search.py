from app.records import load_records
from app.smart_search import smart_search


def test_smart_search_keyword_matching():
    records = load_records()
    results = smart_search(records, "DPIIT")
    assert isinstance(results, list)
    assert len(results) > 0


def test_smart_search_empty_query():
    records = load_records()
    results = smart_search(records, "")
    assert isinstance(results, list)
    assert len(results) == 0


def test_search_endpoint(client):
    response = client.get("/search?q=funding")
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "funding"
    assert data["total_results"] >= 0
    assert "results" in data


def test_search_endpoint_missing_param(client):
    response = client.get("/search")
    assert response.status_code == 422
