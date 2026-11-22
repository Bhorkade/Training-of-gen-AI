from unittest.mock import patch

from app.rag import rag_answer


def test_ask_endpoint_with_fake_llm(client):
    fake_response = {
        "question": "What is DPIIT recognition?",
        "answer": "DPIIT recognition is an official initiative by the Government of India for startups.",
        "citations": [
            {
                "title": "DPIIT Startup Recognition Guidelines",
                "page": 1,
                "source": "https://www.startupindia.gov.in/"
            }
        ],
        "refused": False,
        "retrieved_chunks": []
    }

    with patch("app.main.rag_answer", return_value=fake_response):
        response = client.post("/ask", json={"question": "What is DPIIT recognition?"})
        assert response.status_code == 200
        data = response.json()
        assert data["refused"] is False
        assert "DPIIT recognition is an official initiative" in data["answer"]
        assert len(data["citations"]) == 1
        assert data["citations"][0]["page"] == 1


def test_ask_endpoint_empty_question(client):
    response = client.post("/ask", json={"question": "   "})
    assert response.status_code == 400
    assert "Question cannot be empty" in response.json()["detail"]


def test_rag_answer_unanswerable_refusal():
    out_of_scope = "What are the lunar exploration subsidies offered by NASA to Indian startups?"
    res = rag_answer(out_of_scope)
    assert res["refused"] is True
    assert len(res["citations"]) == 0
    assert "cannot find sufficient information" in res["answer"].lower()
