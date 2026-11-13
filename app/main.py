import json
from pathlib import Path
from app.llm import generate_response
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from app.records import (
    load_records,
    get_by_id
)

from app.smart_search import smart_search


app = FastAPI(title="StartupSetu API")

BASE_DIR = Path(__file__).resolve().parent.parent
QUESTIONS_FILE = BASE_DIR / "data" / "questions.json"


# Request model
class QuestionRequest(BaseModel):
    question: str


# GET /
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "StartupSetu API is running"
    }


# GET /records?limit=5
@app.get("/records")
def get_records(limit: int = Query(default=10, ge=1)):
    records = load_records()

    return records[:limit]


# GET /records/{id}
@app.get("/records/{record_id}")
def get_record(record_id: str):
    records = load_records()

    record = get_by_id(records, record_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    return record


# GET /search?q=startup
@app.get("/search")
def search_records(q: str = Query(..., min_length=1)):
    records = load_records()

    results = smart_search(records, q)

    return {
        "question": q,
        "total_results": len(results),
        "results": results
    }


# POST /questions
@app.post("/questions")
def save_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    QUESTIONS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if QUESTIONS_FILE.exists():
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
            questions = json.load(file)
    else:
        questions = []

    new_question = {
        "id": len(questions) + 1,
        "question": question
    }

    questions.append(new_question)

    with open(QUESTIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(questions, file, indent=4)

    return {
        "message": "Question saved successfully",
        "data": new_question
    }

class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        prompt = f"""
        You are StartupSetu, an assistant helping Indian startup founders.

        Answer questions about:
        - DPIIT Startup Recognition
        - Startup India schemes
        - Startup registration
        - Intellectual Property Rights
        - Maharashtra startup support

        Give simple and clear answers.
        Do not invent government benefits, eligibility,
        funding amounts, or legal rules.

        If the available information is insufficient,
        clearly say so.

        User question: {question}
        """

        answer = generate_response(prompt)

        return {
            "answer": answer,
            "confidence": "medium",
            "follow_up": "Would you like to explore related Startup India schemes?"
        }

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"AI service error: {str(error)}"
        )
