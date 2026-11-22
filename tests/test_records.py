from app.records import get_by_id, load_records


def test_load_records_structure():
    records = load_records()
    assert isinstance(records, list)
    assert len(records) > 0
    first = records[0]
    assert "id" in first
    assert "title" in first
    assert "category" in first


def test_get_records_endpoint_pagination(client):
    response = client.get("/records?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


def test_get_record_by_id_found(client):
    records = load_records()
    target_id = str(records[0]["id"])
    response = client.get(f"/records/{target_id}")
    assert response.status_code == 200
    assert str(response.json()["id"]) == target_id


def test_get_record_by_id_not_found(client):
    response = client.get("/records/99999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Record not found"


def test_get_by_id_helper():
    records = [{"id": 1, "title": "A"}, {"id": 2, "title": "B"}]
    assert get_by_id(records, "1") == {"id": 1, "title": "A"}
    assert get_by_id(records, "99") is None
